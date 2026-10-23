import * as store from './store.js';
import { log } from './log.js';
import { FILES, totalSize } from './model.js';

const SYSTEM_VOICE = { sk: 'sk-SK', cs: 'cs-CZ' };

/** Half a second of silence. Playing it inside a tap lets iOS play the real audio later. */
function silentWavURL() {
    const samples = 8000, rate = 16000;
    const buffer = new ArrayBuffer(44 + samples * 2);
    const view = new DataView(buffer);
    const text = (offset, s) => [...s].forEach((c, i) => view.setUint8(offset + i, c.charCodeAt(0)));
    text(0, 'RIFF'); view.setUint32(4, 36 + samples * 2, true); text(8, 'WAVE'); text(12, 'fmt ');
    view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true);
    view.setUint32(24, rate, true); view.setUint32(28, rate * 2, true); view.setUint16(32, 2, true);
    view.setUint16(34, 16, true); text(36, 'data'); view.setUint32(40, samples * 2, true);
    return URL.createObjectURL(new Blob([buffer], { type: 'audio/wav' }));
}

async function fetchWithProgress(url, size, onProgress) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`${url}: ${response.status}`);
    const out = new Uint8Array(size);
    const reader = response.body.getReader();
    let received = 0;
    for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        out.set(value, received);
        received += value.length;
        onProgress(received);
    }
    if (received !== size) throw new Error(`${url}: got ${received} bytes, expected ${size}`);
    return out.buffer;
}

/**
 * Speaks words and sentences. Uses Supertonic (in a worker) once its model is downloaded and
 * loaded, the phone's own voice until then or if anything fails.
 * `state`: missing, downloading, loading, ready, failed.
 */
export class Speaker {
    state = 'missing';
    progress = 0;
    message = '';
    thinking = false;

    #onChange;
    #worker = null;
    #calls = new Map();
    #nextCall = 0;
    #audio = new Audio();
    #unlocked = false;
    #silent = null;
    #cache = new Map();
    #request = 0;
    #busy = false;
    #queued = null;

    constructor(onChange) {
        this.#onChange = onChange;
    }

    #set(state, message = '') {
        log('state', state, message);
        this.state = state;
        this.message = message;
        this.#onChange();
    }

    async init() {
        try { await navigator.storage?.persist?.(); } catch { /* best effort */ }
        const stored = await store.hasAll(FILES).catch(() => false);
        if (stored) await this.#load(null);
        else this.#set('missing');
    }

    async download() {
        if (this.state === 'downloading' || this.state === 'loading') return;
        this.progress = 0;
        this.#set('downloading');
        const kept = {}; // files IndexedDB refused, handed straight to the worker
        let done = 0;
        try {
            for (const file of FILES) {
                if (await store.has(file.path, file.size).catch(() => false)) { done += file.size; continue; }
                const base = done;
                const buffer = await fetchWithProgress(`model/${file.path}`, file.size, (n) => {
                    this.progress = (base + n) / totalSize;
                    this.#onChange();
                });
                done += file.size;
                try { await store.put(file.path, buffer, file.size); } catch (error) { log('store.put failed', file.path, error); kept[file.path] = buffer; }
            }
        } catch (error) {
            console.error(error);
            log('download failed', error);
            return this.#set('failed', 'Download failed. Check the connection and try again.');
        }
        await this.#load(Object.keys(kept).length ? kept : null);
    }

    #call(message, transfer = []) {
        const id = ++this.#nextCall;
        return new Promise((resolve, reject) => {
            this.#calls.set(id, { resolve, reject });
            this.#worker.postMessage({ ...message, id }, transfer);
        });
    }

    async #load(files) {
        this.#set('loading');
        try {
            this.#worker ??= new Worker(new URL('./tts.worker.js', import.meta.url), { type: 'module' });
            this.#worker.onmessage = ({ data }) => {
                const call = this.#calls.get(data.id);
                this.#calls.delete(data.id);
                if (data.ok) call?.resolve(data); else call?.reject(new Error(data.error));
            };
            this.#worker.onerror = (event) => { console.error('worker', event.message); log('worker error', event.message, event.filename, event.lineno); };
            await this.#call(
                { type: 'load', vendorURL: new URL('../vendor/', import.meta.url).href, files },
                files ? Object.values(files) : [],
            );
            this.#set('ready');
        } catch (error) {
            console.error(error);
            log('load failed', error);
            this.#set('failed', `Voice could not load: ${error.message}`);
        }
    }

    /** Call inside a tap or click. iOS only plays audio later if it was started once by a tap. */
    unlock() {
        if (this.#unlocked) return;
        this.#silent ??= silentWavURL();
        this.#audio.src = this.#silent;
        this.#audio.play().then(() => { this.#unlocked = true; }).catch(() => {});
    }

    speak(text, language, voice, { speed = 1, steps = 8 } = {}) {
        text = text.trim();
        if (!text) return;
        this.stop();
        const id = ++this.#request;

        if (this.state !== 'ready') return this.#speakWithSystem(text, language);
        const key = `${language}|${voice}|${speed}|${steps}|${text}`;
        if (this.#cache.has(key)) return this.#play(this.#cache.get(key));

        this.thinking = true;
        this.#onChange();
        this.#run({ id, key, text, language, voice, speed, steps });
    }

    /** One sentence at a time. If taps come faster, only the newest one waits. */
    async #run(job) {
        if (this.#busy) { this.#queued = job; return; }
        this.#busy = true;
        try {
            const { wav } = await this.#call({
                type: 'speak', text: job.text, lang: job.language, voice: job.voice, speed: job.speed, steps: job.steps,
            });
            const url = URL.createObjectURL(new Blob([wav], { type: 'audio/wav' }));
            this.#cache.set(job.key, url);
            if (job.id === this.#request) { this.thinking = false; this.#onChange(); this.#play(url); }
        } catch (error) {
            console.error(error);
            log('speak failed', error);
            if (job.id === this.#request) { this.thinking = false; this.#onChange(); this.#speakWithSystem(job.text, job.language); }
        } finally {
            this.#busy = false;
            const next = this.#queued;
            this.#queued = null;
            if (next && next.id === this.#request) this.#run(next);
        }
    }

    stop() {
        this.#audio.pause();
        speechSynthesis?.cancel();
        this.#queued = null;
        if (this.thinking) { this.thinking = false; this.#onChange(); }
    }

    #play(url) {
        this.#audio.src = url;
        this.#audio.play().catch((error) => { console.error('play', error); log('play failed', error); });
    }

    #speakWithSystem(text, language) {
        if (!('speechSynthesis' in window)) return;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = SYSTEM_VOICE[language] ?? language;
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }
}
