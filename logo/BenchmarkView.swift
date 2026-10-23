import SwiftUI

/// Measures how long a sentence takes on this phone, for each model variant, and lets the owner
/// hear every variant. Reached from Settings.
struct BenchmarkView: View {
    @State private var runner = BenchmarkRunner()
    @State private var selected: Set<String> = ["original", "q-mm-ve-conv"]
    @State private var steps = 8
    @State private var threads = 0
    @State private var runs = 1
    @AppStorage("benchBase") private var base = "https://rpi-dev.tail2bb2c8.ts.net:8443/model-q"

    private var chosen: [BenchmarkVariant] {
        BenchmarkCatalog.all.filter { selected.contains($0.id) && $0.isDownloaded }
    }

    var body: some View {
        Form {
            Section {
                Text("Measures how long Slovak sentences take on this phone. The original comes from the voice download, the other models from the server below.")
                    .font(.footnote)
                    .foregroundStyle(Theme.muted)
            }

            Section("Server") {
                TextField("https://...", text: $base)
                    .textInputAutocapitalization(.never)
                    .autocorrectionDisabled()
                    .keyboardType(.URL)
            }

            Section {
                ForEach(BenchmarkCatalog.all) { variant in
                    row(variant)
                }
                if let error = runner.error {
                    Text(error).font(.footnote).foregroundStyle(.red)
                }
            } header: {
                Text("Models")
            } footer: {
                Text("Download a model first (the server above must be reachable, Tailscale on), then tick it to include it in the test.")
            }

            Section("Options") {
                Picker("Steps", selection: $steps) {
                    Text("8").tag(8)
                    Text("4").tag(4)
                    Text("4 and 8").tag(0)
                }
                Picker("Threads", selection: $threads) {
                    Text("Default").tag(0)
                    Text("1").tag(1)
                    Text("2").tag(2)
                    Text("4").tag(4)
                    Text("6").tag(6)
                }
                Picker("Runs per sentence", selection: $runs) {
                    Text("1").tag(1)
                    Text("3").tag(3)
                }
            }

            Section {
                Button {
                    runner.run(chosen, steps: steps == 0 ? [4, 8] : [steps], threads: threads, runs: runs)
                } label: {
                    HStack {
                        Text(runner.isRunning ? "Running" : "Run speed test")
                        Spacer()
                        if runner.isRunning { ProgressView() }
                    }
                }
                .disabled(runner.isRunning || chosen.isEmpty)
                if !runner.status.isEmpty {
                    Text(runner.status).font(.footnote).foregroundStyle(Theme.muted)
                }
                if let error = runner.error {
                    Text(error).font(.footnote).foregroundStyle(.red)
                }
            } footer: {
                Text("Keep the screen on and the phone cool. The first sentence of each model is a warm-up and is not counted.")
            }

            if !runner.results.isEmpty {
                Section("Results") {
                    ForEach(runner.results) { result in
                        resultRow(result)
                    }
                    Button("Copy results") { UIPasteboard.general.string = runner.reportText }
                }
            }
        }
        .navigationTitle("Speed test")
        .navigationBarTitleDisplayMode(.inline)
    }

    // MARK: Models

    private func row(_ variant: BenchmarkVariant) -> some View {
        let downloaded = variant.isDownloaded
        return HStack(spacing: 12) {
            leading(variant, downloaded: downloaded)

            VStack(alignment: .leading, spacing: 2) {
                Text(variant.title).foregroundStyle(Theme.text)
                Text(variant.note).font(.caption).foregroundStyle(Theme.muted)
            }
            Spacer()
            trailing(variant, downloaded: downloaded)
        }
    }

    /// Tick box once the model is on the phone, download button before that.
    @ViewBuilder
    private func leading(_ variant: BenchmarkVariant, downloaded: Bool) -> some View {
        if runner.progress[variant.id] != nil {
            ProgressView()
        } else if downloaded {
            Button {
                if selected.contains(variant.id) { selected.remove(variant.id) } else { selected.insert(variant.id) }
            } label: {
                Image(systemName: selected.contains(variant.id) ? "checkmark.circle.fill" : "circle")
                    .font(.system(size: 22))
                    .foregroundStyle(Theme.accent)
            }
            .buttonStyle(.borderless)
        } else if variant.id == "original" {
            Image(systemName: "exclamationmark.circle").font(.system(size: 22)).foregroundStyle(Theme.faint)
        } else {
            Button {
                runner.download(variant, base: base)
            } label: {
                Image(systemName: "arrow.down.circle.fill").font(.system(size: 22)).foregroundStyle(Theme.accent)
            }
            .buttonStyle(.borderless)
        }
    }

    @ViewBuilder
    private func trailing(_ variant: BenchmarkVariant, downloaded: Bool) -> some View {
        if let fraction = runner.progress[variant.id] {
            ProgressView(value: fraction).frame(width: 70)
        } else if variant.id == "original" {
            if !downloaded { Text("Download the voice first").font(.caption).foregroundStyle(Theme.muted) }
        } else if downloaded {
            Button("Delete", role: .destructive) {
                selected.remove(variant.id)
                runner.remove(variant)
            }
            .buttonStyle(.borderless)
            .font(.caption)
        } else {
            Button("Download \(variant.totalSize / 1_000_000) MB") {
                runner.download(variant, base: base)
            }
            .buttonStyle(.borderedProminent)
            .font(.caption)
        }
    }

    // MARK: Results

    private func resultRow(_ result: BenchmarkResult) -> some View {
        let original = runner.results.first { $0.variant.id == "original" }
        return VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(result.variant.title).font(.headline)
                Spacer()
                if result.sample != nil {
                    Button { runner.play(result) } label: { Label("Listen", systemImage: "play.fill") }
                        .buttonStyle(.borderless)
                        .font(.caption)
                }
            }
            if let error = result.error {
                Text(error).font(.footnote).foregroundStyle(.red)
            } else {
                Text("Load \(String(format: "%.1f", result.loadSeconds)) s")
                    .font(.caption).foregroundStyle(Theme.muted)
                ForEach(result.timings, id: \.steps) { timing in
                    VStack(alignment: .leading, spacing: 2) {
                        Text("\(timing.steps) steps: rtf \(String(format: "%.2f", timing.rtf))")
                            + Text(speedup(result, timing, original))
                        Text(timing.medianMs.map { String(format: "%.0f ms", $0) }.joined(separator: ", "))
                            .font(.caption).foregroundStyle(Theme.muted)
                    }
                }
            }
        }
    }

    private func speedup(_ result: BenchmarkResult, _ timing: StepTiming, _ original: BenchmarkResult?) -> String {
        guard result.variant.id != "original", timing.rtf > 0,
              let reference = original?.timings.first(where: { $0.steps == timing.steps }) else { return "" }
        return "  (\(String(format: "%.2f", reference.rtf / timing.rtf))x vs original)"
    }
}
