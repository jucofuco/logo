import Foundation
import OnnxRuntimeBindings

/// Supertonic 3 files, downloaded once from Hugging Face into Application Support.
/// Pinned to the archived revision so the files never change under us.
enum SupertonicModel {
    static let revision = "aafc6e32416a594460b32413efc49d7fe4ce6d46"
    static let baseURL = URL(string: "https://huggingface.co/supertone-oss-archive/supertonic-3/resolve/\(revision)/")!

    /// Preset voices: F1 to F5 women, M1 to M5 men. All work for every language.
    static let voices = ["F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"]
    static let defaultVoice = "F1"

    static func voiceTitle(_ name: String) -> String {
        "\(name.hasPrefix("F") ? "Woman" : "Man") \(name.dropFirst())"
    }

    /// Path inside the repo and size in bytes (for the progress bar and the "already have it" check).
    static let files: [(path: String, size: Int64)] = [
        ("onnx/tts.json", 8_253),
        ("onnx/unicode_indexer.json", 277_676),
        ("onnx/duration_predictor.onnx", 3_700_147),
        ("onnx/text_encoder.onnx", 36_416_150),
        ("onnx/vocoder.onnx", 101_424_195),
        ("onnx/vector_estimator.onnx", 256_534_781),
        ("voice_styles/F1.json", 292_046),
        ("voice_styles/F2.json", 292_423),
        ("voice_styles/F3.json", 290_794),
        ("voice_styles/F4.json", 291_808),
        ("voice_styles/F5.json", 291_479),
        ("voice_styles/M1.json", 291_748),
        ("voice_styles/M2.json", 292_055),
        ("voice_styles/M3.json", 290_198),
        ("voice_styles/M4.json", 291_522),
        ("voice_styles/M5.json", 291_469),
    ]

    static var totalSize: Int64 { files.reduce(0) { $0 + $1.size } }

    static var directory: URL {
        URL.applicationSupportDirectory.appending(path: "supertonic-\(revision.prefix(8))", directoryHint: .isDirectory)
    }

    static func localURL(_ path: String) -> URL { directory.appending(path: path) }

    static func isPresent(_ file: (path: String, size: Int64)) -> Bool {
        let attrs = try? FileManager.default.attributesOfItem(atPath: localURL(file.path).path)
        return (attrs?[.size] as? Int64) == file.size
    }

    static var isDownloaded: Bool { files.allSatisfy(isPresent) }

    /// Downloads the missing files one by one. Finished files stay, so a retry continues.
    static func download(progress: @escaping @Sendable (Double) -> Void) async throws {
        let fm = FileManager.default
        var done: Int64 = files.filter(isPresent).reduce(0) { $0 + $1.size }
        progress(Double(done) / Double(totalSize))

        for file in files where !isPresent(file) {
            let dest = localURL(file.path)
            try fm.createDirectory(at: dest.deletingLastPathComponent(), withIntermediateDirectories: true)
            let base = done
            try await downloadFile(baseURL.appending(path: file.path), to: dest) { received in
                progress(Double(base + received) / Double(totalSize))
            }
            done += file.size
        }

        var dir = directory
        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        try? dir.setResourceValues(values)
    }

    static func downloadFile(_ url: URL, to dest: URL, received: @escaping @Sendable (Int64) -> Void) async throws {
        try await withCheckedThrowingContinuation { (cont: CheckedContinuation<Void, Error>) in
            let task = URLSession.shared.downloadTask(with: url) { tmp, response, error in
                if let error { return cont.resume(throwing: error) }
                guard let tmp, (response as? HTTPURLResponse)?.statusCode == 200 else {
                    return cont.resume(throwing: URLError(.badServerResponse))
                }
                do {
                    try? FileManager.default.removeItem(at: dest)
                    try FileManager.default.moveItem(at: tmp, to: dest)
                    cont.resume()
                } catch {
                    cont.resume(throwing: error)
                }
            }
            task.resume()
            // Polling the byte count is simpler than a session delegate.
            Task {
                while task.state == .running {
                    received(task.countOfBytesReceived)
                    try? await Task.sleep(for: .milliseconds(200))
                }
            }
        }
    }
}

/// Owns the ONNX sessions. An actor so synthesis runs off the main thread, one sentence at a time.
actor SupertonicEngine {
    private let tts: TextToSpeech
    private let env: ORTEnv
    private var styles: [String: Style] = [:]

    init() throws {
        env = try ORTEnv(loggingLevel: .warning)
        tts = try loadTextToSpeech(SupertonicModel.localURL("onnx").path, false, env)
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
        let style = try loadVoiceStyle([SupertonicModel.localURL("voice_styles/\(voice).json").path], verbose: false)
        styles[voice] = style
        return style
    }
}
