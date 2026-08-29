#!/usr/bin/env python3
"""
Take Flow downloads and attach them to shots.

    python3 tools/ingest.py --status              # what's shot, what isn't
    python3 tools/ingest.py --list                # new files in clips/inbox
    python3 tools/ingest.py --auto                # file up by setup name in filename
    python3 tools/ingest.py --assign s012 --file clips/raw/chorus_wide_01.mp4 --in 1.4

Flow names downloads unhelpfully, so the workflow is: download into
clips/inbox/, run --list to see them with durations, rename them to the
setup name (or pass --auto if you named them in Flow), then --auto files
them into clips/raw/ and assigns them to every shot using that setup.

--in sets the in-point within the source clip. Use it to pick the best
2 seconds out of an 8-second generation.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, run, save  # noqa: E402

VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}


def duration(p: pathlib.Path) -> float:
    try:
        return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)]).stdout.strip())
    except Exception:
        return 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--auto", action="store_true")
    ap.add_argument("--assign", metavar="SHOT_OR_SETUP")
    ap.add_argument("--file", type=pathlib.Path)
    ap.add_argument("--in", dest="in_sec", type=float, default=0.0)
    ap.add_argument("--speed", type=float, default=1.0)
    a = ap.parse_args()

    path = ROOT / "shots" / "shotlist.json"
    sl = load(path)
    shots = sl["shots"]
    inbox, raw = ROOT / "clips" / "inbox", ROOT / "clips" / "raw"
    inbox.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)

    if a.list:
        files = sorted(p for p in inbox.iterdir() if p.suffix.lower() in VIDEO)
        if not files:
            print(f"nothing in {inbox}")
        for p in files:
            print(f"  {duration(p):5.1f}s  {p.name}")
        return

    def attach(targets, src: pathlib.Path, in_sec, speed):
        rel = str(src.relative_to(ROOT)) if str(src).startswith(str(ROOT)) else str(src)
        for s in targets:
            s["clip"] = {"file": rel, "in_sec": in_sec, "speed": speed}
        return len(targets)

    if a.auto:
        setups = {s["setup"] for s in shots if s.get("setup")}
        moved = 0
        for p in sorted(inbox.iterdir()):
            if p.suffix.lower() not in VIDEO:
                continue
            hit = next((k for k in sorted(setups, key=len, reverse=True) if k and k in p.stem), None)
            hit = hit or next((s["id"] for s in shots if s["id"] in p.stem), None)
            if not hit:
                print(f"  ?  {p.name} — no setup or shot id in the filename, skipped")
                continue
            dest = raw / p.name
            shutil.move(str(p), dest)
            n = attach([s for s in shots if s.get("setup") == hit or s["id"] == hit], dest, 0.0, 1.0)
            longest = max((s["dur_sec"] for s in shots
                           if s.get("setup") == hit or s["id"] == hit), default=0)
            d = duration(dest)
            flag = "  !! shorter than the longest cut using it" if d < longest - 0.05 else ""
            print(f"  ok {p.name} → {hit}  ({n} shot(s), {d:.1f}s source){flag}")
            moved += 1
        if moved:
            save(path, sl)
        return

    if a.assign:
        if not a.file or not a.file.exists():
            raise SystemExit("--assign needs an existing --file")
        targets = [s for s in shots if s["id"] == a.assign or s.get("setup") == a.assign]
        if not targets:
            raise SystemExit(f"no shot or setup called {a.assign}")
        n = attach(targets, a.file.resolve(), a.in_sec, a.speed)
        save(path, sl)
        print(f"  {a.assign}: {n} shot(s) → {a.file.name} @ in={a.in_sec}s speed={a.speed}")
        return

    # default: status
    done = [s for s in shots if (s.get("clip") or {}).get("file")]
    by_setup = {}
    for s in shots:
        by_setup.setdefault(s.get("setup") or s["id"], []).append(s)
    print(f"{len(done)}/{len(shots)} cuts have footage"
          f"   ({sum(s['dur_sec'] for s in done):.0f}s of {sl['duration_sec']:.0f}s)\n")
    for key, group in by_setup.items():
        f = (group[0].get("clip") or {}).get("file")
        mark = "●" if f else "○"
        need = max(s["dur_sec"] for s in group)
        print(f"  {mark} {key:24s} {len(group):2d} cut(s)  need ≥{need:4.1f}s"
              + (f"   {pathlib.Path(f).name}" if f else ""))


if __name__ == "__main__":
    main()
