import Foundation
import OnnxRuntimeBindings

/// Supertonic 3 files. They are copied into the app from `Model/` (see `Scripts/fetch_model.sh`).
enum SupertonicModel {
    /// Preset voices: F1 to F5 women, M1 to M5 men. All work for every language.
    static let voices = ["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"]
    static let defaultVoice = "F1"

    static func voiceTitle(_ name: String) -> String {
        "\(name.hasPrefix("F") ? "Woman" : "Man") \(name.dropFirst())"
    }

    static var directory: URL {
        Bundle.main.resourceURL!.appending(path: "Model", directoryHint: .isDirectory)
    }
}

/// Owns the ONNX sessions. An actor so synthesis runs off the main thread, one sentence at a time.
actor SupertonicEngine {
    private let tts: TextToSpeech
    private let env: ORTEnv
    private var styles: [String: Style] = [:]

    init() throws {
        env = try ORTEnv(loggingLevel: .warning)
        tts = try loadTextToSpeech(SupertonicModel.directory.appending(path: "onnx").path, false, env)
    }

    /// WAV bytes for `text`. 8 denoising steps is upstream's default quality.
    func synthesize(_ text: String, language: AppLanguage, voice: String) throws -> Data {
        let style = try style(for: voice)
        let (wav, duration) = try tts.call(text, language.voiceCode, style, 8, speed: 1.0)
        let length = min(Int(Double(tts.sampleRate) * Double(duration)), wav.count)
        return try wavData(Array(wav[0..<length]), tts.sampleRate)
    }

    /// Voice files are small, so they are loaded the first time a voice is used.
    private func style(for voice: String) throws -> Style {
        if let style = styles[voice] { return style }
        let path = SupertonicModel.directory.appending(path: "voice_styles/\(voice).json").path
        let style = try loadVoiceStyle([path], verbose: false)
        styles[voice] = style
        return style
    }
}
