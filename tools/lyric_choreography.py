#!/usr/bin/env python3
"""Build full-song lyric choreography from the frame-accurate lyric register.

The first six hand-authored pilot phrases are preserved verbatim. Remaining
lines receive provisional, frame-based word windows and a restrained semantic
gesture from a shared vocabulary. The output is editable data, not a render.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

STOPWORDS = {
    "a", "all", "an", "and", "be", "been", "but", "can", "couldve",
    "do", "for", "from", "got", "has", "i", "if", "in", "is", "it",
    "its", "ive", "like", "me", "my", "of", "on", "or", "should",
    "that", "the", "their", "they", "theyre", "this", "through", "to",
    "was", "we", "well", "what", "whats", "who", "you", "youve", "your",
}

WAVE = {
    "sound", "sounds", "song", "music", "hear", "heard", "words", "meaning",
    "moving", "swimming", "rivers", "river", "wagging", "bends", "mind",
    "follows", "answers", "la-la-la", "la-la-la—la-la", "da-da-dum",
    "the-the-the-the-the",
}
SCATTER = {"pieces", "things", "stuff", "words", "bodies", "mouths", "senses"}
ASSEMBLE = {"attach", "fit", "match", "pattern", "shape", "deal"}
ORBIT = {"around", "spin", "turns", "world", "mars", "moon", "heaven"}
LIGHT = {"green", "light", "waking", "woke", "begin", "night", "goodnight"}
TRAVEL = {"send", "moving", "coming", "follows", "leaves", "falls", "back"}
WEIGHT = {"important", "hard", "subject", "define", "true", "stupid", "shit"}
NEGATE = {"no", "not", "nothing", "dont", "never", "forgot", "fake"}
DOWN = {"dig", "underneath", "falls", "low"}


def clean_word(word: str) -> str:
    return re.sub(r"[^a-z0-9—-]", "", word.lower().replace("’", "'"))


def allocate_frames(words, on, off):
    """Length-weighted provisional timing that exactly fills the line window."""
    count = len(words)
    total = max(count, off - on)
    minimum = 2 if total < count * 4 else 3
    minimum = min(minimum, max(1, total // count))
    weights = [max(1.0, math.sqrt(max(1, len(clean_word(w))))) for w in words]
    remaining = max(0, total - minimum * count)
    raw = [remaining * w / sum(weights) for w in weights]
    durations = [minimum + int(v) for v in raw]
    for i in sorted(range(count), key=lambda n: raw[n] - int(raw[n]), reverse=True)[:total - sum(durations)]:
        durations[i] += 1
    result = []
    cursor = on
    for i, (word, duration) in enumerate(zip(words, durations)):
        end = off if i == count - 1 else min(off, cursor + duration)
        result.append((word, cursor, end))
        cursor = end
    return result


def motif_for(text):
    lower = text.lower()
    if any(w in lower for w in ("garden", "green light", "waking", "woke")):
        return "organic signal ripple"
    if any(w in lower for w in ("send", "attach", "stuff", "pieces")):
        return "handoff and assembly"
    if any(w in lower for w in ("pattern", "shape", "spin", "world")):
        return "formation and orbit"
    if any(w in lower for w in ("dig", "underneath")):
        return "downward excavation"
    if any(w in lower for w in ("meaning", "words", "thread")):
        return "semantic unraveling"
    if any(w in lower for w in ("rockets", "overhead", "falls from heaven")):
        return "overhead arrival"
    if any(w in lower for w in ("rivers of mars", "swimming", "tails wagging")):
        return "liquid travelling wave"
    if any(w in lower for w in ("then turns", "then follows", "then answers")):
        return "call-and-response sequence"
    if any(w in lower for w in ("night", "goodnight", "low light")):
        return "soft closing cadence"
    return "rubber-to-rigid response chain"


def hero_indices(words):
    scored = []
    semantic = WAVE | SCATTER | ASSEMBLE | ORBIT | LIGHT | TRAVEL | WEIGHT | NEGATE | DOWN
    for i, word in enumerate(words):
        key = clean_word(word)
        if key in STOPWORDS:
            continue
        score = len(key) + (20 if key in semantic else 0) + (2 if i == len(words) - 1 else 0)
        scored.append((score, i))
    if not scored:
        return {len(words) - 1}
    scored.sort(reverse=True)
    n = 2 if len(words) >= 5 else 1
    return {i for _, i in scored[:n]}


def motion_for(word, index, count, speaker, hero):
    key = clean_word(word)
    base_rigidity = {"Them 1": 0.42, "Them 2": 0.66, "Them 3": 0.24}.get(speaker, 0.18)
    if key in STOPWORDS:
        base_rigidity = 0.76
    d = {
        "text": word,
        "rigidity": round(base_rigidity, 2),
        "dy": 2 if not hero else 7,
        "sx": 1.02 if not hero else 1.08,
        "sy": 1.02 if not hero else 1.10,
    }
    if hero:
        d["bend"] = 4

    if key in WAVE or key.startswith("la-la") or key.startswith("da-da") or key.startswith("the-the"):
        d.update(rigidity=0.08, wave=14, bend=11, dy=8, sx=1.05, sy=1.16)
    if key in SCATTER:
        d.update(rigidity=0.12, scatter=12, wave=6, bend=9, sx=1.06, sy=1.10)
    if key in ASSEMBLE:
        d.update(rigidity=0.30, split=5, spread=-1.5, recoil_x=6, sx=1.10, sy=1.06)
    if key in ORBIT:
        d.update(rigidity=min(float(d["rigidity"]), 0.35), rotation=8, curve=7,
                 bend=8, sx=1.14, sy=1.06)
    if key in LIGHT:
        d.update(rigidity=0.12, dy=13, wave=5, bend=8, sx=1.08, sy=1.18)
    if key in TRAVEL:
        d.update(rigidity=min(float(d["rigidity"]), 0.35), dx=14, entry_dx=-10,
                 bend=6, recoil_x=4)
    if key in WEIGHT:
        d.update(rigidity=0.92, dy=-6, sx=1.18, sy=0.92,
                 anticipation_y=10, recoil_y=3)
    if key in NEGATE:
        d.update(rigidity=0.88, rotation=-3, sx=1.10, sy=0.94, recoil_x=8)
    if key in DOWN:
        d.update(dy=-13, sy=0.88, anticipation_y=8, recoil_y=-3)
    if key in {"clap", "rockets"}:
        d.update(rigidity=0.22, dy=16 if key == "rockets" else 5,
                 sx=1.20, sy=0.84 if key == "clap" else 1.18, bend=8)
    if word.rstrip().endswith("?"):
        d.update(rigidity=min(float(d["rigidity"]), 0.38), rotation=4,
                 dy=max(7, int(d.get("dy", 0))), recoil_y=4)
    return d


def build_full(cues, pilot):
    phrases = list(pilot["phrases"])
    lane_ends = [max((p["off"] for p in phrases), default=-1), -1]
    for line in cues["lyrics"][len(phrases):]:
        words = line["text"].split()
        heroes = hero_indices(words)
        lane = next((i for i, end in enumerate(lane_ends) if end <= int(line["on"]) + 1), 0)
        lane_ends[lane] = int(line["off"])
        timed = allocate_frames(words, int(line["on"]), int(line["off"]))
        choreography = []
        for i, (word, on, off) in enumerate(timed):
            move = motion_for(word, i, len(words), line.get("speaker"), i in heroes)
            move["on"] = on
            move["off"] = off
            # Put timing first in the serialized object for easier hand review.
            move = {"text": move.pop("text"), "on": move.pop("on"),
                    "off": move.pop("off"), **move}
            choreography.append(move)
        phrase = {
            "id": line["id"],
            "text": line["text"],
            "speaker": line.get("speaker"),
            "on": int(line["on"]),
            "off": int(line["off"]),
            "motif": motif_for(line["text"]),
            "words": choreography,
        }
        if lane:
            phrase["baseline_offset_px_720"] = 58
        phrases.append(phrase)

    full = {k: v for k, v in pilot.items() if k != "phrases"}
    full["_comment"] = (
        "Full-song flat lyric choreography baseline. First six phrases are "
        "hand-authored; later word frames begin provisional and may be refined "
        "with tools/align_lyric_words.py and shots/lyric_timing_review_full.md.")
    full["start"] = 0
    full["end"] = int(cues["frames"]) - 1
    full["type_scale"] = 0.66
    full["backing_band"] = False
    full["line_preroll_frames"] = 1
    full["line_tail_frames"] = 0
    full["line_clearance_frames"] = 4
    full["focus_shadow"] = True
    full["focus_color"] = [1.0, 0.965, 0.86, 1.0]
    full["focus_shadow_color"] = [0.018, 0.020, 0.026, 1.0]
    full["focus_shadow_offset_px_720"] = 2.5
    full["focus_shadow_expand"] = 1.065
    full["phrases"] = phrases
    return full


def timing_markdown(full):
    lines = [
        "# Lyric word-timing review — full song", "",
        "The JSON is the machine-readable source. While listening, put `OK`,",
        "`on -3f`, `on +2f`, or an exact value such as `on=181` in **Correction / OK**.",
        "Use **Listening note** for the intended consonant, syllable, or musical landing.",
        "An agent should apply confirmed changes to `shots/lyric_motion_full.json`,",
        "preserve this sheet as the decision trail, and rerender.", "",
        "| # | Phrase ID | Speaker | Word | Current on | Current off | Correction / OK | Listening note |",
        "|---:|---|---|---|---:|---:|---|---|",
    ]
    for pi, phrase in enumerate(full["phrases"], 1):
        speaker = phrase.get("speaker") or "—"
        for word in phrase["words"]:
            lines.append(
                f"| {pi} | `{phrase['id']}` | {speaker} | {word['text']} | "
                f"{word['on']} | {word['off']} |  |  |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cues", default="generated/overlay_cues.json")
    ap.add_argument("--pilot", default="shots/lyric_motion_pilot.json")
    ap.add_argument("--out", default="shots/lyric_motion_full.json")
    ap.add_argument("--review", default="shots/lyric_timing_review_full.md")
    args = ap.parse_args()
    cues = json.loads((ROOT / args.cues).read_text(encoding="utf-8"))
    pilot = json.loads((ROOT / args.pilot).read_text(encoding="utf-8"))
    full = build_full(cues, pilot)
    out = ROOT / args.out
    review = ROOT / args.review
    out.write_text(json.dumps(full, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    review.write_text(timing_markdown(full), encoding="utf-8")
    words = sum(len(p["words"]) for p in full["phrases"])
    print(f"wrote {out.relative_to(ROOT)}: {len(full['phrases'])} phrases, {words} words")
    print(f"wrote {review.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
