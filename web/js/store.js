// The model files live in IndexedDB, so they are downloaded once. IndexedDB works on plain http
// (the Cache API does not), which matters while this runs from a LAN address.
// Safari on iPhone loses the database connection when one huge value is written, so files are
// kept as 8 MB parts.
const DB_NAME = 'logo-model-2';
const STORE = 'files';
const PART = 8 * 1024 * 1024;

function open() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, 1);
        request.onupgradeneeded = () => request.result.createObjectStore(STORE);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function run(mode, action) {
    const db = await open();
    try {
        return await new Promise((resolve, reject) => {
            const tx = db.transaction(STORE, mode);
            const result = action(tx.objectStore(STORE));
            tx.oncomplete = () => resolve(result.result);
            tx.onerror = () => reject(tx.error);
            tx.onabort = () => reject(tx.error ?? new Error('aborted'));
        });
    } finally {
        db.close();
    }
}

/** Stores the file in parts, then a small marker with its size so `has` never reads the file. */
export async function put(path, buffer, size) {
    const bytes = new Uint8Array(buffer);
    for (let part = 0, offset = 0; offset < size; part++, offset += PART) {
        const slice = bytes.slice(offset, offset + PART).buffer;
        await run('readwrite', (s) => s.put(slice, `${path}#${part}`));
    }
    await run('readwrite', (s) => s.put(size, `size:${path}`));
}

export async function get(path, size) {
    const out = new Uint8Array(size);
    for (let part = 0, offset = 0; offset < size; part++, offset += PART) {
        const slice = await run('readonly', (s) => s.get(`${path}#${part}`));
        if (!slice) throw new Error(`Missing ${path} part ${part}`);
        out.set(new Uint8Array(slice), offset);
    }
    return out.buffer;
}

export async function has(path, size) {
    return (await run('readonly', (s) => s.get(`size:${path}`))) === size;
}

export async function hasAll(files) {
    for (const f of files) {
        if (!(await has(f.path, f.size))) return false;
    }
    return true;
}

/** Throws everything away, for when what is stored cannot be read. */
export function clear() {
    return new Promise((resolve) => {
        const request = indexedDB.deleteDatabase(DB_NAME);
        request.onsuccess = request.onerror = request.onblocked = () => resolve();
    });
}
