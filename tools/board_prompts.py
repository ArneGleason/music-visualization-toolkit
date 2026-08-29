#!/usr/bin/env python3
"""
Generate the image-generation work order for the storyboard.

    ./.venv/bin/python3 tools/board_prompts.py
        -> board/prompts.json   (machine-readable: the work order)
           board/prompts.md     (the same, readable)

Reads world/shots.json (the edit, source of truth) and board/style.md (the
look), and emits every image that has to be made, in the order it has to be
made, with its exact prompt, its canonical output path, and the reference
images that must be attached to it.

CONSISTENCY MECHANISM — do not change without understanding it:

  * Reference sheets describe subjects in words, ONCE.
  * Frame prompts NEVER re-describe the character, worlds or objects. They say
    "the woman from the attached character reference" and attach the sheet.
    Re-describing a subject per frame is the largest single source of drift;
    across 77 frames it compounds into 77 different people.
  * The character sheet itself attaches refs/cover.png, which is the
    authoritative source for who she is.

LOCK PRECEDENCE — see board/style.md. Four blocks, applied mechanically:

    lock_global     every image, always, cannot be overridden
    lock_sheet      character and costume reference sheets (neutral documents)
    palette         world plates and frames: lock_studio, or the world's
                    override (only APART has one — the studio is exposed)

Everything is validated before writing: reference ids must resolve to real
sheets, output paths must be unique, and the counts must match the edit.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save  # noqa: E402

COVER = "refs/cover.png"

# Which palette lock each world uses. APART is the one exception: the set
# flats fall and the studio itself — rig, cyclorama, floor tape — is in shot.
WORLD_LOCK = {
    "record": "lock_studio",
    "machine": "lock_studio",
    "ocean": "lock_studio",
    "lines": "lock_studio",
    "game": "lock_studio",
    "apart": "lock_studio_exposed",
}

# Encounter characters, attached to a frame when its action names them. They
# are previous runners who stopped — each is fused into the world where they
# gave up, so each costume is built from that world's material.
CHARACTERS = {
    "char_explorer": ("explorer",),
    "char_warrior": ("warrior",),
    "char_captain": ("captain",),
    "char_chimera": ("chimera",),
    "char_witchdoctor": ("witchdoctor",),
}

# Cross-world props named directly by an action. World refs cover the normal
# set dressing; these additions keep returning story objects consistent when
# they travel into another world.
OBJECTS = {
    "obj_lines": ("fluorescent", "tube", "neon strip", "branch"),
}

# Which reference sheets a frame in each world must attach.
WORLD_REFS = {
    "record":  ["char", "world_record", "obj_tonearm", "obj_groove"],
    "machine": ["char", "world_machine", "obj_tonearm", "obj_groove"],
    "ocean":   ["char", "world_ocean", "obj_groove"],
    "lines":   ["char", "world_lines", "obj_lines"],
    "game":    ["char", "world_game", "obj_gamepiece"],
    "apart":   ["char", "world_apart", "obj_tonearm", "obj_groove", "obj_lines"],
}

# id, kind, world (world plates only), views-in-the-one-image, attached refs, body
SHEETS = [
    ("char", "character", None, 6, [COVER],
     "Costume reference sheet: ONE image containing six views of the SAME young "
     "woman in the SAME costume, laid out in a grid, full figure unless noted — "
     "(1) standing front; (2) standing three-quarter; (3) profile; (4) mid-run, "
     "side on; (5) horizontal as if suspended on wires; (6) head and shoulders. "
     "Identical costume, hair and proportions in every view. She must be "
     "recognisably the same person as in the attached album cover, which is the "
     "authority for her face, hair and clothing — but built as a television "
     "costume: real fabric, real boots, a made wig of many small buns with "
     "coloured ribbons."),

    ("char_explorer", "character", None, 3, [],
     "Costume reference sheet: ONE image, three views of the same character. A "
     "lost colonial explorer played by a very short, round-bodied older East "
     "Asian male repertory character actor with an enormous white moustache, "
     "thick square spectacles and a pith helmet comically too large for him — "
     "sun-bleached khaki, boots, satchel, "
     "and rolled charts under one arm made from rubbings of record grooves. "
     "Weathered, faded, decades out of date. He is a distinctive character "
     "actor, not a handsome adventure lead or fashion model. The casting is "
     "a comic mismatch; his expression and performance are utterly sincere. "
     "Obvious practical costume."),

    ("char_warrior", "character", None, 3, [],
     "Costume reference sheet: ONE image, three views of the same character. A "
     "short, heavyset middle-aged Black woman cast as a barbarian warrior. Her "
     "soft round silhouette is dwarfed by absurdly enormous armour cut and "
     "lashed together from broken black vinyl record shards, with a blade of "
     "the same material. Scarred; fur, leather straps, painted foam. She is a "
     "distinctive character actress, not an athletic fantasy model. The casting "
     "is a comic mismatch; she carries herself with absolute grim authority. "
     "Obvious hand-built costume, played completely straight."),

    ("char_captain", "character", None, 3, [],
     "Costume reference sheet: ONE image, three views of the same character. A "
     "very tall, reed-thin young South Asian male character actor with prominent "
     "ears cast as a veteran submarine captain. His peaked cap is too wide and "
     "his full uniform hangs one size too large from his narrow shoulders: braid "
     "and brass buttons, salt-stained, holding a brass periscope eyepiece. He is "
     "not a square-jawed military lead. The casting is a comic mismatch; he is "
     "completely dignified and still at his post. Obvious practical costume."),

    ("char_chimera", "character", None, 3, [],
     "Costume reference sheet: ONE image, three views of the same character. An "
     "anthropomorphic bird chimera played by a broad, heavyset older Latina "
     "character actress with powerful shoulders and large square hands, fitted "
     "into an improbably delicate full bird costume with a very long neck, a "
     "moulded beak mask, and plumage made from short fluorescent strip lights "
     "and neon tubes among real feathers. The contrast between sturdy performer "
     "and fragile bird is the comic mismatch; her careful, articulate hands and "
     "performance are completely serious. Visibly a practical costume, not a "
     "sleek creature design."),

    ("char_witchdoctor", "character", None, 3, [],
     "Costume reference sheet: ONE image, three views of the same character. A "
     "short, barrel-shaped elderly white male repertory character actor cast as "
     "a witchdoctor, with an enormous bulbous theatrical prosthetic nose, tiny "
     "round spectacles, and a feathered headdress comically far too tall for "
     "him. Greasepaint; robes hung with charms and fetishes made from broken "
     "record fragments and cartridge parts. Holds a small old vinyl record like "
     "a relic. The costume is a comic mismatch but the actor never mugs and "
     "plays it with grave sincerity. Obvious hand-built costume."),

    ("world_record", "world", "record", 3, [],
     "Set reference plate, NO PEOPLE: one image, three views of the same set. A "
     "television studio floor painted with enormous concentric record grooves "
     "curving away to a painted backdrop horizon, section bands as painted "
     "stripes with raised timber ridges between them, a model record on a "
     "rostrum behind for forced perspective, dust in the air from a hidden air "
     "line."),

    ("world_machine", "world", "machine", 3, [],
     "Set reference plate, NO PEOPLE: one image, three views of the same set. "
     "Groove walls built from plywood and crumpled foil, twice head height, "
     "running away in parallel. A painted cone stylus on a visible track. A "
     "hanging cartridge prop with a lamp inside it overhead. Sparklers rigged at "
     "the contact point."),

    ("world_ocean", "world", "ocean", 3, [],
     "Set reference plate, NO PEOPLE: one image, three views of the same set. An "
     "underwater scene built with NO WATER: deep blue gels, a rippling light "
     "projector, dry ice on the floor, a fish-tank foreground, hanging wires. "
     "The floor is painted with record grooves under a layer of silt. A wrecked "
     "submarine pressed from black vinyl and plywood."),

    ("world_lines", "world", "lines", 2, [],
     "Set reference plate, NO PEOPLE: one image, two views of the same set. Black "
     "studio drapes, no floor visible. Dozens of fluorescent tubes and neon strip "
     "lights suspended at different depths and angles on visible wires, "
     "unordered. The cheapest set in the production and the most striking."),

    ("world_game", "world", "game", 2, [],
     "Set reference plate, NO PEOPLE: one image, two views of the same set. A "
     "playfield of primary-coloured squares built from painted plywood at toy "
     "scale, flat even lighting, hard clean edges, visible brush marks."),

    ("world_apart", "world", "apart", 2, [],
     "Set reference plate, NO PEOPLE: one image, two views. The set collapsing — "
     "painted flats toppling and fallen, bare studio walls, the lighting rig, "
     "cables and cyclorama visible behind them, floor markings exposed, pieces "
     "of the groove set and the plywood playfield lying in the wreckage."),

    ("obj_tonearm", "object", None, 2, [COVER],
     "Prop reference sheet: ONE image, a three-quarter view and a side view of the "
     "same prop. An enormous tonearm and cartridge built for television — timber "
     "tube wrapped in foil, painted headshell, gold-painted cartridge body with "
     "real coloured wiring, a painted cone for a stylus, mounted on a visible "
     "track. Based on the tonearm in the attached album cover."),

    ("obj_groove", "object", None, 2, [COVER],
     "Prop reference sheet: ONE image, two views. A built section of giant record "
     "groove — plywood and crumpled foil walls painted black, a raised timber "
     "ridge between two painted bands, dust and scatter in the valley."),

    ("obj_lines", "object", None, 1, [],
     "Prop reference sheet: ONE image. A bundle of fluorescent tubes and neon strip "
     "lights of varying lengths, lit, with visible end caps and wiring."),

    ("obj_gamepiece", "object", None, 1, [],
     "Prop reference sheet: ONE image. Painted wooden game pieces in primary "
     "colours on a square tile, plus a small old vinyl record used as a relic, "
     "and a witchdoctor charm made from record fragments."),
]


def strip_world(action):
    """script.json prefixes recap actions with "MACHINE:"/"OCEAN:" so the
    alternation reads in the script; the prompt already states the world."""
    return re.sub(r"^[A-Z]{3,}:\s*", "", action)


def locks_from(style_text):
    out = {}
    for m in re.finditer(r"```(lock_[a-z_]+)\s*\n(.*?)```", style_text, re.S):
        out[m.group(1)] = m.group(2).strip()
    return out


def cam_table(style_text):
    out = {}
    for line in style_text.splitlines():
        m = re.match(r"\|\s*`([a-z]+)`\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()

    shots = load(ROOT / "world" / "shots.json")
    style = (ROOT / "board" / "style.md").read_text()
    L = locks_from(style)
    cams = cam_table(style)

    for need in ("lock_global", "lock_sheet", "lock_studio", "lock_studio_exposed"):
        if need not in L:
            raise SystemExit(f"board/style.md is missing the ```{need} block")

    # ---------------------------------------------------------------- sheets
    sheets, by_id = [], {}
    for sid, kind, world, views, refs, body in SHEETS:
        # a world plate is an establishing SCENE and must be in that world's
        # palette; a character or object sheet is a neutral document
        palette = L[WORLD_LOCK[world]] if kind == "world" else L["lock_sheet"]
        entry = {
            "id": sid,
            "kind": kind,
            "world": world,
            "views": views,
            "file": f"board/refs/{sid}.png",
            "attach": list(refs),
            "locks": ["lock_global"] + (
                [WORLD_LOCK[world]] if kind == "world" else ["lock_sheet"]),
            "prompt": f"{body}\n\n{palette}\n\n{L['lock_global']}",
        }
        sheets.append(entry)
        by_id[sid] = entry

    # ---------------------------------------------------------------- frames
    frames = []
    for s in shots["shots"]:
        world = s["world"]
        palette_key = WORLD_LOCK.get(world, "lock_studio")
        refs = list(WORLD_REFS.get(world) or [])
        if not refs:
            raise SystemExit(f"{s['id']}: world '{world}' has no entry in WORLD_REFS")
        # attach an encounter's costume sheet whenever the action names them
        low = (s.get("action") or "").lower()
        for cid, words in CHARACTERS.items():
            if any(w in low for w in words) and cid not in refs:
                refs.append(cid)
        for oid, words in OBJECTS.items():
            if any(w in low for w in words) and oid not in refs:
                refs.append(oid)
        bits = [
            f"Storyboard frame for a music video. World: {world.upper()}.",
            f"Framing: {cams.get(s['cam'], s['cam'])}",
            "Camera variety: Treat the assigned framing as the storytelling "
            "requirement, not a rigid template. Give this shot its own "
            "purposeful lens distance, camera height, angle and foreground; "
            "do not repeat an adjacent shot's composition.",
            ("Action: " + strip_world(s["action"])) if s.get("action") else "",
            "The woman is the SAME PERSON as in the attached character reference "
            "— do not restyle her, do not change her wardrobe or hair, do not "
            "re-imagine her face.",
            "When another named character appears, use that character's attached "
            "reference sheet; do not dress the woman as that character and do "
            "not duplicate or substitute her for them.",
            f"The setting must match the attached {world} world plate.",
            "She is small in the world; do not make her the largest thing in "
            "frame unless this framing is a close-up.",
        ]
        if s.get("lyric"):
            bits.append(f"This frame sits under the sung line: “{s['lyric']}” — "
                        f"let that inform the mood, not the literal content.")
        frames.append({
            "id": s["id"], "section": s["section"], "world": world,
            "cam": s["cam"], "t0": s["t0"], "dur": round(s["t1"] - s["t0"], 3),
            "bar": s["bar"], "lyric": s.get("lyric", ""),
            "action": s.get("action", ""),
            "file": f"board/frames/{s['id']}.png",
            "refs": refs,
            "attach": [by_id[r]["file"] for r in refs],
            "locks": ["lock_global", palette_key],
            "prompt": "\n".join(b for b in bits if b)
                      + f"\n\n{L[palette_key]}\n\n{L['lock_global']}",
        })

    # ------------------------------------------------------------- validate
    problems = []
    for f in frames:
        for r in f["refs"]:
            if r not in by_id:
                problems.append(f"{f['id']}: reference '{r}' has no sheet")
    paths = [x["file"] for x in sheets] + [x["file"] for x in frames]
    if len(paths) != len(set(paths)):
        problems.append("duplicate output paths")
    if len(sheets) != 16:
        problems.append(f"expected 16 reference sheets, have {len(sheets)}")
    if len(frames) != len(shots["shots"]):
        problems.append("frame count does not match world/shots.json")
    if problems:
        for p in problems:
            print("  !! " + p)
        raise SystemExit("work order is not valid")

    save(ROOT / "board" / "prompts.json", {
        "cover": COVER,
        "locks": L,
        "world_lock": WORLD_LOCK,
        "counts": {"sheets": len(sheets), "frames": len(frames)},
        "sheets": sheets,
        "frames": frames,
    })

    md = ["# Storyboard work order", "",
          f"**{len(sheets)} reference sheets, then {len(frames)} frames.** "
          "Sheets first and approved first — every frame attaches them.", "",
          f"Each sheet is ONE canonical file. `views` is how many views appear "
          "*inside* that single image, not how many files to keep. Rejected "
          "attempts go in `board/rejects/`.", "",
          "## Reference sheets", ""]
    for s in sheets:
        md += [f"### `{s['id']}` → `{s['file']}`", "",
               f"{s['views']} view(s) in the one image · locks: "
               f"{', '.join(s['locks'])}"
               + (f" · attach: {', '.join(s['attach'])}" if s["attach"] else ""),
               "", "```", s["prompt"], "```", ""]
    md += ["## Frames", ""]
    cur = None
    for f in frames:
        if f["section"] != cur:
            cur = f["section"]
            md += [f"### {cur}", ""]
        md += [f"**{f['id']}** → `{f['file']}` · {f['t0']:.2f}s · {f['dur']:.2f}s · "
               f"`{f['world']}/{f['cam']}`", "",
               f"attach: {', '.join(f['attach'])}", "",
               "```", f["prompt"], "```", ""]
    (ROOT / "board" / "prompts.md").write_text("\n".join(md))

    cover_ok = (ROOT / COVER).exists()
    print(f"  {len(sheets)} reference sheets  ->  board/refs/")
    print(f"  {len(frames)} frames            ->  board/frames/")
    print(f"  locks: {', '.join(sorted(L))}")
    print(f"  apart world uses {WORLD_LOCK['apart']} (the studio is exposed)")
    status = "present" if cover_ok else "MISSING — the character sheet cannot be generated"
    print(f"  {COVER}: {status}")
    print("  wrote board/prompts.json and board/prompts.md")


if __name__ == "__main__":
    main()
