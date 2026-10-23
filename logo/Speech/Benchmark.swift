import AVFoundation
import Foundation
import Observation
import OnnxRuntimeBindings

struct BenchmarkFile: Sendable {
    let name: String
    let size: Int64
}

/// A model the speed test can load. "original" is the voice download; the others are built by
/// `speech/make_variants.py` and downloaded from the server typed into the test screen.
struct BenchmarkVariant: Identifiable, Sendable {
    let id: String
    let title: String
    let note: String
    /// The four ONNX files and their size in bytes. Empty for the original.
    let files: [BenchmarkFile]

    var totalSize: Int64 { files.reduce(0) { $0 + $1.size } }

    var directory: URL {
        id == "original"
            ? SupertonicModel.localURL("onnx")
            : URL.applicationSupportDirectory.appending(path: "benchmark/\(id)", directoryHint: .isDirectory)
    }

    func isPresent(_ file: BenchmarkFile) -> Bool {
        let attrs = try? FileManager.default.attributesOfItem(atPath: directory.appending(path: file.name).path)
        return (attrs?[.size] as? Int64) == file.size
    }

    var isDownloaded: Bool {
        id == "original" ? SupertonicModel.isDownloaded : files.allSatisfy(isPresent)
    }
}

enum BenchmarkCatalog {
    static let original = BenchmarkVariant(
        id: "original", title: "Original", note: "fp32, from the voice download", files: [])

    static let variants: [BenchmarkVariant] = [
        BenchmarkVariant(
            id: "q-mm-ve-conv", title: "int8 convolutions",
            note: "Main model with int8 convolutions. The browser cannot run it, this phone may.",
            files: [
                BenchmarkFile(name: "duration_predictor.onnx", size: 3_700_147),
                BenchmarkFile(name: "text_encoder.onnx", size: 36_416_150),
                BenchmarkFile(name: "vector_estimator.onnx", size: 65_439_352),
                BenchmarkFile(name: "vocoder.onnx", size: 101_424_195),
            ]),
        BenchmarkVariant(
            id: "fp16", title: "fp16",
            note: "Half the size, half precision numbers.",
            files: [
                BenchmarkFile(name: "duration_predictor.onnx", size: 2_059_197),
                BenchmarkFile(name: "text_encoder.onnx", size: 18_578_974),
                BenchmarkFile(name: "vector_estimator.onnx", size: 128_517_269),
                BenchmarkFile(name: "vocoder.onnx", size: 50_773_459),
            ]),
        BenchmarkVariant(
            id: "w8", title: "int8 weights",
            note: "Smallest file, the math stays fp32.",
            files: [
                BenchmarkFile(name: "duration_predictor.onnx", size: 2_832_229),
                BenchmarkFile(name: "text_encoder.onnx", size: 16_084_638),
                BenchmarkFile(name: "vector_estimator.onnx", size: 65_867_648),
                BenchmarkFile(name: "vocoder.onnx", size: 25_820_925),
            ]),
    ]

    static var all: [BenchmarkVariant] { [original] + variants }
}

struct StepTiming: Sendable {
    let steps: Int
    /// Median milliseconds per sentence, in the order of `BenchmarkWork.sentences`.
    let medianMs: [Double]
    /// Median of (time / length of the audio).
    let rtf: Double
}

struct BenchmarkResult: Identifiable, Sendable {
    let id = UUID()
    let variant: BenchmarkVariant
    let loadSeconds: Double
    let timings: [StepTiming]
    /// The first sentence as a WAV, so the owner can hear what this variant sounds like.
    let sample: Data?
    let error: String?
}

/// The measuring itself. Plain functions so it runs off the main thread.
enum BenchmarkWork {
    static let sentences = [
        "Chcem pohár vody.",
        "Ahoj, ako sa máš?",
        "Včera večer sme s babkou upiekli jablkový koláč, a keď bol hotový, celá kuchyňa voňala škoricou a všetci sme sa tešili na večeru.",
    ]

    static func measure(
        _ variant: BenchmarkVariant, steps: [Int], threads: Int, runs: Int,
        report: @Sendable (String) -> Void
    ) -> BenchmarkResult {
        do {
            report("\(variant.title): loading")
            let env = try ORTEnv(loggingLevel: .warning)
            let started = Date()
            let tts = try loadTextToSpeech(variant.directory.path, false, env, threads)
            let loadSeconds = Date().timeIntervalSince(started)
            let style = try loadVoiceStyle(
                [SupertonicModel.localURL("voice_styles/\(SupertonicModel.defaultVoice).json").path], verbose: false)

            let top = steps.max() ?? 8
            report("\(variant.title): warm-up")
            _ = try tts.call(sentences[0], "sk", style, top, speed: 1.0)

            var timings: [StepTiming] = []
            var sample: Data?
            for step in steps {
                var medians: [Double] = []
                var rtfs: [Double] = []
                for (index, sentence) in sentences.enumerated() {
                    report("\(variant.title): \(step) steps, sentence \(index + 1) of \(sentences.count)")
                    var times: [Double] = []
                    var last: (wav: [Float], duration: Float)?
                    for _ in 0..<runs {
                        let begin = Date()
                        last = try tts.call(sentence, "sk", style, step, speed: 1.0)
                        times.append(Date().timeIntervalSince(begin) * 1000)
                    }
                    let ms = median(times)
                    medians.append(ms)
                    if let last {
                        rtfs.append(ms / 1000 / Double(last.duration))
                        if step == top, index == 0 {
                            let length = min(Int(Double(tts.sampleRate) * Double(last.duration)), last.wav.count)
                            sample = try? wavData(Array(last.wav[0..<length]), tts.sampleRate)
                        }
                    }
                }
                timings.append(StepTiming(steps: step, medianMs: medians, rtf: median(rtfs)))
            }
            return BenchmarkResult(variant: variant, loadSeconds: loadSeconds, timings: timings, sample: sample, error: nil)
        } catch {
            return BenchmarkResult(
                variant: variant, loadSeconds: 0, timings: [], sample: nil, error: error.localizedDescription)
        }
    }

    private static func median(_ values: [Double]) -> Double {
        let sorted = values.sorted()
        guard !sorted.isEmpty else { return 0 }
        let middle = sorted.count / 2
        return sorted.count % 2 == 1 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2
    }
}

/// State of the speed test screen: downloads of the variants, the run, and its results.
@MainActor
@Observable
final class BenchmarkRunner {
    /// Download progress (0 to 1) of the variants that are downloading right now.
    private(set) var progress: [String: Double] = [:]
    private(set) var status = ""
    private(set) var isRunning = false
    private(set) var results: [BenchmarkResult] = []
    private(set) var error: String?
    private(set) var optionsText = ""

    private var player: AVAudioPlayer?

    func download(_ variant: BenchmarkVariant, base: String) {
        guard progress[variant.id] == nil else { return }
        progress[variant.id] = 0
        error = nil
        Task {
            do {
                let fm = FileManager.default
                try fm.createDirectory(at: variant.directory, withIntermediateDirectories: true)
                let total = variant.totalSize
                var done: Int64 = 0
                for file in variant.files {
                    let dest = variant.directory.appending(path: file.name)
                    if !variant.isPresent(file) {
                        guard let url = URL(string: base)?
                            .appending(path: variant.id).appending(path: "onnx").appending(path: file.name)
                        else { throw URLError(.badURL) }
                        let finished = done
                        try await SupertonicModel.downloadFile(url, to: dest) { received in
                            Task { @MainActor [weak self] in
                                self?.progress[variant.id] = Double(finished + received) / Double(total)
                            }
                        }
                        if !variant.isPresent(file) {
                            try? fm.removeItem(at: dest)
                            throw URLError(.cannotParseResponse)
                        }
                    }
                    done += file.size
                }
                // The small config files are the same for every variant.
                for name in ["tts.json", "unicode_indexer.json"] {
                    let dest = variant.directory.appending(path: name)
                    if !fm.fileExists(atPath: dest.path) {
                        try fm.copyItem(at: SupertonicModel.localURL("onnx/\(name)"), to: dest)
                    }
                }
                progress[variant.id] = nil
            } catch {
                progress[variant.id] = nil
                self.error = "Download of \(variant.title) failed: \(error.localizedDescription)"
            }
        }
    }

    func remove(_ variant: BenchmarkVariant) {
        guard variant.id != "original" else { return }
        try? FileManager.default.removeItem(at: variant.directory)
        // Touch the state so the screen refreshes.
        progress[variant.id] = nil
    }

    func run(_ variants: [BenchmarkVariant], steps: [Int], threads: Int, runs: Int) {
        guard !isRunning, !variants.isEmpty else { return }
        isRunning = true
        results = []
        error = nil
        let cores = ProcessInfo.processInfo.activeProcessorCount
        optionsText = "\(cores) cores, threads \(threads == 0 ? "default" : String(threads)), "
            + "\(runs) run\(runs == 1 ? "" : "s") per sentence, voice \(SupertonicModel.defaultVoice)"
        Task.detached(priority: .userInitiated) {
            for variant in variants {
                let result = BenchmarkWork.measure(variant, steps: steps, threads: threads, runs: runs) { text in
                    Task { @MainActor in self.status = text }
                }
                await MainActor.run { self.results.append(result) }
            }
            await MainActor.run {
                self.status = "Done"
                self.isRunning = false
            }
        }
    }

    func play(_ result: BenchmarkResult) {
        guard let sample = result.sample else { return }
        try? AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio)
        try? AVAudioSession.sharedInstance().setActive(true)
        player = try? AVAudioPlayer(data: sample)
        player?.play()
    }

    /// Plain text of all results, to paste into a message.
    var reportText: String {
        var lines = ["Speed test, \(optionsText)"]
        let original = results.first { $0.variant.id == "original" }
        for result in results {
            if let error = result.error {
                lines.append("\(result.variant.title): FAILED \(error)")
                continue
            }
            lines.append("\(result.variant.title): load \(String(format: "%.1f", result.loadSeconds)) s")
            for timing in result.timings {
                let ms = timing.medianMs.map { String(format: "%.0f", $0) }.joined(separator: ", ")
                var line = "  \(timing.steps) steps: rtf \(String(format: "%.2f", timing.rtf)), ms per sentence [\(ms)]"
                if result.variant.id != "original",
                   let reference = original?.timings.first(where: { $0.steps == timing.steps }), timing.rtf > 0 {
                    line += ", \(String(format: "%.2f", reference.rtf / timing.rtf))x vs original"
                }
                lines.append(line)
            }
        }
        return lines.joined(separator: "\n")
    }
}
