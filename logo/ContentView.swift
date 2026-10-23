import SwiftUI

/// The one screen: sentence strip on top, below it the main page (core words + folders) or an
/// opened folder. Tapping a card says the word and adds it, the big button reads the sentence.
struct ContentView: View {
    @State private var speaker = Speaker()
    @State private var openFolderID: String?
    @State private var sentence: [SentenceItem] = []
    @State private var showSettings = false

    @AppStorage("language") private var language = AppLanguage.sk
    @AppStorage("childGender") private var child = ChildGender.boy
    @AppStorage("grammar") private var grammar = true
    @AppStorage("voice") private var voice = SupertonicModel.defaultVoice

    private var words: [String: WordEntry] { Vocabulary.words(for: language) }

    private var rendered: [String] {
        Grammar.render(sentence, words: words, child: child, enabled: grammar)
    }

    private var openFolder: Folder? {
        Vocabulary.folders.first { $0.id == openFolderID }
    }

    private var sentenceText: String {
        let text = rendered.joined(separator: " ")
        return text.prefix(1).uppercased() + text.dropFirst()
    }

    var body: some View {
        VStack(spacing: 14) {
            sentenceStrip
            speakButton
            Group {
                if let folder = openFolder {
                    folderPage(folder).transition(.move(edge: .trailing))
                } else {
                    mainPage.transition(.move(edge: .leading))
                }
            }
            .frame(maxHeight: .infinity, alignment: .top)
            ModelBanner(speaker: speaker)
        }
        .padding(.horizontal, 16)
        .padding(.top, 8)
        .background(Theme.background.ignoresSafeArea())
        .sheet(isPresented: $showSettings) { SettingsView(speaker: speaker) }
        .onChange(of: language) {
            // Hand-picked forms are text in the old language.
            for index in sentence.indices { sentence[index].override = nil }
            speaker.stop()
        }
    }

    // MARK: Sentence

    private var sentenceStrip: some View {
        HStack(spacing: 8) {
            ScrollViewReader { proxy in
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 6) {
                        if sentence.isEmpty {
                            Text("Tap a picture")
                                .font(.display(17, weight: .semibold))
                                .foregroundStyle(Theme.faint)
                                .padding(.leading, 6)
                        }
                        ForEach(Array(sentence.enumerated()), id: \.offset) { index, item in
                            chip(item, index: index)
                                .id(index)
                        }
                    }
                    .frame(minHeight: 64)
                }
                .onChange(of: sentence.count) { _, count in
                    withAnimation { proxy.scrollTo(count - 1, anchor: .trailing) }
                }
            }

            Button {
                if !sentence.isEmpty { sentence.removeLast() }
            } label: {
                Image(systemName: "delete.left.fill")
                    .font(.system(size: 22))
                    .frame(width: 44, height: 44)
            }
            .disabled(sentence.isEmpty)
            .accessibilityLabel("Delete last")
        }
        .card(padding: 10)
        .contextMenu {
            Button("Clear", systemImage: "trash", role: .destructive) { sentence.removeAll() }
        }
    }

    /// A word in the sentence. Tap removes it, long press picks another form of it.
    private func chip(_ item: SentenceItem, index: Int) -> some View {
        let text = rendered.indices.contains(index) ? rendered[index] : item.wordID
        return Button { sentence.remove(at: index) } label: {
            VStack(spacing: 2) {
                Text(Vocabulary.picture(of: item.wordID))
                    .font(.display(30, weight: .heavy))
                    .foregroundStyle(Theme.text)
                Text(text)
                    .font(.display(12, weight: .semibold))
                    .foregroundStyle(Theme.text)
                    .lineLimit(1)
            }
            .padding(.horizontal, 8)
            .frame(minWidth: 56, minHeight: 64)
            .background(Theme.raised, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        }
        .buttonStyle(.plain)
        .contextMenu {
            if grammar {
                Button("Automatic") { sentence[index].override = nil }
                ForEach(Grammar.forms(of: words[item.wordID]), id: \.self) { form in
                    Button(form) { sentence[index].override = form }
                }
            }
        }
    }

    private var speakButton: some View {
        Button {
            speaker.speak(sentenceText, language: language, voice: voice)
        } label: {
            HStack(spacing: 10) {
                if speaker.isThinking {
                    ProgressView().tint(Theme.onAccent)
                } else {
                    Image(systemName: "speaker.wave.2.fill")
                }
                Text("Speak")
            }
            .font(.display(22, weight: .heavy))
            .foregroundStyle(Theme.onAccent)
            .frame(maxWidth: .infinity, minHeight: 60)
            .background(Theme.accent, in: RoundedRectangle(cornerRadius: 20, style: .continuous))
            .opacity(sentence.isEmpty ? 0.4 : 1)
        }
        .buttonStyle(.plain)
        .disabled(sentence.isEmpty)
    }

    // MARK: Cards

    /// Main screen: settings button, core words, then the folders.
    private var mainPage: some View {
        ScrollView {
            VStack(spacing: 14) {
                HStack {
                    Spacer()
                    Button { showSettings = true } label: {
                        Image(systemName: "gearshape.fill")
                            .font(.system(size: 20))
                            .foregroundStyle(Theme.muted)
                            .frame(width: 44, height: 36)
                    }
                    .accessibilityLabel("Settings")
                }
                LazyVGrid(columns: columns(5), spacing: 8) {
                    ForEach(Vocabulary.core, id: \.self) { id in
                        cardButton(id, color: Theme.accent, pictureSize: 34, minHeight: 84)
                    }
                }
                LazyVGrid(columns: columns(3), spacing: 10) {
                    ForEach(Vocabulary.folders) { folder in
                        Button {
                            withAnimation(.snappy) { openFolderID = folder.id }
                        } label: {
                            tile(picture: folder.picture, title: Vocabulary.title(of: folder, words: words),
                                 color: folder.color, pictureSize: 44, minHeight: 108)
                                .overlay(alignment: .topTrailing) {
                                    Image(systemName: "folder.fill")
                                        .font(.system(size: 12))
                                        .foregroundStyle(folder.color)
                                        .padding(8)
                                }
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
            .padding(.bottom, 12)
        }
        .scrollIndicators(.hidden)
    }

    /// An opened folder: back button and its cards.
    private func folderPage(_ folder: Folder) -> some View {
        VStack(spacing: 10) {
            Button {
                withAnimation(.snappy) { openFolderID = nil }
            } label: {
                HStack(spacing: 8) {
                    Image(systemName: "chevron.left").font(.system(size: 18, weight: .bold))
                    Text(folder.picture).font(.system(size: 24))
                    Text(Vocabulary.title(of: folder, words: words)).font(.display(20, weight: .heavy))
                    Spacer()
                }
                .foregroundStyle(Theme.text)
                .frame(minHeight: 44)
                .contentShape(Rectangle())
            }
            .buttonStyle(.plain)

            ScrollView {
                LazyVGrid(columns: columns(3), spacing: 10) {
                    ForEach(folder.wordIDs, id: \.self) { id in
                        cardButton(id, color: folder.color, pictureSize: 44, minHeight: 108)
                    }
                }
                .padding(.bottom, 12)
            }
            .scrollIndicators(.hidden)
        }
    }

    private func columns(_ count: Int) -> [GridItem] {
        Array(repeating: GridItem(.flexible(), spacing: 10), count: count)
    }

    private func cardButton(_ id: String, color: Color, pictureSize: CGFloat, minHeight: CGFloat) -> some View {
        Button {
            add(id)
        } label: {
            tile(picture: Vocabulary.picture(of: id),
                 title: Vocabulary.label(of: id, words: words, child: child),
                 color: color, pictureSize: pictureSize, minHeight: minHeight)
        }
        .buttonStyle(.plain)
    }

    /// Adds the word and says it in the form it has in the sentence.
    private func add(_ id: String) {
        sentence.append(SentenceItem(wordID: id))
        speaker.speak(rendered.last ?? "", language: language, voice: voice)
    }

    private func tile(picture: String, title: String, color: Color, pictureSize: CGFloat, minHeight: CGFloat) -> some View {
        VStack(spacing: 6) {
            Text(picture)
                .font(.display(pictureSize, weight: .heavy))
                .foregroundStyle(Theme.text)
            Text(title)
                .font(.display(pictureSize > 40 ? 15 : 13, weight: .bold))
                .foregroundStyle(Theme.text)
                .lineLimit(2)
                .multilineTextAlignment(.center)
                .minimumScaleFactor(0.6)
        }
        .padding(.horizontal, 4)
        .frame(maxWidth: .infinity, minHeight: minHeight)
        .background(color.opacity(0.18), in: RoundedRectangle(cornerRadius: 20, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 20, style: .continuous)
                .stroke(color.opacity(0.45), lineWidth: 2)
        )
    }
}

/// Shows while the voice loads or if it could not load. Hidden once it works.
private struct ModelBanner: View {
    let speaker: Speaker

    var body: some View {
        switch speaker.modelState {
        case .ready:
            EmptyView()
        case .loading:
            row("Preparing voice") { ProgressView() }
        case .failed:
            row("Voice could not load, using the phone voice") { EmptyView() }
        }
    }

    private func row(_ text: String, @ViewBuilder trailing: () -> some View) -> some View {
        HStack {
            Text(text)
                .font(.system(size: 14, weight: .medium, design: .rounded))
                .foregroundStyle(Theme.muted)
            Spacer()
            trailing()
        }
        .card(padding: 12)
        .padding(.bottom, 4)
    }
}

#Preview {
    ContentView()
}
