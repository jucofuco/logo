import Foundation
import OnnxRuntimeBindings

/// Supertonic 3 model files, downloaded once from Hugging Face into Application Support.
/// Pinned to the archived revision so the files never change under us.
enum SupertonicModel {
    static let revision = "aafc6e32416a594460b32413efc49d7fe4ce6d46"
    static let baseURL = URL(string: "https://huggingface.co/supertone-oss-archive/supertonic-3/resolve/\(revision)/")!
    static let voice = "F1"

    /// Path inside the repo and size in bytes (for the progress bar and the "already have it" check).
    static let files: [(path: String, size: Int64)] = [
        ("onnx/tts.json", 8_253),
        ("onnx/unicode_indexer.json", 277_676),
        ("onnx/duration_predictor.onnx", 3_700_147),
        ("onnx/text_encoder.onnx", 36_416_150),
        ("onnx/vocoder.onnx", 101_424_195),
        ("onnx/vector_estimator.onnx", 256_534_781),
        ("voice_styles/\(voice).json", 292_046),
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

    private static func downloadFile(_ url: URL, to dest: URL, received: @escaping @Sendable (Int64) -> Void) async throws {
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
            // Downloads are a few at most, polling the byte count is simpler than a session delegate.
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
    private let style: Style
    private let env: ORTEnv

    init() throws {
        env = try ORTEnv(loggingLevel: .warning)
        tts = try loadTextToSpeech(SupertonicModel.localURL("onnx").path, false, env)
        style = try loadVoiceStyle([SupertonicModel.localURL("voice_styles/\(SupertonicModel.voice).json").path], verbose: false)
    }

    /// WAV bytes for `text`. 8 denoising steps is upstream's default quality.
    func synthesize(_ text: String, lang: String = "sk") throws -> Data {
        let (wav, duration) = try tts.call(text, lang, style, 8, speed: 1.0)
        let length = min(Int(Double(tts.sampleRate) * Double(duration)), wav.count)
        return try wavData(Array(wav[0..<length]), tts.sampleRate)
    }
}
