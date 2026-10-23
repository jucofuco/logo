# Plan: declension, Czech, model in the app bundle

**Status: implemented** (see `CLAUDE.md` code map for the differences). Kept as a record.

Written 2026-10-23 for an implementing agent. Read `CLAUDE.md` first (environment, build
commands, owner preferences). Reminders that matter here:

- There is **no Swift compiler on the Pi**. You cannot build. Write careful Swift 6 code, then
  give the owner the build commands from `CLAUDE.md` and wait for the result.
- Commit messages: only what the commit did. **No Co-Authored-By line.** Commit and
  `git push origin main` after each part.
- UI strings in English, short, no em/en dashes. Spoken words are Slovak or Czech.
- Work in the order of the parts below. Each part should build on its own.

Current code to know: `logo/Vocabulary.swift` (cards as Swift literals), `logo/ContentView.swift`
(sentence strip, Speak button, main page with core words + folders, opened folder),
`logo/Speech/Speaker.swift` (Supertonic or system voice), `logo/Speech/SupertonicEngine.swift`
(model download + synthesis actor), `logo/Speech/SupertonicHelper.swift` (vendored, do not edit).

---

## Part 1. Vocabulary as data with word forms

Replace the Swift literals in `logo/Vocabulary.swift` with JSON resources, so every word can carry
its grammatical forms and Czech can be added as a second file with the same ids.

### Files

- `logo/Vocabulary/structure.json`: what is shown where, same for all languages.
- `logo/Vocabulary/words.sk.json`: Slovak forms for every word id.
- `logo/Vocabulary/words.cs.json`: Czech forms for every word id (Part 3, start with Slovak).
- `logo/Vocabulary.swift`: Codable types + loading + lookup. Load once (static let), crash with a
  clear `fatalError` message if a word id from `structure.json` is missing in a words file
  (that is a data bug the owner should see immediately).

They are under `logo/`, so XcodeGen picks them up as bundle resources (check that the built app
contains them: `Bundle.main.url(forResource: "structure", withExtension: "json")`).

### `structure.json`

```json
{
  "core": ["me", "yes", "want", "no", "dontWant"],
  "folders": [
    { "id": "toys", "picture": "🧸", "color": "orange", "words": ["ball", "computer", "..."] }
  ],
  "pictures": { "me": "🙋", "ball": "⚽", "...": "..." }
}
```

- Folder order, word order and pictures: take them from the current `Vocabulary.swift`
  (they follow the owner's tree, keep it exactly).
- Folder titles are per language, so they live in the words files as words with id
  `folder.<id>` (e.g. `"folder.toys": { "kind": "word", "base": "hračky" }`).
- `color` is one of the SwiftUI names already used (orange, blue, green, red, pink, purple,
  yellow, teal, indigo, gray); map it in Swift.
- Ids are short English camelCase (`ball`, `glassOfWater`, `shoppingMall`).
- ABC and numbers: ids `letter.a` … `letter.z`, `number.0` … `number.9`; picture is the
  uppercase letter / digit (as today).

New words that are not in the owner's tree but are needed for grammar: add them to the
`verbs` folder at the start: `be` (byť / být), `have` (mať / mít), `see` (vidieť / vidět),
`need` (potrebovať / potřebovat). Tell the owner you added them.

### `words.<lang>.json`

One entry per id. `kind` decides which fields exist:

| kind | fields | example (sk) |
|---|---|---|
| `pronoun` | `base`, `person` (`1s 2s 3s 1p 2p 3p`), `gender` (`m`/`f`/`n`, only for on/ona/ono) | ja: `{base:"ja", person:"1s"}` |
| `noun` | `base` (nom), `acc`, `gen`, `ins`, `gender` (`m`/`f`/`n`/`pl`), optional `goal` (direction, places only), optional `person: true` for people | voda: `{base:"voda", acc:"vodu", gen:"vody", ins:"vodou", gender:"f"}` |
| `verb` | `base` (infinitive), `label` (what the card shows, defaults to base), `present` (6 forms in order 1s 2s 3s 1p 2p 3p), `governs` (`acc` / `goal` / `adj` / none) | chcieť: `{base:"chcieť", label:"chcem", present:["chcem","chceš","chce","chceme","chcete","chcú"], governs:"acc"}` |
| `adjective` | `m`, `f`, `n`, `pl` | `{m:"šťastný", f:"šťastná", n:"šťastné", pl:"šťastní"}` |
| `prep` | `base`, `governs` (`acc` / `gen` / `ins`) | bez: `{base:"bez", governs:"gen"}` |
| `word` | `base`, optional `keepsCase: true` (conjunctions a, alebo) | áno, nie, letters, numbers |

Which words are which:

- Pronouns: ja, ty (if added later), on, ona, oni, my, vy. `mňa`, `nás` are `word`.
- People (`person: true` nouns): mama, otec, brat, sestra, babička, dedko, učiteľ.
- Places get `goal`: sk `domov`→"domov", `škola`→"do školy", `zoo`→"do zoo", `more`→"k moru",
  `obchod`→"do obchodu", `park`→"do parku", `kúpeľňa`→"do kúpeľne", `knižnica`→"do knižnice",
  `kino`→"do kina", `múzeum`→"do múzea", `reštaurácia`→"do reštaurácie",
  `nákupné centrum`→"do nákupného centra", `trieda`→"do triedy", `bazén`→"na bazén",
  `ambulancia`→"do ambulancie".
- Adjectives: feelings šťastný, smutný, prekvapený, nahnevaný, zvedavý, znudený, vystrašený,
  chorý; sizes veľký, stredný, malý; ďalší. `láska`, `zima`, `horúco`, `v rozpakoch` are `word`.
- `core.want` = chcieť (label "chcem"), `core.dontWant` = nechcieť (label "nechcem").
- Verb `governs`: chcieť, nechcieť, mať, jesť, piť, vidieť, potrebovať, robiť, hádzať,
  počúvať → `acc`; ísť → `goal`; byť → `adj`; the rest none.
- Prepositions: s → `ins`, bez → `gen`, z → `gen`, na → `acc`. `a`, `alebo` → `word` with
  `keepsCase: true`. `ale`, `hoci`, `ak`, `ako` → plain `word`.

The owner is a native speaker and will check the forms. Write them carefully, then in the final
message list any word you were unsure about.

Nothing in the UI changes in Part 1 except that labels now come from the data (cards show
`label` for verbs, `base` for nouns/words, the adjective form for the child's gender, see Part 2).

---

## Part 2. Grammar: the sentence picks the right forms

### Sentence model

Today the sentence is `[Card]`. Change it to `[SentenceItem]`:

```swift
struct SentenceItem: Identifiable { let id = UUID(); let wordID: String; var override: String? }
```

Storing ids (not strings) means the sentence re-renders when the language or child gender
changes.

### `logo/Grammar.swift` (new, pure functions, no UI)

```swift
enum ChildGender: String { case boy, girl }
/// Surface form for every item, in order.
static func render(_ items: [SentenceItem], words: Words, child: ChildGender) -> [String]
```

Walk left to right with this state:

- `subject`: person + gender. Starts as `1s` with the child's gender (the child talks about
  themself, so "chcieť" alone gives "chcem").
- `governs`: what the next noun/adjective should be (`acc`, `gen`, `ins`, `goal`, `adj`, or nil).
- `afterVerb`: true right after a verb (or after a verb + `keepsCase` word).

Rules per kind:

1. **pronoun**: output `base`. Set `subject` to its person; gender from the word, or the child's
   gender for `1s`, or plural for `1p 2p 3p`. Reset `governs`, `afterVerb = false`.
2. **noun**: form from `governs`: `acc`/`gen`/`ins` → that field; `goal` → `goal` if present,
   else `acc`. No `governs` → `base`. If `governs` is nil and the noun has `person: true`, it
   becomes the subject (`3s`, its gender). After output, reset `governs`, `afterVerb = false`.
3. **verb**: if `afterVerb` → `base` (infinitive: "chcem **jesť**", "idem **spať**"), else
   `present[subject.person]`. Then `governs = verb.governs`, `afterVerb = true`.
4. **adjective**: form by `subject` gender (`m`/`f`/`n`, `pl` for plural persons). Reset
   `governs`, `afterVerb = false`.
5. **prep**: output `base`, `governs = prep.governs`, `afterVerb = false`.
6. **word**: output `base`. If `keepsCase`, keep `governs` and `afterVerb` ("chcem vodu
   **a** mlieko", "chcem jesť **a** piť"). Otherwise reset both.
7. **override**: if the item has `override`, output it instead, but still update the state as
   the kind says.

Capitalize the first letter of the joined sentence (already done in `sentenceText`).

### Expected results (check these by hand in the app, child = girl unless noted)

| taps | Slovak | Czech |
|---|---|---|
| ja, chcem, voda | Ja chcem vodu | Já chci vodu |
| chcem, lopta, a, autíčko | Chcem loptu a autíčko | Chci míč a autíčko |
| ona, chcem, jesť | Ona chce jesť | Ona chce jíst |
| ísť, škola | Idem do školy | Jdu do školy |
| my, ísť, park | My ideme do parku | My jdeme do parku |
| ja, byť, šťastný | Ja som šťastná | Já jsem šťastná |
| ja, byť, šťastný (boy) | Ja som šťastný | Já jsem šťastný |
| mama, byť, chorý | Mama je chorá | Máma je nemocná |
| oni, byť, smutný | Oni sú smutní | Oni jsou smutní |
| chcem, piť, mlieko | Chcem piť mlieko | Chci pít mléko |
| bez, mlieko | Bez mlieka | Bez mléka |
| s, mama | S mamou | S mámou |

### UI changes in `ContentView.swift`

- Sentence strip shows the rendered forms (picture + rendered word).
- Tapping a card: append the item, then speak the **rendered** form of that new item (what the
  strip shows), not the base form.
- **Long press a sentence chip** → `contextMenu` (or `confirmationDialog`) listing every distinct
  form of that word (all fields of its kind) plus "Automatic". Picking one sets `override`;
  "Automatic" clears it. Tap still removes the chip, as today.
- Card labels: verbs show `label`, adjectives show the child's gender form, others `base`.

---

## Part 3. Czech

- `logo/Vocabulary/words.cs.json` with every id from `structure.json` (same kinds and fields).
  Core: já, ano, chci (chtít), ne, nechci (nechtít). Folder titles: hračky, oblečení, slovesa,
  jídlo, pocity, místa, lidé, ABC, čísla, více.
- Use natural Czech, not a letter-by-letter copy of Slovak (lopta → míč, mama → máma,
  chorý → nemocný, kúpeľňa → koupelna, šiltovka → kšiltovka, nohavice → kalhoty, …).
- `enum AppLanguage: String { case sk, cs }` with the Supertonic code (`sk`/`cs`, both are in
  `AVAILABLE_LANGS`) and the system voice (`sk-SK` / `cs-CZ`).
- `Speaker.speak(_ text: String, language: AppLanguage)`: pass the language to
  `SupertonicEngine.synthesize(_:lang:)` and to the system voice. Cache key = language + text.

### Settings sheet (new, `logo/SettingsView.swift`)

A small gear button on the main page (top right, above the core words; not on folder pages,
so kids hit it less). Sheet with `.followsAppearance()`:

- **Language**: Slovenčina / Čeština (`@AppStorage("language")`, default `sk`).
- **Child**: Boy / Girl (`@AppStorage("childGender")`, default `boy`).
- **Appearance**: System / Light / Dark (`Appearance` already exists in `Theme.swift`).

Changing language or child re-renders the sentence (it stores ids); clear all `override`s on a
language change because they are strings in the old language.

---

## Part 4. Supertonic model in the app bundle (no Download button)

The model files are too big for GitHub (two are over 100 MB), so they are fetched on the Mac
before building into a git-ignored folder and copied into the app as a folder reference.

- `Scripts/fetch_model.sh`: downloads the 7 files listed in `SupertonicModel.files`
  (`logo/Speech/SupertonicEngine.swift`) from
  `https://huggingface.co/supertone-oss-archive/supertonic-3/resolve/aafc6e32416a594460b32413efc49d7fe4ce6d46/<path>`
  into `Model/onnx/…` and `Model/voice_styles/F1.json` at the repo root. Skip files that already
  exist with the right size; check sizes after download and exit non-zero on a mismatch.
  POSIX `sh` + `curl -fL`, no other tools.
- `.gitignore`: add `Model/`.
- `project.yml`, target `logo`: add a resource folder reference
  ```yaml
      sources:
        - logo
        - path: Model
          type: folder
          buildPhase: resources
  ```
  If `Model/` is missing, the build must fail (do not mark it optional): that tells the owner to
  run the script.
- `SupertonicModel`: read files from `Bundle.main.resourceURL/Model/...` instead of
  Application Support. Delete the download code, `ModelState.missing/downloading`, and the
  Download / Retry banner. Keep a small "Preparing voice" indicator while the engine loads
  (loading 4 ONNX sessions takes a few seconds), then the system voice is only the fallback if
  loading fails.
- `CLAUDE.md`: add `sh Scripts/fetch_model.sh` as a one-time step before the first build, and
  note the app is now about 400 MB bigger (each install takes longer).

---

## Part 5. Finish

- Update `CLAUDE.md` code map and "Current status" for all new files.
- Give the owner, in this order: `sh Scripts/fetch_model.sh` (once), then the build command
  (`~/bin/run.sh <path to repo>` on the Mac).
- On the phone the owner checks: the table in Part 2 in both languages, long press override,
  settings switch, that Supertonic speaks without any download.
- List words whose forms you were unsure about.
