#!/usr/bin/env python3
"""Serve the collaborative timeline editor and persist its register safely."""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import pathlib
import sys
import tempfile
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402
from serve import Handler as RangeHandler, Server, RANGE, SINK, _Slice  # noqa: E402
from timeline import (MusicalGrid, compile_timeline, load_project,  # noqa: E402
                      validate_timeline, _resolve)

STATE = {"project": None, "project_dir": None, "timeline_path": None,
         "beatmap_path": None, "audio_path": None}
MAX_BODY = 2 * 1024 * 1024


def _json(handler, data, status=200):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class TimelineHandler(RangeHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        if path == "/api/project":
            project = {k: v for k, v in STATE["project"].items()
                       if not k.startswith("_") and k != "sources"}
            _json(self, {"project": project,
                         "timeline": load(STATE["timeline_path"]),
                         "beatmap": load(STATE["beatmap_path"]),
                         "waveforms": self._waveforms(),
                         "hasAudio": bool(STATE["audio_path"] and STATE["audio_path"].exists())})
            return
        if path == "/api/audio":
            self._audio()
            return
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/timeline/")
            self.end_headers()
            return
        super().do_GET()

    def _waveforms(self):
        cfg = STATE["project"].get("referenceWaveforms")
        if not cfg:
            return {"schemaVersion": 1, "rate": 0, "tracks": []}
        path = _resolve(STATE["project_dir"], cfg["output"])
        return load(path) if path.exists() else {"schemaVersion": 1, "rate": 0, "tracks": []}

    def do_PUT(self):
        if urllib.parse.urlsplit(self.path).path != "/api/timeline":
            self.send_error(404)
            return
        size = int(self.headers.get("Content-Length") or 0)
        if size <= 0 or size > MAX_BODY:
            _json(self, {"ok": False, "errors": ["invalid request size"]}, 413)
            return
        try:
            timeline = json.loads(self.rfile.read(size))
            grid = MusicalGrid(load(STATE["beatmap_path"]))
            errors = validate_timeline(timeline, grid)
            if errors:
                _json(self, {"ok": False, "errors": errors}, 400)
                return
            target = STATE["timeline_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp",
                                             dir=target.parent)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    json.dump(timeline, fh, indent=2, ensure_ascii=False)
                    fh.write("\n")
                os.replace(temp_name, target)
            finally:
                if os.path.exists(temp_name):
                    os.unlink(temp_name)
            compiled = compile_timeline(STATE["project"], STATE["project_dir"])
            _json(self, {"ok": True,
                         "durationFrames": compiled["timing"]["durationFrames"]})
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            _json(self, {"ok": False, "errors": [str(exc)]}, 400)

    def _audio(self):
        audio = STATE["audio_path"]
        if not audio or not audio.is_file():
            self.send_error(404)
            return
        size = audio.stat().st_size
        start, end, status = 0, size - 1, 200
        rng = self.headers.get("Range")
        if rng:
            match = RANGE.match(rng.strip())
            if not match:
                self.send_error(416)
                return
            start = int(match.group(1) or 0)
            end = min(int(match.group(2) or size - 1), size - 1)
            status = 206
        if start > end:
            self.send_error(416)
            return
        fh = open(audio, "rb")
        fh.seek(start)
        self.send_response(status)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Accept-Ranges", "bytes")
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        try:
            self.copyfile(_Slice(fh, end - start + 1), self.wfile)
        finally:
            fh.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", type=pathlib.Path, required=True)
    ap.add_argument("--port", type=int, default=8760)
    ap.add_argument("--sink",
                    help="write POSTed /frame bodies to this file, or '-' for stdout")
    args = ap.parse_args()
    project, project_dir = load_project(args.project)
    STATE.update({
        "project": project,
        "project_dir": project_dir,
        "timeline_path": _resolve(project_dir, project["timeline"]),
        "beatmap_path": _resolve(project_dir, project["timing"]["beatmap"]),
        "audio_path": _resolve(project_dir, project["sources"]["audio"]),
    })
    if not STATE["beatmap_path"].exists():
        raise SystemExit("beatmap missing; run tools/timeline.py sync first")
    # In render-sink mode stdout is the binary frame stream into ffmpeg. Keep
    # the register compiler's friendly "wrote ..." message off that stream.
    if args.sink:
        with contextlib.redirect_stdout(sys.stderr):
            compile_timeline(project, project_dir)
        SINK["fh"] = sys.stdout.buffer if args.sink == "-" else open(args.sink, "wb")
    else:
        compile_timeline(project, project_dir)
    with Server(("127.0.0.1", args.port), TimelineHandler) as httpd:
        if not args.sink:
            print(f"timeline editor: http://127.0.0.1:{args.port}/timeline/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
