// Runs Supertonic in a worker so the page does not freeze while a sentence is generated.
import { TextToSpeech, UnicodeProcessor, setOrt, styleFromJson, writeWavFile } from './supertonic.js';
import * as store from './store.js';
import { log } from './log.js';
import { SIZES, VOICES } from './model.js';

const decoder = new TextDecoder();
const styles = new Map();
let tts = null;
let ort = null;

/** A file handed over by the page (when IndexedDB could not keep it) or the stored one. */
async function readFile(path, provided) {
    const buffer = provided?.[path] ?? (await store.get(path, SIZES[path]));
    if (!buffer) throw new Error(`Missing ${path}`);
    return buffer;
}

async function load({ vendorURL, files, engine }) {
    // GPU needs WebGPU, which only exists on https pages. Without it the CPU build is used.
    const useGpu = engine === 'gpu' && 'gpu' in navigator;
    ort = await import(useGpu ? '../vendor/ort.min.mjs' : '../vendor/ort.wasm.min.mjs');
    setOrt(ort);
    ort.env.wasm.wasmPaths = vendorURL;
    // More than one thread needs a cross-origin isolated page (https plus headers).
    ort.env.wasm.numThreads = self.crossOriginIsolated ? Math.min(4, navigator.hardwareConcurrency || 1) : 1;
    log('worker load', 'engine', useGpu ? 'gpu' : 'cpu', '(asked', engine + ')', 'threads', ort.env.wasm.numThreads,
        'cores', navigator.hardwareConcurrency, 'isolated', self.crossOriginIsolated, 'files from page:', Object.keys(files ?? {}).length);

    const cfgs = JSON.parse(decoder.decode(await readFile('onnx/tts.json', files)));
    const indexer = JSON.parse(decoder.decode(await readFile('onnx/unicode_indexer.json', files)));

    // One at a time, so only one big file is in memory at once.
    const sessions = [];
    for (const name of ['duration_predictor', 'text_encoder', 'vector_estimator', 'vocoder']) {
        const path = `onnx/${name}.onnx`;
        const buffer = await readFile(path, files);
        log('worker creating session', name, buffer.byteLength);
        sessions.push(await ort.InferenceSession.create(new Uint8Array(buffer), {
            executionProviders: useGpu ? ['webgpu', 'wasm'] : ['wasm'],
            graphOptimizationLevel: 'all',
        }));
        if (files) delete files[path];
    }
    tts = new TextToSpeech(cfgs, new UnicodeProcessor(indexer), ...sessions);

    // All voices now, so speaking never has to read storage again.
    for (const voice of VOICES) {
        try {
            const json = JSON.parse(decoder.decode(await readFile(`voice_styles/${voice}.json`, files)));
            styles.set(voice, styleFromJson(json));
        } catch (error) {
            log('voice not loaded', voice, error);
        }
    }
    if (!styles.has('F1')) throw new Error('Voice files could not be read');
    log('worker loaded', [...styles.keys()]);
}

function style(voice) {
    return styles.get(voice) ?? styles.get('F1');
}

async function speak({ text, lang, voice, speed, steps }) {
    const started = performance.now();
    const { wav, duration } = await tts.call(text, lang, style(voice), steps, speed);
    const length = Math.min(Math.floor(tts.sampleRate * duration[0]), wav.length);
    const took = (performance.now() - started) / 1000;
    log('speak', `"${text}"`, lang, 'steps', steps, 'audio', duration[0].toFixed(2) + 's', 'took', took.toFixed(1) + 's');
    return writeWavFile(wav.slice(0, length), tts.sampleRate);
}

self.onmessage = async ({ data }) => {
    const { id, type } = data;
    try {
        if (type === 'load') {
            await load(data);
            self.postMessage({ id, ok: true });
        } else if (type === 'speak') {
            const wav = await speak(data);
            self.postMessage({ id, ok: true, wav }, [wav]);
        }
    } catch (error) {
        self.postMessage({ id, ok: false, error: String(error?.message ?? error) });
    }
};
