// Supertonic 3 files served from web/model/ (see fetch_model.sh). Path and size in bytes.
export const FILES = [
    { path: 'onnx/tts.json', size: 8253 },
    { path: 'onnx/unicode_indexer.json', size: 277676 },
    { path: 'onnx/duration_predictor.onnx', size: 3700147 },
    { path: 'onnx/text_encoder.onnx', size: 36416150 },
    { path: 'onnx/vocoder.onnx', size: 101424195 },
    { path: 'onnx/vector_estimator.onnx', size: 256534781 },
    { path: 'voice_styles/F1.json', size: 292046 },
    { path: 'voice_styles/F2.json', size: 292423 },
    { path: 'voice_styles/F3.json', size: 290794 },
    { path: 'voice_styles/F4.json', size: 291808 },
    { path: 'voice_styles/F5.json', size: 291479 },
    { path: 'voice_styles/M1.json', size: 291748 },
    { path: 'voice_styles/M2.json', size: 292055 },
    { path: 'voice_styles/M3.json', size: 290198 },
    { path: 'voice_styles/M4.json', size: 291522 },
    { path: 'voice_styles/M5.json', size: 291469 },
];

export const totalSize = FILES.reduce((sum, f) => sum + f.size, 0);

/** Preset voices: F1 to F5 women, M1 to M5 men. All work for every language. */
export const VOICES = ['F1', 'F2', 'F3', 'F4', 'F5', 'M1', 'M2', 'M3', 'M4', 'M5'];

export function voiceTitle(name) {
    return `${name.startsWith('F') ? 'Woman' : 'Man'} ${name.slice(1)}`;
}
