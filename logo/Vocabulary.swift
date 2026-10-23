import SwiftUI

/// One picture card. `word` is what gets spoken and added to the sentence.
/// `picture` is an emoji, or a letter/digit for ABC and numbers.
struct Card: Identifiable, Hashable {
    let id = UUID()
    let picture: String
    let word: String

    init(_ picture: String, _ word: String) {
        self.picture = picture
        self.word = word
    }
}

/// A subcategory on the main screen. Opening it shows its cards.
struct Folder: Identifiable {
    let id: String
    let picture: String
    let title: String
    let color: Color
    let cards: [Card]
}

/// Slovak vocabulary, laid out like the owner's tree: core words on the main screen, then folders.
enum Vocabulary {
    /// Always visible on the main screen.
    static let core: [Card] = [
        Card("🙋", "ja"),
        Card("👍", "áno"),
        Card("🙏", "chcem"),
        Card("👎", "nie"),
        Card("🙅", "nechcem"),
    ]

    static let folders: [Folder] = [
        Folder(id: "toys", picture: "🧸", title: "hračky", color: .orange, cards: [
            Card("⚽", "lopta"),
            Card("💻", "počítač"),
            Card("📱", "mobilný telefón"),
            Card("🧸", "medvedík"),
            Card("🪆", "bábika"),
            Card("🧱", "kocky"),
            Card("⭕", "obruč"),
            Card("🎲", "spoločenská hra"),
            Card("🃏", "karty"),
            Card("🏗️", "lego"),
            Card("🚗", "autíčko"),
            Card("🎈", "balón"),
            Card("🧩", "puzzle"),
            Card("🚲", "bicykel"),
            Card("🕹️", "tetris"),
        ]),
        Folder(id: "clothes", picture: "👕", title: "oblečenie", color: .blue, cards: [
            Card("👖", "nohavice"),
            Card("👕", "tričko"),
            Card("🩳", "šortky"),
            Card("👔", "košeľa"),
            Card("🧦", "ponožky"),
            Card("👟", "topánky"),
            Card("🧢", "šiltovka"),
            Card("🧥", "kabát"),
            Card("🩲", "nohavičky"),
            Card("👓", "okuliare"),
            Card("🕶️", "slnečné okuliare"),
            Card("🧣", "šatka"),
        ]),
        Folder(id: "verbs", picture: "🏃", title: "slovesá", color: .green, cards: [
            Card("🛠️", "robiť"),
            Card("🙋", "požiadať"),
            Card("👕", "obliekať sa"),
            Card("🥤", "piť"),
            Card("🍽️", "jesť"),
            Card("🚶", "ísť"),
            Card("👂", "počúvať"),
            Card("🛝", "hrať"),
            Card("😴", "spať"),
            Card("🗣️", "hovoriť"),
            Card("🍳", "variť"),
            Card("⌨️", "zadať"),
            Card("🥄", "miešať"),
            Card("🤾", "hádzať"),
        ]),
        Folder(id: "food", picture: "🍎", title: "jedlo", color: .red, cards: [
            Card("🍕", "pizza"),
            Card("🍞", "chlieb"),
            Card("🧀", "syr"),
            Card("🥛", "mlieko"),
            Card("🎂", "torta"),
            Card("🥃", "pohár vody"),
            Card("🧈", "maslo"),
            Card("🍚", "ryža"),
            Card("🍎", "ovocie"),
            Card("🥦", "zelenina"),
            Card("🍦", "zmrzlina"),
            Card("🍫", "čokoláda"),
            Card("🥚", "vajcia"),
            Card("🍲", "polievka"),
            Card("🍗", "kurča"),
        ]),
        Folder(id: "feelings", picture: "😊", title: "pocity", color: .pink, cards: [
            Card("😊", "šťastný"),
            Card("❤️", "láska"),
            Card("😢", "smutný"),
            Card("😮", "prekvapený"),
            Card("😠", "nahnevaný"),
            Card("🤔", "zvedavý"),
            Card("😳", "v rozpakoch"),
            Card("😑", "znudený"),
            Card("😨", "vystrašený"),
            Card("🤒", "chorý"),
            Card("🥵", "horúco"),
            Card("🥶", "zima"),
        ]),
        Folder(id: "places", picture: "🏠", title: "miesta", color: .purple, cards: [
            Card("🏠", "domov"),
            Card("🏫", "škola"),
            Card("🦁", "zoo"),
            Card("🌊", "more"),
            Card("🛒", "obchod"),
            Card("🌳", "park"),
            Card("🛁", "kúpeľňa"),
            Card("📚", "knižnica"),
            Card("🎬", "kino"),
            Card("🏛️", "múzeum"),
            Card("🍴", "reštaurácia"),
            Card("🏬", "nákupné centrum"),
            Card("🧑‍🏫", "trieda"),
            Card("🏊", "bazén"),
            Card("🩺", "ambulancia"),
        ]),
        Folder(id: "people", picture: "👨‍👩‍👧", title: "ľudia", color: .yellow, cards: [
            Card("🙋", "ja"),
            Card("👦", "on"),
            Card("👧", "ona"),
            Card("👥", "oni"),
            Card("🫂", "my"),
            Card("👉", "vy"),
            Card("👈", "mňa"),
            Card("🤝", "nás"),
            Card("👩", "mama"),
            Card("👨", "otec"),
            Card("👦", "brat"),
            Card("👧", "sestra"),
            Card("👵", "babička"),
            Card("👴", "dedko"),
            Card("🧑‍🏫", "učiteľ"),
        ]),
        Folder(id: "abc", picture: "🔤", title: "ABC", color: .teal,
               cards: "abcdefghijklmnopqrstuvwxyz".map { Card(String($0).uppercased(), String($0)) }),
        Folder(id: "numbers", picture: "🔢", title: "čísla", color: .indigo, cards:
            ["nula", "jeden", "dva", "tri", "štyri", "päť", "šesť", "sedem", "osem", "deväť"]
                .enumerated().map { Card(String($0.offset), $0.element) }),
        Folder(id: "more", picture: "💬", title: "viac", color: .gray, cards: [
            Card("🎨", "farby"),
            Card("➕", "a"),
            Card("🔀", "alebo"),
            Card("↩️", "ale"),
            Card("🤷", "hoci"),
            Card("🤝", "s"),
            Card("🚫", "bez"),
            Card("⏭️", "ďalší"),
            Card("⬇️", "na"),
            Card("⬅️", "z"),
            Card("❓", "ak"),
            Card("🐘", "veľký"),
            Card("🐕", "stredný"),
            Card("🐁", "malý"),
            Card("🟰", "ako"),
        ]),
    ]
}
