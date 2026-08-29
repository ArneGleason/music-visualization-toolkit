#!/usr/bin/env python3
"""
Expand the shot list into paste-ready Veo prompts.

    python3 tools/prompts.py

Reads shots/shotlist.json + shots/style.md and writes prompts/prompts.md,
grouped by SETUP rather than by shot -- because several cuts share one
generated clip, you generate once per setup, not once per cut.

Every prompt gets the LOCK block from style.md appended verbatim. Identical
wording on every generation is the cheapest consistency mechanism there is;
do not paraphrase it between shots.
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402


def read_style(path: pathlib.Path):
    """style.md: prose for humans, plus a fenced ```lock block appended to every prompt."""
    if not path.exists():
        return "", {}
    text = path.read_text()
    lock = ""
    m = re.search(r"```lock\s*\n(.*?)```", text, re.S)
    if m:
        lock = m.group(1).strip()
    refs = dict(re.findall(r"^\s*-\s*ref\s+([\w-]+)\s*:\s*(.+)$", text, re.M))
    return lock, refs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "prompts" / "prompts.md")
    a = ap.parse_args()

    sl = load(ROOT / "shots" / "shotlist.json")
    lock, refs = read_style(ROOT / "shots" / "style.md")

    groups = collections.OrderedDict()
    for s in sl["shots"]:
        key = s.get("setup") or s["id"]
        groups.setdefault(key, []).append(s)

    out = ["# Veo prompts", "",
           f"{len(groups)} setups covering {len(sl['shots'])} cuts. "
           "Generate one clip per setup (a couple of takes each for the ones you'll return to). "
           "Longest cut using each setup is noted -- generate at least that long.", ""]
    if refs:
        out += ["**Reference images** (attach via Ingredients-to-Video every time):", ""]
        out += [f"- `{k}` — {v}" for k, v in refs.items()] + [""]
    out.append("---\n")

    for key, shots in groups.items():
        longest = max(s["dur_sec"] for s in shots)
        kinds = {s["type"] for s in shots}
        secs = sorted({s["section"] for s in shots})
        body = next((s["prompt"] for s in shots if s.get("prompt")), "") or \
               next((s["description"] for s in shots if s.get("description")), "") or \
               "TODO — write this shot"
        lyric = next((s["lyric"] for s in shots if s.get("lyric")), "")

        out.append(f"## `{key}`  ·  {', '.join(sorted(kinds))}")
        out.append("")
        out.append(f"Used by {len(shots)} cut(s): " +
                   ", ".join(f"{s['id']} ({s['dur_sec']:.1f}s)" for s in shots))
        out.append(f"Sections: {', '.join(secs)} · **generate ≥ {longest:.1f}s**")
        if lyric:
            out.append(f"Lyric: *{lyric}*")
        out += ["", "```", body.strip()]
        if lock:
            out += ["", lock]
        out += ["```", ""]

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(out))
    todo = sum(1 for k, v in groups.items()
               if not any(s.get("prompt") or s.get("description") for s in v))
    print(f"wrote {a.out}  —  {len(groups)} setups"
          + (f", {todo} still TODO" if todo else ""))


if __name__ == "__main__":
    main()
