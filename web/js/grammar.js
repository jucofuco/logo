// Port of logo/Grammar.swift. Keep the two in step.
// A sentence item is { id, override? }. `words` maps word ids to their entry in words.<lang>.json.

const PERSON = { '1s': 0, '2s': 1, '3s': 2, '1p': 3, '2p': 4, '3p': 5 };

/** Text on a card. Verbs show their label, adjectives the form for the child. */
export function label(id, words, child) {
    const word = words[id];
    if (!word) return id;
    if (word.kind === 'verb') return word.label ?? word.base;
    if (word.kind === 'adjective') return (child === 'girl' ? word.f : word.m) ?? word.base;
    return word.base;
}

function adjectiveForm(word, gender) {
    const form = { f: word.f, n: word.n, pl: word.pl }[gender] ?? word.m;
    return form ?? word.base;
}

/** The text of every item. With `enabled` false each word is just its card text. */
export function render(items, words, child, enabled = true) {
    if (!enabled) return items.map((it) => it.override ?? label(it.id, words, child));

    const childGender = child === 'girl' ? 'f' : 'm';
    let subject = { person: 0, gender: childGender };
    let governs = null;
    let afterVerb = false;
    // State to come back to after "a" / "alebo": "chcem vodu a mlieko", "chcem jesť a piť".
    let carryGoverns = null;
    let carryAfterVerb = false;
    const output = [];

    items.forEach((item, index) => {
        const word = words[item.id];
        if (!word) {
            output.push(item.id);
            return;
        }
        let text = word.base;

        switch (word.kind) {
            case 'pronoun': {
                const person = PERSON[word.person ?? '1s'] ?? 0;
                subject = { person, gender: person >= 3 ? 'pl' : (word.gender ?? childGender) };
                governs = null; afterVerb = false;
                carryGoverns = null; carryAfterVerb = false;
                break;
            }
            case 'noun': {
                switch (governs) {
                    case 'acc': text = word.acc ?? word.base; break;
                    case 'gen': text = word.gen ?? word.base; break;
                    case 'ins': text = word.ins ?? word.base; break;
                    case 'goal': text = word.goal ?? word.acc ?? word.base; break;
                    default: break;
                }
                if (governs === null && word.isPerson) {
                    subject = { person: word.gender === 'pl' ? 5 : 2, gender: word.gender ?? 'm' };
                }
                carryGoverns = governs; carryAfterVerb = false;
                governs = null; afterVerb = false;
                break;
            }
            case 'verb': {
                if (afterVerb) text = word.base;
                else if (word.present?.[subject.person] !== undefined) text = word.present[subject.person];
                governs = word.governs ?? null;
                afterVerb = true;
                carryGoverns = governs; carryAfterVerb = true;
                break;
            }
            case 'adjective': {
                if (word.attr) {
                    // Agrees with the next noun and keeps the case that is waiting for it.
                    let nounGender = subject.gender;
                    for (const later of items.slice(index + 1)) {
                        const next = words[later.id];
                        if (next?.kind === 'noun') { nounGender = next.gender ?? nounGender; break; }
                    }
                    text = (nounGender === 'f' && governs === 'acc' && word.accF)
                        ? word.accF
                        : adjectiveForm(word, nounGender);
                } else {
                    text = adjectiveForm(word, subject.gender);
                    governs = null; afterVerb = false;
                    carryGoverns = null; carryAfterVerb = false;
                }
                break;
            }
            case 'prep': {
                governs = word.governs ?? null;
                afterVerb = false;
                break;
            }
            default: { // word
                if (word.keepsCase) {
                    governs = carryGoverns; afterVerb = carryAfterVerb;
                } else {
                    governs = null; afterVerb = false;
                    carryGoverns = null; carryAfterVerb = false;
                }
            }
        }
        output.push(item.override ?? text);
    });
    return output;
}

/** Every distinct form of a word, for the "pick a form" menu. */
export function forms(word) {
    if (!word) return [];
    let all;
    switch (word.kind) {
        case 'noun': all = [word.base, word.acc, word.gen, word.ins, word.goal]; break;
        case 'verb': all = [word.base, word.label, ...(word.present ?? [])]; break;
        case 'adjective': all = [word.m, word.f, word.n, word.pl, word.accF]; break;
        default: all = [word.base];
    }
    return [...new Set(all.filter(Boolean))];
}
