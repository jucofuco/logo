import SwiftUI

enum AppLanguage: String, CaseIterable, Identifiable {
    case sk, cs

    var id: String { rawValue }

    var title: String {
        switch self {
        case .sk: "Slovenčina"
        case .cs: "Čeština"
        }
    }

    /// Language code Supertonic expects (`sk` and `cs` are both supported).
    var voiceCode: String { rawValue }

    /// Voice of the phone, used while Supertonic is not ready.
    var systemVoice: String {
        switch self {
        case .sk: "sk-SK"
        case .cs: "cs-CZ"
        }
    }

    var sampleSentence: String {
        switch self {
        case .sk: "Ahoj, ako sa máš?"
        case .cs: "Ahoj, jak se máš?"
        }
    }
}

enum ChildGender: String, CaseIterable, Identifiable {
    case boy, girl

    var id: String { rawValue }
    var title: String { rawValue.capitalized }
}

/// One entry of `words.<lang>.json`. Which fields are filled depends on `kind`.
struct WordEntry: Decodable {
    enum Kind: String, Decodable { case pronoun, noun, verb, adjective, prep, word }

    let kind: Kind
    /// Dictionary form: nominative, infinitive, masculine singular.
    let base: String
    /// Shown on the card instead of `base` (verbs: "chcem" for chcieť).
    var label: String?

    /// Pronoun: 1s 2s 3s 1p 2p 3p.
    var person: String?
    /// Pronoun (on/ona), noun: m f n pl.
    var gender: String?

    /// Noun: accusative, genitive, instrumental, and the "where to" form of places and people.
    var acc: String?
    var gen: String?
    var ins: String?
    var goal: String?
    /// Noun that can be the subject of the sentence (mama, otec).
    var isPerson: Bool?

    /// Verb: six present forms in the order of `person`, and what the next word is put into.
    var present: [String]?
    /// Verb: acc, goal or adj. Preposition: acc, gen or ins.
    var governs: String?

    /// Adjective forms. `accF` is the feminine accusative, used by `attr` adjectives.
    var m: String?
    var f: String?
    var n: String?
    var pl: String?
    var accF: String?
    /// Adjective that agrees with the noun after it (veľký), not with the subject (šťastný).
    var attr: Bool?

    /// "a", "alebo": the next word gets the same form as the one before.
    var keepsCase: Bool?
}

/// A folder on the main screen. Its title comes from the words file (`folder.<id>`).
struct Folder: Identifiable {
    let id: String
    let picture: String
    /// Id of its pictogram (`icon` in structure.json), nil if the folder has none.
    let icon: String?
    let color: Color
    let wordIDs: [String]
}

/// Loads `structure.json` (what is shown where) and `words.<lang>.json` (the forms of each word).
/// A missing id is a data bug, so it stops the app with a clear message.
enum Vocabulary {
    private struct Structure: Decodable {
        struct FolderSpec: Decodable {
            let id: String
            let picture: String
            let icon: String?
            let color: String
            let words: [String]
        }

        let core: [String]
        let folders: [FolderSpec]
        let pictures: [String: String]
    }

    private static let structure: Structure = load("structure")

    private static let wordsByLanguage: [AppLanguage: [String: WordEntry]] = {
        var result: [AppLanguage: [String: WordEntry]] = [:]
        for language in AppLanguage.allCases {
            let words: [String: WordEntry] = load("words.\(language.rawValue)")
            for id in requiredIDs where words[id] == nil {
                fatalError("words.\(language.rawValue).json has no entry for \"\(id)\"")
            }
            result[language] = words
        }
        return result
    }()

    /// Shown in every main screen row.
    static let core: [String] = structure.core

    static let folders: [Folder] = structure.folders.map {
        Folder(id: $0.id, picture: $0.picture, icon: $0.icon, color: color(named: $0.color), wordIDs: $0.words)
    }

    static func words(for language: AppLanguage) -> [String: WordEntry] {
        wordsByLanguage[language] ?? [:]
    }

    static func picture(of id: String) -> String {
        structure.pictures[id] ?? "❓"
    }

    static func title(of folder: Folder, words: [String: WordEntry]) -> String {
        words["folder.\(folder.id)"]?.base ?? folder.id
    }

    /// Text on a card. Verbs show their `label`, adjectives the form for the child.
    static func label(of id: String, words: [String: WordEntry], child: ChildGender) -> String {
        guard let word = words[id] else { return id }
        switch word.kind {
        case .verb: return word.label ?? word.base
        case .adjective: return (child == .girl ? word.f : word.m) ?? word.base
        default: return word.base
        }
    }

    private static var requiredIDs: [String] {
        structure.core
            + structure.folders.flatMap { ["folder.\($0.id)"] + $0.words }
    }

    private static func load<T: Decodable>(_ name: String) -> T {
        guard let url = Bundle.main.url(forResource: name, withExtension: "json") else {
            fatalError("\(name).json is not in the app bundle")
        }
        do {
            return try JSONDecoder().decode(T.self, from: Data(contentsOf: url))
        } catch {
            fatalError("Cannot read \(name).json: \(error)")
        }
    }

    private static func color(named name: String) -> Color {
        switch name {
        case "orange": .orange
        case "blue": .blue
        case "green": .green
        case "red": .red
        case "pink": .pink
        case "purple": .purple
        case "yellow": .yellow
        case "teal": .teal
        case "indigo": .indigo
        default: .gray
        }
    }
}
