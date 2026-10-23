#!/usr/bin/env python3
"""Static server for the web prototype. Usage: python3 web/serve.py [port]  (default 8500)

Model files and the ONNX Runtime files never change, so they get a long cache time.
"""
import functools
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",
        ".mjs": "text/javascript",
        ".js": "text/javascript",
        ".json": "application/json",
        ".webmanifest": "application/manifest+json",
    }

    def do_POST(self):
        if self.path != "/log":
            return self.send_error(404)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(min(length, 8192)).decode("utf-8", "replace")
        print(f"CLIENT {self.client_address[0]}: {body}", flush=True)
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        path = self.path.split("?")[0]
        if path.startswith(("/model/", "/vendor/")):
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8500
    handler = functools.partial(Handler, directory=ROOT)
    server = http.server.ThreadingHTTPServer(("0.0.0.0", port), handler)
    print(f"Serving {ROOT} on http://0.0.0.0:{port}", flush=True)
    server.serve_forever()


main()
