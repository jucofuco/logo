import SwiftUI

struct SettingsView: View {
    let speaker: Speaker

    @Environment(\.dismiss) private var dismiss
    @AppStorage("language") private var language = AppLanguage.sk
    @AppStorage("childGender") private var child = ChildGender.boy
    @AppStorage("grammar") private var grammar = true
    @AppStorage("voice") private var voice = SupertonicModel.defaultVoice
    @AppStorage("appearance") private var appearance = Appearance.system

    var body: some View {
        NavigationStack {
            Form {
                Section("Language") {
                    Picker("Language", selection: $language) {
                        ForEach(AppLanguage.allCases) { Text($0.title).tag($0) }
                    }
                    .pickerStyle(.segmented)
                }

                Section {
                    Toggle("Word forms", isOn: $grammar)
                    if grammar {
                        Picker("Child", selection: $child) {
                            ForEach(ChildGender.allCases) { Text($0.title).tag($0) }
                        }
                        .pickerStyle(.segmented)
                    }
                } header: {
                    Text("Grammar")
                } footer: {
                    Text(grammar
                         ? "Picks the right form of each word, like \"chcem vodu\". Long press a word in the sentence to change its form."
                         : "Every word is said as it is on the card.")
                }

                Section("Voice") {
                    ForEach(SupertonicModel.voices, id: \.self) { name in
                        Button {
                            voice = name
                            speaker.speak(language.sampleSentence, language: language, voice: name)
                        } label: {
                            HStack {
                                Text(SupertonicModel.voiceTitle(name)).foregroundStyle(Theme.text)
                                Spacer()
                                if voice == name {
                                    Image(systemName: "checkmark").foregroundStyle(Theme.accent)
                                }
                            }
                        }
                    }
                }

                Section("Developer") {
                    NavigationLink("Speed test") { BenchmarkView() }
                }

                Section("Appearance") {
                    Picker("Appearance", selection: $appearance) {
                        ForEach(Appearance.allCases) { Text($0.title).tag($0) }
                    }
                    .pickerStyle(.segmented)
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
        .followsAppearance()
    }
}
