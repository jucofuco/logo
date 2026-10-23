#!/bin/sh
# Downloads the Supertonic 3 model and the 10 preset voices into Model/ (git-ignored).
# project.yml copies that folder into the app. Run once before the first build, safe to rerun.
set -eu
cd "$(dirname "$0")/.."

# Pinned revision of supertone-oss-archive/supertonic-3, so the files never change.
BASE=https://huggingface.co/supertone-oss-archive/supertonic-3/resolve/aafc6e32416a594460b32413efc49d7fe4ce6d46

fetch() { # path size-in-bytes
  dest="Model/$1"
  if [ -f "$dest" ] && [ "$(wc -c < "$dest" | tr -d ' ')" = "$2" ]; then
    echo "have $1"
    return
  fi
  echo "download $1"
  mkdir -p "$(dirname "$dest")"
  curl -fL --retry 3 -o "$dest.part" "$BASE/$1"
  if [ "$(wc -c < "$dest.part" | tr -d ' ')" != "$2" ]; then
    echo "wrong size for $1, expected $2 bytes" >&2
    rm -f "$dest.part"
    exit 1
  fi
  mv "$dest.part" "$dest"
}

fetch onnx/tts.json 8253
fetch onnx/unicode_indexer.json 277676
fetch onnx/duration_predictor.onnx 3700147
fetch onnx/text_encoder.onnx 36416150
fetch onnx/vocoder.onnx 101424195
fetch onnx/vector_estimator.onnx 256534781
fetch voice_styles/F1.json 292046
fetch voice_styles/F2.json 292423
fetch voice_styles/F3.json 290794
fetch voice_styles/F4.json 291808
fetch voice_styles/F5.json 291479
fetch voice_styles/M1.json 291748
fetch voice_styles/M2.json 292055
fetch voice_styles/M3.json 290198
fetch voice_styles/M4.json 291522
fetch voice_styles/M5.json 291469
echo "Model ready in Model/"
