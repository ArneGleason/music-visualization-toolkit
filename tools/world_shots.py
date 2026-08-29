#!/usr/bin/env python3
"""
Generate the shot score for the 3D world: which world, which camera, when.

    python3 tools/world_shots.py      ->  world/shots.json

Same principle as shotplan.py — the edit is data, the render is derived — but
the units are worlds and cameras instead of Veo prompts.

Cut rules per section live in world/plan.json:

    world       the world this section lives in
    worlds      OR a list to alternate between, one per cut
    cams        camera presets to cycle through
    cut_on      "line"  cut on every lyric line (the song edits itself)
                "bar":N every N bars
                "beat":N every N beats
    hold        explicit bar.beat positions to force a cut at

The recap section uses cut_on "line" with two worlds, because the lyric there
alternates verse-1 and verse-2 material line by line — the song is already an
A/B montage and the edit only has to follow it.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, Beatmap, load, save  # noqa: E402

DEFAULT_PLAN = {
    "min_shot_sec": 0.9,
    "sections": {
        "intro":        {"world": "record",  "cut_on": ["bar", 4],
                         "cams": ["drop", "wide", "stylus"]},
        "verse-1":      {"world": "machine", "cut_on": ["line"],
                         "cams": ["macro", "arm", "furrow", "heat", "macro", "arm", "reveal"]},
        "chorus-1":     {"world": "record",  "cut_on": ["bar", 1],
                         "cams": ["runner", "chase", "low", "wide"]},
        "verse-2":      {"world": "ocean",   "cut_on": ["line"],
                         "cams": ["floor", "enter", "descend", "descend", "deep", "deep", "vast"]},
        "chorus-2":     {"world": "record",  "cut_on": ["bar", 1],
                         "cams": ["chase", "runner", "low", "wide"]},
        "verse-3":      {"world": "lines",   "cut_on": ["bar", 2],
                         "cams": ["grid", "order", "swap", "grid"]},
        "recap":        {"worlds": ["machine", "ocean"], "cut_on": ["line"],
                         "cams": {"machine": ["macro", "heat", "reveal", "furrow"],
                                  "ocean": ["deep", "descend", "vast", "enter"]}},
        "turn":         {"world": "game",    "cut_on": ["bar", 2],
                         "cams": ["board", "toy", "board"]},
        "unravel":      {"world": "apart",   "cut_on": ["bar", 1],
                         "cams": ["fault", "bleed", "fault"]},
        "final-chorus": {"world": "record",  "cut_on": ["beat", 4],
                         "cams": ["chase", "runner", "low", "sprint", "wide", "runout"]},
    },
}


def cut_times(sec, rules, bm, lines):
    t0, t1 = sec["start_sec"], sec["end_sec"]
    kind = rules.get("cut_on", ["bar", 2])
    out = [t0]
    if kind[0] == "line":
        out += [l["sec"] for l in lines if t0 < l["sec"] < t1]
    elif kind[0] == "beat":
        n = int(kind[1])
        flat = [x for b in bm.d["bars"] for x in b["beats"] if t0 <= x < t1]
        out += flat[::n]
    else:
        n = int(kind[1])
        out += [b["sec"] for b in bm.d["bars"] if t0 <= b["sec"] < t1][::n]
    for h in rules.get("hold", []):
        out.append(bm.sec(h))
    return sorted({round(x, 4) for x in out if t0 - 1e-6 <= x < t1})


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "world" / "shots.json")
    a = ap.parse_args()

    bm = Beatmap.load()
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    lines = load(ROOT / "analysis" / "lyrics.json")["lines"]

    script_path = ROOT / "world" / "script.json"
    script = load(script_path) if script_path.exists() else {"sections": {}}
    actions = script.get("sections", {})

    plan_path = ROOT / "world" / "plan.json"
    plan = load(plan_path) if plan_path.exists() else DEFAULT_PLAN
    if not plan_path.exists():
        save(plan_path, plan)
    min_sec = plan.get("min_shot_sec", 0.9)

    shots, n = [], 0
    for sec in sections:
        rules = plan["sections"].get(sec["id"], {"world": "record", "cut_on": ["bar", 2],
                                                 "cams": ["wide"]})
        cuts = cut_times(sec, rules, bm, lines)
        edges = [(x, y) for x, y in zip(cuts, cuts[1:] + [sec["end_sec"]])
                 if y - x >= min_sec]
        worlds = rules.get("worlds") or [rules.get("world", "record")]
        cams = rules.get("cams") or ["wide"]
        # When worlds alternate, the LYRIC decides which one — not the shot
        # index. A lyric-less sliver at the head of the section would otherwise
        # steal the first slot and invert the whole montage.
        acts = actions.get(sec["id"], [])
        k = 0
        for i, (t0, t1) in enumerate(edges):
            n += 1
            covered = [l["text"] for l in lines if t0 - 1e-6 <= l["sec"] < t1]
            # In line-cut sections the LYRIC indexes both the world and the
            # action — a lyric-less sliver at the head would otherwise shift
            # the whole section's writing against the words it was written for.
            on_lines = rules.get("cut_on", ["bar", 2])[0] == "line"
            ai = k if on_lines else i
            wi = k if len(worlds) > 1 else i
            if covered:
                k += 1
            camset = cams[worlds[wi % len(worlds)]] if isinstance(cams, dict) else cams
            ci = ai if on_lines else i
            cam = rules.get("cam_overrides", {}).get(str(i), camset[ci % len(camset)])
            shots.append({
                "id": f"w{n:03d}",
                "section": sec["id"],
                "world": worlds[wi % len(worlds)],
                "cam": cam,
                "t0": round(t0, 4),
                "t1": round(t1, 4),
                "bar": bm.nearest_barbeat(t0),
                "lyric": " / ".join(covered),
                # actions map on in order; the last one repeats if the cut rate
                # gains shots, so re-planning never silently drops the writing
                "action": acts[min(ai, len(acts) - 1)] if acts else "",
            })

    save(a.out, {"duration": bm.duration,
                 "character": script.get("character", ""), "shots": shots})

    # a readable script that always matches the edit
    md = ["# Music visualization — shooting script", "",
          f"*{len(shots)} shots · {bm.duration:.1f}s · generated from world/script.json"
          " and world/plan.json — edit those, not this file*", ""]
    if script.get("character"):
        md += ["## Her", "", script["character"], ""]
    cur = None
    for s in shots:
        if s["section"] != cur:
            cur = s["section"]
            md += ["", f"## {cur.replace('-', ' ')}", ""]
        mins, secs = divmod(s["t0"], 60)
        md.append(f"**{s['id']}** · {int(mins)}:{secs:05.2f} · {s['t1']-s['t0']:.2f}s · "
                  f"`{s['world']}/{s['cam']}` · bar {s['bar']}  ")
        if s["lyric"]:
            md.append(f"> *{s['lyric']}*  ")
        md.append(f"{s['action']}" if s["action"] else "—")
        md.append("")
    (ROOT / "world" / "script.md").write_text("\n".join(md))
    print(f"  wrote {ROOT / 'world' / 'script.md'}")
    per_world = {}
    for s in shots:
        per_world[s["world"]] = per_world.get(s["world"], 0) + 1
    print(f"  {len(shots)} shots across {len(per_world)} worlds")
    for w, c in sorted(per_world.items(), key=lambda x: -x[1]):
        print(f"    {w:9s} {c:3d} shots")
    durs = [s["t1"] - s["t0"] for s in shots]
    print(f"  shortest {min(durs):.2f}s   longest {max(durs):.2f}s   "
          f"average {sum(durs)/len(durs):.2f}s")


if __name__ == "__main__":
    main()
