#!/usr/bin/env python3
"""
A small static server that can actually serve audio.

    python3 tools/serve.py [port]

Python's SimpleHTTPRequestHandler does not implement HTTP Range, so a browser
cannot seek inside a 62MB WAV — it refetches from zero, stalls, and aborts the
old request, which surfaces as a wall of BrokenPipeError. This adds Range
support (so scrubbing works), swallows client disconnects, and keeps the log
to one line per request.
"""
from __future__ import annotations

import os
import re
import sys
import http.server
import socketserver

RANGE = re.compile(r"bytes=(\d*)-(\d*)")

# Frames posted by the page land here, in arrival order. The page awaits each
# POST before rendering the next frame, so this stays strictly ordered without
# any sequencing of its own.
SINK = {"fh": None, "count": 0, "lock": __import__("threading").Lock()}


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):                       # one quiet line
        if "404" in (args[1] if len(args) > 1 else ""):
            return
        sys.stderr.write("  %s\n" % (fmt % args))

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            self.close_connection = True                     # the browser moved on

    def copyfile(self, src, dst):
        try:
            super().copyfile(src, dst)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def do_POST(self):
        """Accept a rendered frame from the page.

        Screenshotting through the devtools protocol costs ~46ms a frame,
        because it captures and crops the whole page and hands the result back
        base64-encoded. The page can instead encode its own canvas and POST the
        bytes straight here — same origin, so no preflight, and binary all the
        way. See tools/capture_bench.py for the measurements.
        """
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        if SINK["fh"] is not None and body:
            with SINK["lock"]:
                SINK["fh"].write(body)
                SINK["count"] += 1
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_head(self):
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        m = RANGE.match(rng.strip())
        if not m:
            return super().send_head()
        a, b = m.group(1), m.group(2)
        start = int(a) if a else 0
        end = int(b) if b else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416)
            return None
        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        return _Slice(f, end - start + 1)


class _Slice:
    """Wraps a file so copyfile stops at the end of the requested range."""

    def __init__(self, f, n):
        self.f, self.n = f, n

    def read(self, k=-1):
        if self.n <= 0:
            return b""
        if k is None or k < 0:
            k = self.n
        data = self.f.read(min(k, self.n))
        self.n -= len(data)
        return data

    def close(self):
        self.f.close()


class Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8747
    # `--sink -` sends posted frames to stdout, so the caller can pipe them
    # straight into ffmpeg without them ever passing through the debugger.
    if "--sink" in sys.argv:
        where = sys.argv[sys.argv.index("--sink") + 1]
        SINK["fh"] = sys.stdout.buffer if where == "-" else open(where, "wb")
    with Server(("127.0.0.1", port), Handler) as httpd:
        if SINK["fh"] is not sys.stdout.buffer:
            print(f"  serving on http://127.0.0.1:{port}/world/   (ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped")
