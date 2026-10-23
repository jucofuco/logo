# Plan: quantize the Supertonic 3 model ourselves (speed test)

Written 2026-10-23 for an implementing agent. Read `CLAUDE.md` first (the "Web version" section
and owner preferences). Reminders that matter here:

- Answer the owner in the language of their last message (Slovak or English), short and concrete.
- Commit messages: only what the commit did. **No Co-Authored-By line.** `git push origin main`
  after each commit.
- This runs on a Raspberry Pi (Linux). The Swift/iOS side is not touched by this plan.
- **Only use the official model** that is already in `web/model/onnx/` (pinned revision of
  `supertone-oss-archive/supertonic-3`, fetched by `web/fetch_model.sh`). **Do not download
  quantized or converted models made by other people, and never run scripts that come with them.**
  We build our own variants from the official files.
- Model files are big. Never commit them. Variants go in `web/model-q/` (add it to `.gitignore`).
- The web server is already running (`python3 web/serve.py 8500`, plus `tailscale serve` on
  `https://rpi-dev.tail2bb2c8.ts.net:8443`). Do not stop it. Files under `web/` are served as they
  are. If you must restart it: `setsid nohup python3 web/serve.py 8500 > <scratchpad>/serve.log 2>&1 < /dev/null &`.
- Python installs: use a virtualenv **outside the repo** (`~/venvs/quant`), run scripts with
  `python3 -I` style isolation where they read files you did not write. If `pip install` is
  denied by the permission system, stop and ask the owner to approve it.

## Why

The web prototype runs the model in the browser (ONNX Runtime Web, WASM on CPU). Measured on the
owner's iPhone 12 mini over https with 4 threads: about 3.2 s for one short phrase at 8 steps,
2.3 s at 6 steps (about 0.45 s per step). The iPhone with WebGPU crashed the tab (most likely out
of memory, the model is 398 MB in fp32). A Mac with Firefox needs 0.8 s. The time is the model
compute, mostly `vector_estimator` which runs once per step.

Goal: find out whether a smaller or quantized variant of our own making is clearly faster on CPU
and/or small enough for WebGPU, without making the voice worse. Deliver numbers and listening
samples, the owner decides.

## What is known about this model (do not rely on it, verify)

- Four ONNX files: `duration_predictor` (3.7 MB), `text_encoder` (36 MB), `vector_estimator`
  (257 MB, run once per denoising step), `vocoder` (101 MB, run once).
- Other people report: int8 on everything breaks the voice (word error rate explodes), a
  dynamically quantized vocoder adds audible noise, int8 on Conv nodes can produce `ConvInteger`
  ops that some ONNX Runtime builds do not implement. int8 on `MatMul` only (Conv left in fp32) and
  fp16 are reported as safe. Weight-only int8 may be converted back to fp32 at load time (smaller
  download, same speed). Treat all of this as hints to test, not facts.

## Part 1: setup and inspection

1. `python3 -m venv ~/venvs/quant && ~/venvs/quant/bin/pip install onnx onnxruntime onnxconverter-common numpy`
   (aarch64 wheels exist for these). Record the versions in the report.
2. Script `web/tools/inspect_model.py` (committed): for each of the four files in
   `web/model/onnx/` print input and output names, shapes, and a table of op types with counts and
   total initializer bytes per op type (which ops hold the weights: MatMul, Conv, Gemm, others).
   This decides what to quantize. Put the table in the report.

## Part 2: build variants

Script `web/tools/make_variants.py` (committed). Output to `web/model-q/<variant>/onnx/` with the
four files; copy `tts.json` and `unicode_indexer.json` unchanged; voices are not needed in the
variant folders (the bench reads them from `web/model/voice_styles/`).

| variant | what |
|---|---|
| `q-mm-ve` | `onnxruntime.quantization.quantize_dynamic`, `weight_type=QInt8`, `op_types_to_quantize=['MatMul']` on `vector_estimator` only. Others copied as fp32. |
| `q-mm-ve-te` | same, on `vector_estimator` and `text_encoder`. |
| `fp16` | all four with `onnxconverter_common.float16.convert_float_to_float16(model, keep_io_types=True)`. Mainly for WebGPU (half the memory). |
| `q-mm-ve-conv` | optional, only if Part 1 shows Conv holds most weights: also quantize Conv per channel and check whether the graph then contains `ConvInteger`; drop the variant if it does or if it does not load in Part 3. |

Rules: always run `onnx.checker.check_model` on the result and load it with onnxruntime (Python)
once. After building, list for each variant the op types in the graph that are new
(`MatMulInteger`, `DynamicQuantizeLinear`, `ConvInteger`, `Cast`, ...) and the file sizes. Anything
that fails to build or load is reported, not hidden.

## Part 3: benchmark in the same runtime as the browser

The browser uses ONNX Runtime Web 1.22.0 (`web/vendor/ort.wasm.min.mjs`). Benchmark with that, in
Node, not with Python onnxruntime, because the supported ops differ.

Script `web/tools/bench.mjs` (committed). Start from this working pattern (it was tested, it loads
the model and generates sk and cs sentences):

```js
import * as ort from '../vendor/ort.wasm.min.mjs';
import { TextToSpeech, UnicodeProcessor, setOrt, styleFromJson, writeWavFile } from '../js/supertonic.js';
setOrt(ort);
ort.env.wasm.wasmPaths = 'file://<abs path to web/vendor>/';
ort.env.wasm.numThreads = 1;   // also run with 4
// sessions: InferenceSession.create(new Uint8Array(readFileSync(path)), { executionProviders: ['wasm'], graphOptimizationLevel: 'all' })
// tts = new TextToSpeech(cfgs, new UnicodeProcessor(indexer), dp, textEnc, vectorEst, vocoder)
// const { wav, duration } = await tts.call(text, lang, style, steps, speed)
```

Facts: `ort.wasm.min.mjs` as an ES module works in Node; `supertonic.js` needs `setOrt(ort)` first.

- Variants to run: `original` (`web/model/onnx`) and every variant from Part 2.
- Sentences (sk): "Chcem pohár vody.", "Ahoj, ako sa máš?", "Ja chcem ponožky a topánky." and one long
  sentence of about 150 characters. (cs): "Chci sklenici vody.", "Ahoj, jak se máš?", "Chci ponožky a boty."
  and one long one.
- Settings: voice F1, then M1; steps 8 and 4; threads 1 and 4. Warm up once, then run each case 5
  times and report the median of wall time, the audio length, and the real-time factor.
- Make the runs deterministic: `sampleNoisyLatent` uses `Math.random`. Replace `Math.random` with a
  seeded generator (mulberry32) before each run so that all variants start from the same noise.
- The Pi is slower than a phone. Report relative speed (variant / original), that is what carries
  over, not the absolute seconds.

## Part 4: quality check

1. For every variant, voice and sentence, write a WAV with the seeded run into
   `web/model-q/samples/<variant>/<lang>-<voice>-<n>.wav` (git-ignored, so it is served at
   `http://192.168.0.190:8500/model-q/samples/...`). Make a small `web/model-q/samples/index.html` that
   lists them in a table (rows: sentence, columns: original and each variant, `<audio controls>` in
   each cell) so the owner can listen and compare side by side.
2. Objective checks per sample (put them in the report table): any NaN or Inf, peak level, fraction
   of near-silent samples, duration compared with the original (the duration predictor should be
   unchanged, a different duration means something broke), and a spectral distance to the original
   with the same seed (log-magnitude STFT L1, simple numpy or JS). These numbers do not replace
   listening, they only catch broken variants. State clearly which variants the owner should hear first.
3. Do not claim a variant "sounds good". Only the owner can judge that.

## Part 5: report and hand-over

Write `docs/quantize-results.md` (committed) with: versions, the inspection table, a table
`variant | size | steps | threads | median ms | speed vs original | broken? | spectral distance`,
what failed and why, and a recommendation (which one or two variants the owner should listen to,
and whether any is worth trying with WebGPU on the iPhone). Then tell the owner:

- where to listen: `http://192.168.0.190:8500/model-q/samples/` (LAN) or the https address with
  `/model-q/samples/`,
- that nothing is integrated in the app yet.

## Part 6: integration (only after the owner picked a variant)

Do not start before the owner says which variant sounds good enough.

- `web/js/model.js`: file list and sizes per variant (read the real sizes from the files).
- Setting "Model" (Original / the chosen small one) next to Engine in `web/js/app.js`; the
  download and the IndexedDB keys must include the variant name (`web/js/store.js`, `speaker.js`)
  so the two never mix. The page reloads when it changes, like Engine.
- `web/fetch_model.sh` stays for the original; the variants are produced by `make_variants.py`
  and served from `web/model-q/`.
- Log the variant in the worker load line so the owner's phone tests show it in the server log
  (`grep CLIENT <scratchpad>/serve.log`).
- Ask the owner to test on the iPhone: https address, Engine CPU and Engine GPU, then read the
  timings from the log (`speak "<text>" ... took Ns`) and compare with the numbers in
  "Why" above. Report faithfully: the phone result is what counts, the Pi numbers only predict it.
- Update `CLAUDE.md` (Web version section) and `.gitignore`.
