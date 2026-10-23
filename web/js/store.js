// The model files live in IndexedDB, so they are downloaded once. IndexedDB works on plain http
// (the Cache API does not), which matters while this runs from a LAN address.
const DB_NAME = 'logo-model';
const STORE = 'files';

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

/** Stores the file, then a small marker with its size so `has` never has to read the file. */
export async function put(path, buffer, size) {
    await run('readwrite', (s) => s.put(buffer, path));
    await run('readwrite', (s) => s.put(size, `size:${path}`));
}

export function get(path) {
    return run('readonly', (s) => s.get(path));
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
