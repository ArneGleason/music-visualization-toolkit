#!/usr/bin/env python3
"""
Expand the shot list into paste-ready image and video prompts.

    python3 tools/prompts.py

Reads shots/shotlist.json + shots/style.md and writes prompts/prompts.md,
grouped by SETUP rather than by shot -- because several cuts share one
generated clip, you generate once per setup, not once per cut.

Each setup gets two prompts when the shot list carries a `still` text:
  Still  -- "Film still." + the frame description, for the storyboard image
            (no camera-motion words: they get drawn as captions)
  Video  -- frame + motion, for Frames-to-Video from the approved still

Cast placeholders ({{astronaut}}, {{suit}}, {{merfolk}}, ...) are replaced
verbatim from the `- cast name: text` lines in style.md, and every prompt
gets the LOCK block from style.md appended verbatim. Identical wording on
every generation is the cheapest consistency mechanism there is; do not
paraphrase it between shots.
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402

PLACEHOLDER = re.compile(r"\{\{\s*([\w-]+)\s*\}\}")


def read_style(path: pathlib.Path):
    """style.md: prose for humans, plus a fenced ```lock block appended to
    every prompt, `- ref name: path` lines, and `- cast name: text` lines."""
    if not path.exists():
        return "", {}, {}
    text = path.read_text(encoding="utf-8")
    lock = ""
    m = re.search(r"```lock\s*\n(.*?)```", text, re.S)
    if m:
        lock = m.group(1).strip()
    refs = dict(re.findall(r"^\s*-\s*ref\s+([\w-]+)\s*:\s*(.+)$", text, re.M))
    cast = {k: v.strip() for k, v in
            re.findall(r"^\s*-\s*cast\s+([\w-]+)\s*:\s*(.+)$", text, re.M)}
    return lock, refs, cast


def expand(text: str, cast: dict, missing: set) -> str:
    def sub(m):
        key = m.group(1)
        if key in cast:
            return cast[key]
        missing.add(key)
        return m.group(0)
    return PLACEHOLDER.sub(sub, text)


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "prompts" / "prompts.md")
    a = ap.parse_args()

    sl = load(ROOT / "shots" / "shotlist.json")
    lock, refs, cast = read_style(ROOT / "shots" / "style.md")
    missing: set = set()

    groups = collections.OrderedDict()
    for s in sl["shots"]:
        key = s.get("setup") or s["id"]
        groups.setdefault(key, []).append(s)

    out = ["# Prompts", "",
           f"{len(groups)} setups covering {len(sl['shots'])} cuts. "
           "Generate the still first (free), approve it, then the video from it "
           "(Frames-to-Video, start frame = the still). Longest cut using each "
           "setup is noted -- generate at least that long.", ""]
    if cast:
        out += ["**Cast lines** (substituted verbatim wherever a prompt says `{{name}}`):", ""]
        out += [f"- `{k}` — {v}" for k, v in cast.items()] + [""]
    if refs:
        out += ["**Reference images** (attach the matching ones every time):", ""]
        out += [f"- `{k}` — {v}" for k, v in refs.items()] + [""]
    out.append("---\n")

    def block(title, body):
        lines = [f"**{title}**", "", "```", body.strip()]
        if lock:
            lines += ["", lock]
        return lines + ["```", ""]

    for key, shots in groups.items():
        longest = max(s["dur_sec"] for s in shots)
        kinds = {s["type"] for s in shots}
        secs = sorted({s["section"] for s in shots})
        body = next((s["prompt"] for s in shots if s.get("prompt")), "") or \
               next((s["description"] for s in shots if s.get("description")), "") or \
               "TODO — write this shot"
        still = next((s["still"] for s in shots if s.get("still")), "")
        lyric = next((s["lyric"] for s in shots if s.get("lyric")), "")
        slate = next((s["description"] for s in shots if s.get("description")), "")

        out.append(f"## `{key}`  ·  {', '.join(sorted(kinds))}" + (f"  ·  {slate}" if slate else ""))
        out.append("")
        out.append(f"Used by {len(shots)} cut(s): " +
                   ", ".join(f"{s['id']} ({s['dur_sec']:.1f}s)" for s in shots))
        out.append(f"Sections: {', '.join(secs)} · **generate ≥ {longest:.1f}s**")
        if lyric:
            out.append(f"Lyric: *{lyric}*")
        out.append("")
        if still:
            out += block("Still", "Film still. " + expand(still, cast, missing))
        out += block("Video", expand(body, cast, missing))

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(out), encoding="utf-8")
    todo = sum(1 for k, v in groups.items()
               if not any(s.get("prompt") or s.get("description") for s in v))
    print(f"wrote {a.out}  —  {len(groups)} setups"
          + (f", {todo} still TODO" if todo else ""))
    if missing:
        print(f"  !! placeholders with no cast line in style.md: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
