import Foundation

/// A word in the sentence. Stores the id, not the text, so the sentence follows the language and
/// the child's gender. `override` is a form picked by hand (long press on the chip).
struct SentenceItem: Identifiable, Hashable {
    let id = UUID()
    let wordID: String
    var override: String?
}

/// Picks the form of each word from the words before it: object case after a verb, verb form by
/// person, "where to" forms after "ísť", adjective gender by subject or by the next noun.
enum Grammar {
    private enum Governed: String {
        case acc, gen, ins, goal, adj
    }

    private struct Subject {
        /// Index into `WordEntry.present`.
        var person: Int
        /// m f n pl.
        var gender: String
    }

    private static let personIndex = ["1s": 0, "2s": 1, "3s": 2, "1p": 3, "2p": 4, "3p": 5]

    /// The text of every item, in order. With `enabled` false each word is just its card text.
    static func render(_ items: [SentenceItem], words: [String: WordEntry], child: ChildGender, enabled: Bool = true) -> [String] {
        guard enabled else {
            return items.map { $0.override ?? Vocabulary.label(of: $0.wordID, words: words, child: child) }
        }

        let childGender = child == .girl ? "f" : "m"
        var subject = Subject(person: 0, gender: childGender)
        var governs: Governed?
        var afterVerb = false
        // State to come back to after "a" / "alebo": "chcem vodu a mlieko", "chcem jesť a piť".
        var carryGoverns: Governed?
        var carryAfterVerb = false
        var output: [String] = []

        for (index, item) in items.enumerated() {
            guard let word = words[item.wordID] else {
                output.append(item.wordID)
                continue
            }
            var text = word.base

            switch word.kind {
            case .pronoun:
                let person = personIndex[word.person ?? "1s"] ?? 0
                let gender = person >= 3 ? "pl" : (word.gender ?? childGender)
                subject = Subject(person: person, gender: gender)
                governs = nil
                afterVerb = false
                carryGoverns = nil
                carryAfterVerb = false

            case .noun:
                switch governs {
                case .acc: text = word.acc ?? word.base
                case .gen: text = word.gen ?? word.base
                case .ins: text = word.ins ?? word.base
                case .goal: text = word.goal ?? word.acc ?? word.base
                case .adj, nil: break
                }
                if governs == nil, word.isPerson == true {
                    subject = Subject(person: word.gender == "pl" ? 5 : 2, gender: word.gender ?? "m")
                }
                carryGoverns = governs
                carryAfterVerb = false
                governs = nil
                afterVerb = false

            case .verb:
                if afterVerb {
                    text = word.base
                } else if let forms = word.present, forms.indices.contains(subject.person) {
                    text = forms[subject.person]
                }
                governs = word.governs.flatMap(Governed.init(rawValue:))
                afterVerb = true
                carryGoverns = governs
                carryAfterVerb = true

            case .adjective:
                if word.attr == true {
                    // Agrees with the next noun and keeps the case that is waiting for it.
                    let nounGender = items[(index + 1)...]
                        .lazy.compactMap { words[$0.wordID] }
                        .first { $0.kind == .noun }?.gender ?? subject.gender
                    if nounGender == "f", governs == .acc, let accF = word.accF {
                        text = accF
                    } else {
                        text = form(of: word, gender: nounGender)
                    }
                } else {
                    text = form(of: word, gender: subject.gender)
                    governs = nil
                    afterVerb = false
                    carryGoverns = nil
                    carryAfterVerb = false
                }

            case .prep:
                governs = word.governs.flatMap(Governed.init(rawValue:))
                afterVerb = false

            case .word:
                if word.keepsCase == true {
                    governs = carryGoverns
                    afterVerb = carryAfterVerb
                } else {
                    governs = nil
                    afterVerb = false
                    carryGoverns = nil
                    carryAfterVerb = false
                }
            }

            output.append(item.override ?? text)
        }
        return output
    }

    /// Every distinct form of a word, for the "pick a form" menu.
    static func forms(of word: WordEntry?) -> [String] {
        guard let word else { return [] }
        let all: [String?]
        switch word.kind {
        case .noun: all = [word.base, word.acc, word.gen, word.ins, word.goal]
        case .verb: all = [word.base, word.label] + (word.present ?? [])
        case .adjective: all = [word.m, word.f, word.n, word.pl, word.accF]
        case .pronoun, .prep, .word: all = [word.base]
        }
        var seen = Set<String>()
        return all.compactMap { $0 }.filter { seen.insert($0).inserted }
    }

    private static func form(of word: WordEntry, gender: String) -> String {
        let form: String?
        switch gender {
        case "f": form = word.f
        case "n": form = word.n
        case "pl": form = word.pl
        default: form = word.m
        }
        return form ?? word.base
    }
}
