// Sends a line to the server log (serve.py prints it), so problems on the phone can be read on the Pi.
export function log(...parts) {
    const text = parts
        .map((p) => (p instanceof Error ? `${p.name}: ${p.message}` : typeof p === 'string' ? p : JSON.stringify(p)))
        .join(' ');
    try { fetch('/log', { method: 'POST', body: text, keepalive: true }).catch(() => {}); } catch { /* ignore */ }
}
