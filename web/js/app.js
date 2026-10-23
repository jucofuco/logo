// Web version of the picture board. Same words (logo/Vocabulary, served as data/) and the same
// grammar as the iOS app; see ../CLAUDE.md. Plain ES modules, no build step.
import { Speaker } from './speaker.js';
import { render, forms, label } from './grammar.js';
import { VOICES, voiceTitle, totalSize } from './model.js';
import { log } from './log.js';

const LANGS = {
    sk: { title: 'Slovenčina', sample: 'Ahoj, ako sa máš?' },
    cs: { title: 'Čeština', sample: 'Ahoj, jak se máš?' },
};
const COLORS = {
    orange: '#FF9500', blue: '#0A84FF', green: '#34C759', red: '#FF3B30', pink: '#FF2D55',
    purple: '#AF52DE', yellow: '#FFCC00', teal: '#30B0C7', indigo: '#5856D6', gray: '#8E8E93',
};
const STEPS = [['Fastest', 4], ['Fast', 6], ['Normal', 8], ['Best', 12]];
const DEFAULTS = { language: 'sk', child: 'boy', grammar: true, voice: 'F1', speed: 1, steps: 8, engine: 'cpu' };

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

const settings = (() => {
    try { return { ...DEFAULTS, ...JSON.parse(localStorage.getItem('logo-settings') ?? '{}') }; } catch { return { ...DEFAULTS }; }
})();
function saveSettings() {
    try { localStorage.setItem('logo-settings', JSON.stringify(settings)); } catch { /* private mode */ }
}

let structure;
let wordsByLang;
const state = { sentence: [], folder: null };
const speaker = new Speaker(() => { renderBanner(); renderSpeak(); }, settings.engine);

const words = () => wordsByLang[settings.language];
const rendered = () => render(state.sentence, words(), settings.child, settings.grammar);
const sentenceText = () => {
    const text = rendered().join(' ');
    return text.charAt(0).toUpperCase() + text.slice(1);
};
const say = (text) => speaker.speak(text, settings.language, settings.voice, { speed: settings.speed, steps: settings.steps });

// ---------------------------------------------------------------- sentence

function renderStrip() {
    const texts = rendered();
    $('chips').innerHTML = state.sentence.length
        ? state.sentence.map((item, i) => `<button class="chip" data-i="${i}"><span class="pic">${esc(structure.pictures[item.id] ?? '❓')}</span><span class="lbl">${esc(texts[i])}</span></button>`).join('')
        : '<span class="hint">Tap a picture</span>';
    $('chips').scrollLeft = $('chips').scrollWidth;
    $('undo').disabled = !state.sentence.length;
    $('speak').disabled = !state.sentence.length;
}

function renderSpeak() {
    $('speak').classList.toggle('thinking', speaker.thinking);
}

function add(id) {
    state.sentence.push({ id });
    renderStrip();
    say(rendered().at(-1));
}

function removeAt(index) {
    state.sentence.splice(index, 1);
    renderStrip();
}

// A tap on a chip removes it, a long press picks another form of the word.
let press = null;
const chips = $('chips');
function cancelPress() {
    if (press) clearTimeout(press.timer);
    press = null;
}
chips.addEventListener('pointerdown', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    const index = Number(chip.dataset.i);
    press = {
        index, x: e.clientX, y: e.clientY,
        timer: setTimeout(() => { press = null; openForms(index); }, 450),
    };
});
chips.addEventListener('pointermove', (e) => {
    if (press && Math.hypot(e.clientX - press.x, e.clientY - press.y) > 8) cancelPress();
});
chips.addEventListener('pointerup', () => {
    if (!press) return;
    const { index } = press;
    cancelPress();
    removeAt(index);
});
chips.addEventListener('pointercancel', cancelPress);
chips.addEventListener('contextmenu', (e) => e.preventDefault());

$('undo').addEventListener('click', () => removeAt(state.sentence.length - 1));
$('speak').addEventListener('click', () => say(sentenceText()));

// ---------------------------------------------------------------- forms menu

let formsFor = null;
function openForms(index) {
    if (!settings.grammar) return;
    const item = state.sentence[index];
    if (!item) return;
    const options = forms(words()[item.id]);
    if (options.length < 2) return;
    formsFor = index;
    $('forms-title').textContent = rendered()[index];
    $('forms-list').innerHTML =
        `<button data-form="" class="${item.override === undefined ? 'on' : ''}">Automatic</button>` +
        options.map((f) => `<button data-form="${esc(f)}" class="${item.override === f ? 'on' : ''}">${esc(f)}</button>`).join('');
    $('forms').showModal();
}
$('forms-list').addEventListener('click', (e) => {
    const button = e.target.closest('[data-form]');
    if (!button || formsFor === null) return;
    const item = state.sentence[formsFor];
    if (button.dataset.form) item.override = button.dataset.form; else delete item.override;
    $('forms').close();
    renderStrip();
});

// ---------------------------------------------------------------- cards

function tile(id) {
    return `<button class="tile" data-word="${esc(id)}"><span class="pic">${esc(structure.pictures[id] ?? '❓')}</span><span class="lbl">${esc(label(id, words(), settings.child))}</span></button>`;
}

function folderTile(folder) {
    return `<button class="tile" style="--c:${COLORS[folder.color] ?? COLORS.gray}" data-folder="${esc(folder.id)}"><span class="folder">📁</span><span class="pic">${esc(folder.picture)}</span><span class="lbl">${esc(words()[`folder.${folder.id}`].base)}</span></button>`;
}

function renderPage() {
    const page = $('page');
    if (state.folder) {
        const folder = structure.folders.find((f) => f.id === state.folder);
        page.innerHTML =
            `<button class="back" data-back><span class="arrow">‹</span><span class="pic">${esc(folder.picture)}</span><span>${esc(words()[`folder.${folder.id}`].base)}</span></button>` +
            `<div class="grid cards" style="--c:${COLORS[folder.color] ?? COLORS.gray}">${folder.words.map(tile).join('')}</div>`;
    } else {
        page.innerHTML =
            '<div class="head"><button class="gear" data-settings aria-label="Settings">⚙️</button></div>' +
            `<div class="grid core" style="--c:var(--accent)">${structure.core.map(tile).join('')}</div>` +
            `<div class="grid cards">${structure.folders.map(folderTile).join('')}</div>`;
    }
    page.scrollTop = 0;
}

$('page').addEventListener('click', (e) => {
    const word = e.target.closest('[data-word]');
    if (word) return add(word.dataset.word);
    const folder = e.target.closest('[data-folder]');
    if (folder) { state.folder = folder.dataset.folder; return renderPage(); }
    if (e.target.closest('[data-back]')) { state.folder = null; return renderPage(); }
    if (e.target.closest('[data-settings]')) openSettings();
});

// ---------------------------------------------------------------- banner

function renderBanner() {
    const banner = $('banner');
    const megabytes = Math.round(totalSize / 1e6);
    if (speaker.state === 'downloading' && banner.querySelector('progress')) {
        banner.querySelector('progress').value = speaker.progress;
        return;
    }
    switch (speaker.state) {
        case 'ready':
            banner.hidden = true;
            return;
        case 'missing':
            banner.innerHTML = `<span>Better voice, ${megabytes} MB</span><button data-download>Download</button>`;
            break;
        case 'downloading':
            banner.innerHTML = `<span>Downloading voice</span><progress max="1" value="${speaker.progress}"></progress>`;
            break;
        case 'loading':
            banner.innerHTML = '<span>Preparing voice</span><span>⏳</span>';
            break;
        default:
            banner.innerHTML = `<span>${esc(speaker.message)}</span><button data-download>Retry</button>`;
    }
    banner.hidden = false;
}
$('banner').addEventListener('click', (e) => {
    if (e.target.closest('[data-download]')) speaker.download();
});

// ---------------------------------------------------------------- settings

function openSettings() {
    renderSettings();
    $('settings').showModal();
}

function seg(name, options) {
    return `<div class="seg" data-seg="${name}">` +
        options.map(([title, value]) => `<button data-value="${value}" class="${String(settings[name]) === String(value) ? 'on' : ''}">${esc(title)}</button>`).join('') +
        '</div>';
}

function renderSettings() {
    $('settings-body').innerHTML = `
        <div class="group"><h3>Language</h3>${seg('language', Object.entries(LANGS).map(([k, v]) => [v.title, k]))}</div>
        <div class="group"><h3>Grammar</h3>
            <label class="switch">Word forms<input type="checkbox" id="grammar" ${settings.grammar ? 'checked' : ''}></label>
            ${settings.grammar ? seg('child', [['Boy', 'boy'], ['Girl', 'girl']]) : ''}
            <p>${settings.grammar
                ? 'Picks the right form of each word, like "chcem vodu". Long press a word in the sentence to change its form.'
                : 'Every word is said as it is on the card.'}</p>
        </div>
        <div class="group"><h3>Voice</h3><div class="list">${VOICES.map((v) =>
            `<button data-voice="${v}" class="${settings.voice === v ? 'on' : ''}"><span>${voiceTitle(v)}</span><span>${settings.voice === v ? '✓' : ''}</span></button>`).join('')}</div></div>
        <div class="group"><h3>Speed</h3><div class="range"><input type="range" id="speed" min="0.8" max="1.3" step="0.05" value="${settings.speed}"><span id="speed-val">${Number(settings.speed).toFixed(2)}</span></div></div>
        <div class="group"><h3>Engine</h3>${seg('engine', [['CPU', 'cpu'], ['GPU', 'gpu']])}<p>GPU is faster but experimental, it needs https. The page reloads when you change it.</p></div>
        <div class="group"><h3>Quality</h3>${seg('steps', STEPS.map(([t, v]) => [t, v]))}<p>Fewer steps are faster but sound rougher.</p></div>`;
}

$('settings-body').addEventListener('click', (e) => {
    const option = e.target.closest('[data-seg] button');
    if (option) {
        const name = option.parentElement.dataset.seg;
        settings[name] = name === 'steps' ? Number(option.dataset.value) : option.dataset.value;
        saveSettings();
        if (name === 'engine') return location.reload();
        if (name === 'language') {
            // Hand-picked forms are text in the old language.
            state.sentence.forEach((item) => delete item.override);
            speaker.stop();
        }
        renderSettings();
        renderAll();
        return;
    }
    const voice = e.target.closest('[data-voice]');
    if (voice) {
        settings.voice = voice.dataset.voice;
        saveSettings();
        renderSettings();
        say(LANGS[settings.language].sample);
    }
});
$('settings-body').addEventListener('change', (e) => {
    if (e.target.id === 'grammar') {
        settings.grammar = e.target.checked;
        saveSettings();
        renderSettings();
        renderAll();
    } else if (e.target.id === 'speed') {
        settings.speed = Number(e.target.value);
        saveSettings();
        say(LANGS[settings.language].sample);
    }
});
$('settings-body').addEventListener('input', (e) => {
    if (e.target.id === 'speed') $('speed-val').textContent = Number(e.target.value).toFixed(2);
});

for (const dialog of document.querySelectorAll('dialog')) {
    dialog.addEventListener('click', (e) => {
        if (e.target === dialog || e.target.closest('[data-close]')) dialog.close();
    });
}

// ---------------------------------------------------------------- start

function renderAll() {
    renderStrip();
    renderPage();
    renderBanner();
    renderSpeak();
}

// iOS plays audio later only if a tap started some audio first.
document.addEventListener('click', () => speaker.unlock(), true);

async function boot() {
    try {
        const [structureData, sk, cs] = await Promise.all(['structure', 'words.sk', 'words.cs'].map(async (name) => {
            const response = await fetch(`data/${name}.json`);
            if (!response.ok) throw new Error(`${name}.json: ${response.status}`);
            return response.json();
        }));
        structure = structureData;
        wordsByLang = { sk, cs };
        const required = [...structure.core, ...structure.folders.flatMap((f) => [`folder.${f.id}`, ...f.words])];
        const missing = Object.entries(wordsByLang).flatMap(([lang, w]) => required.filter((id) => !w[id]).map((id) => `${lang}:${id}`));
        if (missing.length) throw new Error(`missing words ${missing.join(', ')}`);
    } catch (error) {
        $('page').textContent = `Could not load the words: ${error.message}`;
        return;
    }
    renderAll();
    speaker.init();
}
window.addEventListener('error', (e) => log('window error', e.message, e.filename, e.lineno));
window.addEventListener('unhandledrejection', (e) => log('unhandled rejection', e.reason instanceof Error ? e.reason : String(e.reason)));
log('boot', navigator.userAgent, 'secure:', window.isSecureContext, 'isolated:', window.crossOriginIsolated);
boot();
