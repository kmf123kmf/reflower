"""Static server for the tests, plus a slow endpoint for real-time headless runs.

Run from anywhere:  python tests/serve.py [port]      (default 8765, serves the repo root)

GET /__hold?ms=6000 answers after the given delay (default 6000 ms). tests/ui.html?...&hold=/__hold
loads it, so `chrome --headless --dump-dom` (without --virtual-time-budget) waits that long in real
time, and checks that need rendered frames (requestAnimationFrame, ResizeObserver) can run.
"""
import functools
import http.server
import os
import sys
import time
from urllib.parse import parse_qs, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/__hold":
            time.sleep(int(parse_qs(url.query).get("ms", ["6000"])[0]) / 1000)
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # always test the current index.html
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Handler, directory=ROOT))
    print(f"serving {ROOT} on http://127.0.0.1:{port}")
    server.serve_forever()
