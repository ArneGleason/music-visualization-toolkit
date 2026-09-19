"""Local constant-frame-rate video review with shared frame notes."""
import argparse
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import subprocess
import threading
from urllib.parse import urlparse, parse_qs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--master-start", type=int, default=1)
    parser.add_argument("--port", type=int, default=8767)
    parser.add_argument("--state", type=Path, help="JSON pointer to current video and master_start")
    args = parser.parse_args()
    @lru_cache(maxsize=16)
    def inspect(path, stamp):
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate,avg_frame_rate,nb_frames",
            "-of", "json", path]))["streams"][0]
        num, den = map(int, probe["r_frame_rate"].split("/"))
        if probe["r_frame_rate"] != probe["avg_frame_rate"]:
            raise ValueError("Use a constant-frame-rate export.")
        return num / den, int(probe["nb_frames"])

    revisions = {}

    def current():
        state = json.loads(args.state.read_text(encoding="utf-8")) if args.state and args.state.exists() else {}
        video = Path(state.get("video", args.video)).resolve()
        stamp = video.stat().st_mtime_ns
        fps, count = inspect(str(video), stamp)
        result = video, fps, count, int(state.get("master_start", args.master_start)), str(stamp)
        revisions[str(stamp)] = result
        return result

    ui = Path(__file__).resolve().parent.parent / "review"
    lock = threading.Lock()
    args.notes.parent.mkdir(parents=True, exist_ok=True)

    def read_notes():
        return json.loads(args.notes.read_text(encoding="utf-8")) if args.notes.exists() else []

    @lru_cache(maxsize=256)
    def still(path, fps, frame, revision):
        # Accurate input seek decodes from the preceding keyframe to this CFR frame.
        return subprocess.check_output([
            "ffmpeg", "-v", "error", "-ss", f"{(frame-1)/fps:.9f}",
            "-i", path, "-frames:v", "1", "-vf", "scale=1280:-2",
            "-f", "image2pipe", "-vcodec", "mjpeg", "-q:v", "2", "-"],
            timeout=30)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, data, kind="application/json", status=200):
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

        def do_GET(self):
            route = urlparse(self.path)
            active = current()
            requested = parse_qs(route.query).get("v", [active[-1]])[0]
            video, fps, count, master_start, revision = revisions.get(requested, active)
            if route.path == "/api":
                with lock:
                    notes = read_notes()
                self.send(json.dumps(dict(name=video.name, fps=fps, count=count,
                    masterStart=master_start, revision=revision, notes=notes)).encode())
            elif route.path == "/frame":
                try:
                    frame = int(parse_qs(route.query)["n"][0])
                    if not 1 <= frame <= count:
                        raise ValueError()
                    self.send(still(str(video), fps, frame, revision), "image/jpeg")
                except (ValueError, KeyError):
                    self.send(b"Invalid frame", "text/plain", 400)
                except subprocess.SubprocessError:
                    self.send(b"Frame decoding failed", "text/plain", 500)
            elif route.path == "/media":
                size = video.stat().st_size
                value = self.headers.get("Range", "")
                match = re.fullmatch(r"bytes=(\d+)-(\d*)", value)
                start = int(match[1]) if match else 0
                end = min(int(match[2]), size-1) if match and match[2] else size-1
                if start > end or start >= size:
                    self.send(b"", status=416)
                    return
                self.send_response(206 if match else 200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(end-start+1))
                if match:
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.end_headers()
                try:
                    with video.open("rb") as source:
                        source.seek(start)
                        remaining = end-start+1
                        while remaining:
                            chunk = source.read(min(262144, remaining))
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            remaining -= len(chunk)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass
            elif route.path in ("/", "/app.js"):
                path = ui / ("index.html" if route.path == "/" else "app.js")
                self.send(path.read_bytes(), "text/html; charset=utf-8" if route.path == "/" else "text/javascript; charset=utf-8")
            else:
                self.send(b"Not found", "text/plain", 404)

        def do_POST(self):
            video, fps, count, master_start, revision = current()
            if self.path != "/notes":
                self.send(b"", status=404)
                return
            origin = self.headers.get("Origin")
            if origin and origin != f"http://127.0.0.1:{args.port}":
                self.send(b"", status=403)
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                if not 0 < length <= 8192:
                    raise ValueError()
                item = json.loads(self.rfile.read(length))
                if item.get("revision") != revision:
                    self.send(b"Video changed; reload before saving.", "text/plain", 409)
                    return
                frame = item["frame"]
                if type(frame) is not int or not 1 <= frame <= count:
                    raise ValueError()
                note = dict(video=video.name, preview_frame=frame,
                    master_frame=master_start+frame-1,
                    master_seconds=(master_start+frame-2)/fps,
                    fps=fps, text=str(item.get("text", ""))[:2000])
                with lock:
                    notes = read_notes()
                    notes.append(note)
                    temp = args.notes.with_suffix(".tmp")
                    temp.write_text(json.dumps(notes, indent=2)+"\n", encoding="utf-8")
                    temp.replace(args.notes)
                self.send(json.dumps(notes).encode())
            except (ValueError, KeyError, TypeError):
                self.send(b"Invalid note", "text/plain", 400)

    print(f"Frame review: http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
