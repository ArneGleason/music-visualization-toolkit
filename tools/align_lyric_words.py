#!/usr/bin/env python3
"""Conservatively pull late lyric words toward local Whisper onsets.

Line windows remain authoritative.  A later-song phrase is eligible only when
every registered word can be matched, in order, to a Whisper word inside that
line's small timing window.  The correction is intentionally one-way: a word
may move earlier, with a one-frame early bias, but never later.  This leaves
already-good or already-early animation alone while repairing the most obvious
late length-weighted placements.
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import pathlib
import re
import statistics


ROOT = pathlib.Path(__file__).resolve().parents[1]


def clean(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower().replace("’", "'"))


def similarity(left: str, right: str) -> float:
    return difflib.SequenceMatcher(None, clean(left), clean(right)).ratio()


def transcript_words(data: dict) -> list[dict]:
    words = []
    for segment in data.get("segments", []):
        for word in segment.get("words") or []:
            if clean(word.get("word", "")):
                words.append({
                    "text": word["word"].strip(),
                    "start": float(word["start"]),
                    "end": float(word["end"]),
                    "probability": float(word.get("probability", 0.0)),
                })
    return words


def match_all(expected: list[dict], candidates: list[dict], fps: float,
              minimum_similarity: float) -> list[tuple[dict, float]] | None:
    """Return the best ordered candidate for every expected word."""
    n, m = len(expected), len(candidates)
    minus_inf = -10_000.0
    score = [[minus_inf] * (m + 1) for _ in range(n + 1)]
    parent = [[None] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        score[0][j] = 0.0
        if j:
            parent[0][j] = (0, j - 1, False, 0.0)

    for i in range(1, n + 1):
        expected_sec = float(expected[i - 1]["on"]) / fps
        for j in range(1, m + 1):
            # Extra transcript words are harmless inside a known line window.
            score[i][j] = score[i][j - 1]
            parent[i][j] = (i, j - 1, False, 0.0)
            sim = similarity(expected[i - 1]["text"], candidates[j - 1]["text"])
            if sim < minimum_similarity or score[i - 1][j - 1] <= minus_inf:
                continue
            timing_distance = abs(candidates[j - 1]["start"] - expected_sec)
            value = (score[i - 1][j - 1] + sim
                     + 0.08 * candidates[j - 1]["probability"]
                     - 0.035 * min(timing_distance, 2.5))
            if value > score[i][j]:
                score[i][j] = value
                parent[i][j] = (i - 1, j - 1, True, sim)

    if score[n][m] <= minus_inf:
        return None
    found = []
    i, j = n, m
    while i:
        step = parent[i][j]
        if step is None:
            return None
        pi, pj, used, sim = step
        if used:
            found.append((candidates[j - 1], sim))
        i, j = pi, pj
    found.reverse()
    return found if len(found) == n else None


def propose(choreography: dict, transcript: dict, preserve_first: int,
            early_bias: int, window: float, minimum_similarity: float,
            minimum_average: float, minimum_probability: float,
            minimum_adjustment: int) -> tuple[list[dict], list[dict]]:
    fps = float(choreography["fps"])
    heard = transcript_words(transcript)
    phrase_results = []
    changes = []
    for phrase_index, phrase in enumerate(choreography["phrases"]):
        t0 = float(phrase["on"]) / fps - window
        t1 = float(phrase["off"]) / fps + window
        candidates = [w for w in heard if t0 <= w["start"] <= t1]
        matched = match_all(phrase["words"], candidates, fps, minimum_similarity)
        result = {
            "index": phrase_index + 1,
            "id": phrase["id"],
            "text": phrase["text"],
            "matched": bool(matched),
            "eligible": False,
            "changes": [],
        }
        if not matched:
            phrase_results.append(result)
            continue
        average_similarity = statistics.mean(sim for _, sim in matched)
        average_probability = statistics.mean(w["probability"] for w, _ in matched)
        result["average_similarity"] = average_similarity
        result["average_probability"] = average_probability
        eligible = (
            phrase_index >= preserve_first
            and average_similarity >= minimum_average
            and average_probability >= minimum_probability
        )
        result["eligible"] = eligible
        previous_on = int(phrase["on"]) - 2
        proposed_ons = []
        for word, (detected, sim) in zip(phrase["words"], matched):
            detected_frame = math.floor(detected["start"] * fps) - early_bias
            # Never push a word later. Preserve readable ordering and two
            # frames of minimum active time for the preceding word.
            proposed_on = min(int(word["on"]), detected_frame)
            proposed_on = max(int(phrase["on"]), previous_on + 2, proposed_on)
            proposed_ons.append(proposed_on)
            previous_on = proposed_on
            delta = proposed_on - int(word["on"])
            detail = {
                "word": word["text"],
                "heard": detected["text"],
                "current": int(word["on"]),
                "detected": detected_frame,
                "proposed": proposed_on,
                "delta": delta,
                "similarity": sim,
                "probability": detected["probability"],
            }
            if eligible and delta <= -minimum_adjustment:
                result["changes"].append(detail)
                changes.append({"phrase": phrase, **detail})
        result["proposed_ons"] = proposed_ons
        phrase_results.append(result)
    return phrase_results, changes


def apply_changes(choreography: dict, phrase_results: list[dict]) -> None:
    by_id = {result["id"]: result for result in phrase_results}
    for phrase in choreography["phrases"]:
        result = by_id[phrase["id"]]
        if not result["eligible"] or not result["changes"]:
            continue
        for word, on in zip(phrase["words"], result["proposed_ons"]):
            word["on"] = on
        for index, word in enumerate(phrase["words"]):
            word["off"] = (phrase["words"][index + 1]["on"]
                           if index + 1 < len(phrase["words"])
                           else int(phrase["off"]))


def report_markdown(transcript_path: pathlib.Path, phrase_results: list[dict],
                    changes: list[dict], args) -> str:
    matched = sum(bool(item["matched"]) for item in phrase_results)
    eligible = sum(bool(item["eligible"]) for item in phrase_results)
    changed_phrases = sum(bool(item["changes"]) for item in phrase_results)
    deltas = [item["delta"] for item in changes]
    lines = [
        "# Conservative lyric-onset alignment report", "",
        f"Whisper source: `{transcript_path.as_posix()}` (local, generated, not tracked).",
        "", "The line windows remain authoritative. The first six hand-timed",
        "phrases are preserved. A later phrase is eligible only when every word",
        "matches in order inside its line window. Corrections are early-only:",
        f"detected onsets receive a {args.early_bias}-frame early bias, and a word",
        "is never moved later than its existing frame.", "",
        f"- Line-window tolerance: ±{args.window:.2f} seconds",
        f"- Minimum phrase-average lexical match: {args.minimum_average:.2f}",
        f"- Minimum phrase-average confidence: {args.minimum_probability:.2f}",
        f"- Fully matched phrases: {matched} / {len(phrase_results)}",
        f"- Eligible phrases: {eligible}",
        f"- Changed phrases: {changed_phrases}",
        f"- Changed words: {len(changes)}",
        f"- Median applied shift: {statistics.median(deltas) if deltas else 0:g} frames",
        "", "| Phrase | Word | Heard | Current | Detected+bias | Applied | Shift | Match | Confidence |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in changes:
        lines.append(
            f"| `{item['phrase']['id']}` | {item['word']} | {item['heard']} | "
            f"{item['current']} | {item['detected']} | {item['proposed']} | "
            f"{item['delta']:+d} | {item['similarity']:.2f} | {item['probability']:.2f} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--choreography", default="shots/lyric_motion_full.json")
    parser.add_argument("--transcript", default="out/_lyric_alignment_v01/song.json")
    parser.add_argument("--report", default="out/_lyric_alignment_v01/report.md")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--preserve-first", type=int, default=6)
    parser.add_argument("--early-bias", type=int, default=1)
    parser.add_argument("--window", type=float, default=0.45)
    parser.add_argument("--minimum-similarity", type=float, default=0.72)
    parser.add_argument("--minimum-average", type=float, default=0.88)
    parser.add_argument("--minimum-probability", type=float, default=0.30)
    parser.add_argument("--minimum-adjustment", type=int, default=2)
    parser.add_argument("--timing-review", default="shots/lyric_timing_review_full.md")
    args = parser.parse_args()

    choreography_path = ROOT / args.choreography
    transcript_path = ROOT / args.transcript
    report_path = ROOT / args.report
    choreography = json.loads(choreography_path.read_text(encoding="utf-8"))
    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
    phrase_results, changes = propose(
        choreography, transcript, args.preserve_first, args.early_bias,
        args.window, args.minimum_similarity, args.minimum_average,
        args.minimum_probability, args.minimum_adjustment)
    if args.apply:
        apply_changes(choreography, phrase_results)
        choreography_path.write_text(
            json.dumps(choreography, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        review_path = ROOT / args.timing_review
        existing = review_path.read_text(encoding="utf-8") if review_path.exists() else ""
        marked_rows = []
        for line in existing.splitlines():
            if not re.match(r"^\|\s*\d+\s*\|", line):
                continue
            columns = line.split("|")
            if len(columns) >= 10 and (columns[7].strip() or columns[8].strip()):
                marked_rows.append(line)
        if marked_rows:
            print(f"kept {review_path.relative_to(ROOT)}: it contains owner notes")
        else:
            from lyric_choreography import timing_markdown
            review_path.write_text(timing_markdown(choreography), encoding="utf-8")
            print(f"refreshed {review_path.relative_to(ROOT)}")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        report_markdown(pathlib.Path(args.transcript), phrase_results, changes, args),
        encoding="utf-8")
    print(f"matched {sum(r['matched'] for r in phrase_results)}/{len(phrase_results)} phrases")
    print(f"eligible {sum(r['eligible'] for r in phrase_results)} phrases")
    print(f"proposed {len(changes)} earlier word adjustments")
    print(f"wrote {report_path.relative_to(ROOT)}")
    if args.apply:
        print(f"updated {choreography_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
