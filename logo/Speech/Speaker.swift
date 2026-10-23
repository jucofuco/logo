import AVFoundation
import Observation

/// Speaks words and sentences. Uses Supertonic once its model is downloaded and loaded,
/// the built-in iOS voice for the language until then or if anything fails.
@MainActor
@Observable
final class Speaker {
    enum ModelState: Equatable {
        case missing
        case downloading(Double)
        case loading
        case ready
        case failed(String)
    }

    private(set) var modelState: ModelState = .missing
    /// True while a Supertonic sentence is being generated, for a small spinner.
    private(set) var isThinking = false

    private var engine: SupertonicEngine?
    private var player: AVAudioPlayer?
    private let system = AVSpeechSynthesizer()
    /// Generated audio per language, voice and text, so tapping the same card again is instant.
    private var cache: [String: Data] = [:]
    /// Latest request wins: a tap while an older one is still generating drops the older one.
    private var request = 0

    init() {
        // .playback so the kid hears it even with the silent switch on.
        try? AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio)
        if SupertonicModel.isDownloaded { loadEngine() }
    }

    func downloadModel() {
        if case .downloading = modelState { return }
        modelState = .downloading(0)
        Task {
            do {
                try await SupertonicModel.download { fraction in
                    Task { @MainActor [weak self] in
                        if case .downloading = self?.modelState { self?.modelState = .downloading(fraction) }
                    }
                }
                loadEngine()
            } catch {
                modelState = .failed("Download failed. Check the connection and try again.")
            }
        }
    }

    private func loadEngine() {
        modelState = .loading
        Task.detached(priority: .userInitiated) {
            do {
                let engine = try SupertonicEngine()
                await MainActor.run {
                    self.engine = engine
                    self.modelState = .ready
                }
            } catch {
                await MainActor.run { self.modelState = .failed("Voice could not load.") }
            }
        }
    }

    func speak(_ text: String, language: AppLanguage, voice: String) {
        let text = text.trimmingCharacters(in: .whitespaces)
        guard !text.isEmpty else { return }
        stop()
        request += 1
        let id = request

        guard let engine else { return speakWithSystem(text, language: language) }
        let key = "\(language.rawValue)|\(voice)|\(text)"
        if let data = cache[key] { return play(data) }

        isThinking = true
        Task {
            let data = try? await engine.synthesize(text, language: language, voice: voice)
            guard id == request else { return }
            isThinking = false
            if let data {
                cache[key] = data
                play(data)
            } else {
                speakWithSystem(text, language: language)
            }
        }
    }

    func stop() {
        player?.stop()
        system.stopSpeaking(at: .immediate)
        isThinking = false
    }

    private func play(_ data: Data) {
        try? AVAudioSession.sharedInstance().setActive(true)
        player = try? AVAudioPlayer(data: data)
        player?.play()
    }

    private func speakWithSystem(_ text: String, language: AppLanguage) {
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: language.systemVoice)
        utterance.rate = 0.45
        system.speak(utterance)
    }
}
