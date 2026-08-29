#!/usr/bin/env python3
"""
Export the musical substrate for the VECTOR STAGE — the laser-show visualiser.

    ./.venv/bin/python3 tools/stage_export.py     ->  stage/data.json

This is world_export.py's richer sibling. The 3D world only needs to know when
things hit; the vector stage needs to know what everything is DOING, because
every actor is a line whose shape carries the information.

Three kinds of data, in increasing order of how much work they took to get:

1. WHAT WAS PLAYED — MIDI notes per track, from the DAWproject, on the exact
   tempo-ramp grid. Notes give the figures their pitch, their density and
   their attacks.

2. WHAT WAS AUTOMATED — the 10 real automation lanes, resampled from sparse
   breakpoints onto the same continuous grid as everything else, so the
   renderer can read `lane[i]` without interpolating. These are the moves the
   author actually made: reverb decay and feedback, the sends opening up, one
   pan sweep, two transposes.

3. WHAT THE AUDIO IMPLIES — derived features. The automation is sparse, and a
   visualiser driven only by it would sit still for a minute at a time. So for
   every stem we also compute, at the export rate:

       amp       rms, normalised to the stem's own 95th percentile
       centroid  spectral centre of mass across the six bands, 0..1.
                 This is BRIGHTNESS. It moves constantly and it is the single
                 most useful continuous control in the whole file.
       flux      positive spectral change — how much the timbre is MOVING.
                 Near zero on a held pad, high on a busy vocal.
       spread    how many bands carry real energy, 0..1. Narrow = a sine-ish
                 tone, wide = noise or a full chord.
       tilt      high-band energy minus low-band energy, -1..1. Which end of
                 the spectrum the part lives at.
       attack    transient density: a decaying counter kicked by every rise.

   plus, for tracks that have MIDI:

       density   notes started per second, smoothed
       poly      how many notes are sounding at once
       ambitus   the pitch range currently in play, in semitones

Everything is quantised to small integers or 3 decimals and stored as flat
parallel arrays at one rate, so the JSON stays a few megabytes rather than
tens, and the renderer's inner loop is an array index rather than a search.
"""
from __future__ import annotations

import argparse
import array
import bisect
import math
import pathlib
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save  # noqa: E402
from dawproject import TempoCurve, read_project_xml  # noqa: E402
from stage import (ARCHETYPES, DEFAULT_STYLE, PARAM_KEYS, kit_hits,  # noqa: E402
                   load_lanes, load_notes, short)

# Which figure family each instrument gets. The renderer owns the geometry;
# this file only says which one, so the assignment is reviewable in one place.
#
#   ribbon   an open line that unrolls — voices, things with words
#   knot     a closed torus knot — sustained harmonic material
#   lissajous a closed 3D Lissajous — bass, slow and deep
#   comb     a rigid rack of parallel segments — percussive, non-pitched
FIGURES = [
    ("lead vocal", "ribbon"),
    ("backing",    "ribbon"),
    ("bass",       "lissajous"),
    ("synth",      "knot"),
    ("drum",       "comb"),
    ("perc",       "comb"),
]


def figure_for(name, kind):
    """Audio stems get a family by name; MIDI tracks all get `chord`.

    A MIDI track knows something no audio stem does — the exact notes, and so
    the exact intervals. `chord` turns that into a harmonic rose whose lobe
    count comes from the intervals above the bass, which means a triad and its
    inversion produce visibly different figures. That is the most literal
    music-to-shape mapping in the piece and it is worth its own family.
    """
    if kind == "midi":
        return "chord"
    low = name.lower()
    for key, fig in FIGURES:
        if key in low:
            return fig
    return "knot"


MIN_NOTES = 5      # below this a "MIDI track" is a stray note, not a part


def resample_lane(lane, rate, n):
    """Sparse breakpoints -> a dense series on the export grid.

    DAWproject stores automation as breakpoints with an implied hold or ramp
    between them. `load_lanes` already converted the times through the tempo
    curve, so this is a straight linear walk. Before the first point the lane
    holds its first value; after the last it holds its last. That matches what
    the DAW does on playback.
    """
    pts = lane["pts"]
    out = [0.0] * n
    j = 0
    for i in range(n):
        t = i / rate
        while j + 1 < len(pts) - 1 and pts[j + 1][0] <= t:
            j += 1
        if t <= pts[0][0]:
            out[i] = pts[0][1]
        elif t >= pts[-1][0]:
            out[i] = pts[-1][1]
        else:
            (t0, v0), (t1, v1) = pts[j], pts[j + 1]
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            out[i] = v0 + (v1 - v0) * f
    return out


def aligned_series(series, src_rate, rate, n, delta=0.0):
    """Sample a stem-domain envelope on the mix clock.

    ``delta_sec`` is defined by the extractor as stem time minus mix time, so
    the sample belonging at mix time ``t`` lives at ``t + delta`` in the
    source envelope.  Keeping this correction here means every downstream
    feature, gate and visual onset shares the same clock as the master audio.
    """
    if not series:
        return [0] * n
    last = len(series) - 1
    return [series[max(0, min(last, round((i / rate + delta) * src_rate)))]
            for i in range(n)]


def features(tr, band_names, src_rate, rate, n, delta=0.0):
    """Per-stem continuous features on the export grid. See the module docstring.

    Everything here is derived from the six-band envelope and the rms the stem
    extractor already computed — no second pass over the audio.
    """
    rms = tr["rms"]
    bands = [tr.get("bands", {}).get(b, []) for b in band_names]
    nb = len(bands)

    vals = sorted(v for v in rms if v > 5)
    norm = max(60.0, vals[int(len(vals) * 0.95)] if vals else 700.0)

    amp, cen, flx, spr, tlt, atk = [], [], [], [], [], []
    prev = None
    attack = 0.0
    slow = 0.0
    for i in range(n):
        k = max(0, min(len(rms) - 1,
                       round((i / rate + delta) * src_rate)))
        a = min(1.6, rms[k] / norm) if rms else 0.0
        amp.append(a)

        row = [bands[b][k] if k < len(bands[b]) else 0 for b in range(nb)]
        tot = sum(row) or 1e-6
        # centroid: energy-weighted band index, mapped to 0..1
        c = sum(row[b] * b for b in range(nb)) / tot / max(1, nb - 1)
        cen.append(c)
        # spread: normalised entropy of the band distribution
        p = [r / tot for r in row]
        ent = -sum(x * math.log(x + 1e-9) for x in p) / math.log(nb)
        spr.append(max(0.0, min(1.0, ent)))
        # tilt: top third minus bottom third
        lo = sum(row[:max(1, nb // 3)])
        hi = sum(row[-max(1, nb // 3):])
        tlt.append((hi - lo) / tot)
        # flux: positive change only, normalised
        if prev is None:
            flx.append(0.0)
        else:
            f = sum(max(0.0, row[b] - prev[b]) for b in range(nb)) / tot
            flx.append(min(1.0, f))
        prev = row
        # attack: a counter kicked by rises above a slow average, decaying
        slow += (a - slow) * 0.06
        attack = max(attack * 0.86, min(1.0, max(0.0, a - slow) * 3.2))
        atk.append(attack)

    q = lambda v, d=3: [round(x, d) for x in v]  # noqa: E731
    return {"norm": round(norm, 1), "amp": q(amp), "centroid": q(cen, 3),
            "flux": q(flx), "spread": q(spr), "tilt": q(tlt), "attack": q(atk)}


def _ema(series, rate, tau):
    k = 1.0 - math.exp(-1.0 / (rate * tau))
    out, v = [0.0] * len(series), series[0] if series else 0.0
    for i, x in enumerate(series):
        v += (x - v) * k
        out[i] = v
    return out


def _norm(series, pct=0.90, floor=1e-6):
    """Scale to 0..1 against the series' own high percentile."""
    v = sorted(x for x in series if x > 0)
    ref = v[int(len(v) * pct)] if v else 1.0
    ref = max(ref, floor)
    return [round(min(1.0, x / ref), 3) for x in series]



# Set this in a project fork only when the source metadata cannot supply the
# desired display title. Keeping the toolkit default empty makes a new project
# derive its own title instead of inheriting the example song's name.
TITLE_OVERRIDE = None


def song_title(root, env, bm):
    """The track's title, from wherever it actually exists.

    The DAWproject metadata block is present but empty — Bitwig does not fill
    it in unless you do — so fall back to the stems, which are all named
    "<title> - clear vocals (Part)". The common prefix before the first dash
    IS the title, and it is the only place in this project where it is
    written down.
    """
    if TITLE_OVERRIDE:
        return TITLE_OVERRIDE
    for md in root.iter("MetaData"):
        el = md.find("Title")
        if el is not None and (el.text or "").strip():
            return el.text.strip()
    names = [n for n in env["tracks"]]
    if names:
        heads = [n.split(" - ")[0].strip() for n in names if " - " in n]
        if heads and len(set(heads)) == 1 and heads[0]:
            return heads[0]
    stem = pathlib.Path(bm.get("master_wav", "") or "untitled").stem
    return stem.split(" 20")[0].strip() or "untitled"


def silence_gate(amp, rate, n, quiet=0.085, gap=1.0, lead_out=0.60,
                 clear=1.00, lead_in=0.40):
    """When should this actor be off stage, decided ahead of time.

    A player that is about to go quiet for more than a second should already
    be leaving — an exit that starts when the sound stops is an exit you watch
    happen, which is exactly the wrong thing to be looking at. So: find every
    stretch where the level sits below `quiet` for at least `gap` seconds,
    begin the departure `lead_out` seconds BEFORE it starts, and be completely
    gone `clear` seconds after it starts. Coming back is quicker — the return
    only has to beat the note by `lead_in`.

    Returns 0..1: 1 = belongs on stage, 0 = should not be visible at all.
    """
    q = [1 if a > quiet else 0 for a in amp]
    gates = [1.0] * n
    i = 0
    G = max(1, int(gap * rate))
    while i < n:
        if q[i]:
            i += 1
            continue
        j = i
        while j < n and not q[j]:
            j += 1
        if j - i >= G:                       # a real silence, not a rest
            s0 = i / rate
            a0, a1 = s0 - lead_out, s0 + clear
            b1 = j / rate - lead_in          # back before the next entry
            b0 = b1 - 0.45
            for k in range(max(0, int(a0 * rate)), min(n, int(b1 * rate) + 1)):
                t = k / rate
                if t < a0:
                    v = 1.0
                elif t < a1:
                    v = 1.0 - (t - a0) / max(1e-6, a1 - a0)
                elif t < b0:
                    v = 0.0
                else:
                    v = (t - b0) / max(1e-6, b1 - b0)
                gates[k] = min(gates[k], max(0.0, min(1.0, v)))
        i = j
    return [round(x, 3) for x in gates]


def salience(amp, attack, rate, look=2.0):
    """How much this actor deserves the stage right now — including soon.

    Two parts. What it is doing (level plus attack), and what it is ABOUT to
    do: a forward window over the next couple of seconds, weighted so that a
    big entry two seconds away already counts for something. That is what lets
    the renderer walk an actor on BEFORE its moment rather than after it, so
    the arrival lands with the music instead of chasing it.

    Returned normalised to its own 88th percentile, so ranking actors against
    each other compares like with like — a quiet pad at full tilt can out-rank
    a loud synth that is coasting.
    """
    n = len(amp)
    L = max(1, int(look * rate))
    now = [amp[i] + 1.6 * attack[i] for i in range(n)]
    # forward maximum with a linear ramp: nearer events count for more
    lead = [0.0] * n
    for i in range(n):
        best = 0.0
        for j in range(i, min(n, i + L)):
            w = 1.0 - 0.85 * (j - i) / L
            v = now[j] * w
            if v > best:
                best = v
        lead[i] = best
    raw = [0.55 * now[i] + 0.85 * lead[i] for i in range(n)]
    return _norm(_ema(raw, rate, 0.20), 0.88), _norm(lead, 0.88)


def note_features(notes, rate, n):
    """density / poly / ambitus on the export grid, from the note list."""
    ons = [x[0] for x in notes]
    den, poly, amb, mp = [0.0] * n, [0] * n, [0] * n, [0.0] * n
    d, held = 0.0, 60.0
    for i in range(n):
        t = i / rate
        lo = bisect.bisect_left(ons, t - 1.0 / rate)
        hi = bisect.bisect_right(ons, t)
        d = d * 0.90 + (hi - lo) * rate * 0.10
        den[i] = round(min(1.0, d / 12.0), 3)
        live = [p for on, off, p, _ in notes[max(0, hi - 64):hi] if on <= t < off]
        poly[i] = len(live)
        amb[i] = (max(live) - min(live)) if len(live) > 1 else 0
        if live:
            held = sum(live) / len(live)
        mp[i] = round(held, 2)
    return {"density": den, "poly": poly, "ambitus": amb, "meanpitch": mp}



# ═══════════════════════════════════════════════════════════════════════════
# THE INSTRUMENT PANEL
#
# Readouts that behave like instruments rather than captions: each one carries
# an `interest` series, and the renderer only brings it on stage when that
# rises. So the panel is quiet through a steady verse and crowded through a
# tempo ramp or a key change — the display itself becomes a reading of how
# much is happening.
#
# On honesty, because metering invites overclaiming:
#   * The "mix" here is the SUM OF THE STEMS. That is the mix before the
#     master bus, not the master.
#   * Loudness is K-weighted across six bands and expressed relative to this
#     song's own 95th percentile. It is not LUFS and must not be read as LUFS.
#   * Crest is derived from stem peak and rms, so it is a proxy.
#   * There is no stereo width or correlation here, because the envelopes are
#     mono. Those would need a second pass over the master audio.
#   * The tonal-balance target is THIS SONG's own long-term average spectrum,
#     not a genre curve. Deviation from it is a real measurement of what the
#     arrangement is doing right now.
# ═══════════════════════════════════════════════════════════════════════════

# Rough K-weighting at our six band centres (55, 140, 450, 1400, 3900, 9000 Hz):
# the RLB high-pass pulls the bottom down, the shelf lifts the top.
K_WEIGHT = [0.06, 0.63, 1.00, 1.00, 1.58, 1.58]


def novelty(series, rate, fast=0.30, slow=5.0):
    """How unlike its recent self a series is right now.

    A fast and a slow follower; where they diverge, something changed. This is
    deliberately scale-free — it fires on a tempo ramp and on a spectral shift
    alike, without either needing a hand-set threshold.
    """
    if not series:
        return []
    f, sl = _ema(series, rate, fast), _ema(series, rate, slow)
    raw = [abs(f[i] - sl[i]) for i in range(len(series))]
    return _norm(_ema(raw, rate, 0.45))


def event_interest(times, n, rate, decay=1.9, rise=0.12):
    """A spike at each event, decaying after it. For things that CHANGE rather
    than drift — a chord, a section, the top of a phrase."""
    out = [0.0] * n
    for t in times:
        i0 = int(t * rate)
        if not (0 <= i0 < n):
            continue
        for j in range(i0, min(n, i0 + int(decay * rate * 3))):
            age = (j - i0) / rate
            e = min(1.0, age / rise) if age < rise else math.exp(-(age - rise) / decay)
            if e > out[j]:
                out[j] = e
    return [round(x, 3) for x in out]


CHORD_TEMPLATES = [
    ("",     (0, 4, 7)),        ("m",    (0, 3, 7)),
    ("dim",  (0, 3, 6)),        ("aug",  (0, 4, 8)),
    ("sus4", (0, 5, 7)),        ("sus2", (0, 2, 7)),
    ("7",    (0, 4, 7, 10)),    ("maj7", (0, 4, 7, 11)),
    ("m7",   (0, 3, 7, 10)),    ("m7b5", (0, 3, 6, 10)),
    ("6",    (0, 4, 7, 9)),     ("m6",   (0, 3, 7, 9)),
]
PITCH_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def name_chord(pcs, bass_pc):
    """Best-matching chord name for a set of pitch classes.

    Scored by how much of the template is present minus what is left over, with
    a nudge toward roots that are actually in the bass. Ties go to the simpler
    template because it is listed first.
    """
    if not pcs:
        return ""
    best, score = "", -99
    for root in range(12):
        for suffix, ivs in CHORD_TEMPLATES:
            tpl = {(root + i) % 12 for i in ivs}
            hit = len(tpl & pcs)
            sc = hit * 2 - len(tpl - pcs) - len(pcs - tpl) * 0.5
            if root == bass_pc:
                sc += 1.0
            if sc > score:
                best, score = PITCH_NAMES[root] + suffix, sc
    return best if score > 0 else ""


def build_panel(bm, env, actors, notes, rate, n, dur, band_names, sections):
    """Everything the instrument panel needs, on the export grid."""
    nb = len(band_names)

    # ── tempo: two different true answers, and they disagree ───────────────
    # The DAWproject holds 942 tempo points swinging 119-133 BPM. That is a
    # fast humanising wobble, not a slow drift — so deriving tempo from the
    # beat grid, which averages over half a second, gives 124-129 and hides
    # the very thing that is interesting. Export both: the instantaneous
    # automation, which is what was actually written, and the tapped tempo,
    # which is what you would count. The readout shows the first and the
    # second is there for reference.
    def _resample(pts, n_):
        out, j_ = [0.0] * n_, 0
        if not pts:
            return [120.0] * n_
        for i_ in range(n_):
            t_ = i_ / rate
            while j_ + 1 < len(pts) - 1 and pts[j_ + 1][0] <= t_:
                j_ += 1
            if t_ <= pts[0][0]:
                out[i_] = pts[0][1]
            elif t_ >= pts[-1][0]:
                out[i_] = pts[-1][1]
            else:
                (t0, v0), (t1, v1) = pts[j_], pts[j_ + 1]
                f_ = (t_ - t0) / (t1 - t0) if t1 > t0 else 0.0
                out[i_] = v0 + (v1 - v0) * f_
        return out

    tm = sorted((p_["sec"], p_["bpm"]) for p_ in bm["tempo_map"])
    bpm = _resample(tm, n)
    beats = sorted({round(x, 6) for b in bm["bars"] for x in b["beats"]})
    tap_pts = [((beats[i] + beats[i + 1]) / 2, 60.0 / (beats[i + 1] - beats[i]))
               for i in range(len(beats) - 1)
               if 0.02 < beats[i + 1] - beats[i] < 2.0]
    tapped = _ema(_resample(tap_pts, n), rate, 0.9)

    # ── bar and beat position ──────────────────────────────────────────────
    bar_no, beat_no = [0] * n, [0] * n
    bar_times = [(b["sec"], b["bar"], b["beats"]) for b in bm["bars"]]
    downbeats = []
    k = 0
    for i in range(n):
        t = i / rate
        while k + 1 < len(bar_times) and bar_times[k + 1][0] <= t:
            k += 1
        sec0, num, bts = bar_times[k]
        bar_no[i] = num
        beat_no[i] = sum(1 for x in bts if x <= t)
    for sec0, num, _ in bar_times:
        if 0 <= sec0 <= dur:
            downbeats.append(sec0)
    # a phrase is four bars; those are the downbeats worth announcing
    phrases = [bar_times[i][0] for i in range(len(bar_times))
               if bar_times[i][1] % 4 == 0 and 0 <= bar_times[i][0] <= dur]

    # ── the mix, summed from the stems ─────────────────────────────────────
    step = max(1, env["rate"] // rate)
    mix = [[0.0] * n for _ in range(nb)]
    for tr in env["tracks"].values():
        for b, bn in enumerate(band_names):
            src = tr.get("bands", {}).get(bn, [])
            for i in range(n):
                q = i * step
                if q < len(src):
                    mix[b][i] += src[q]
    peak_band = max((max(m) if m else 1.0) for m in mix) or 1.0
    mixn = [[v / peak_band for v in m] for m in mix]

    loud, cen, spread_, flux_ = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
    prev = None
    for i in range(n):
        row = [mixn[b][i] for b in range(nb)]
        pw = sum(K_WEIGHT[b] * row[b] * row[b] for b in range(nb))
        loud[i] = 10.0 * math.log10(pw + 1e-9)
        tot = sum(row) or 1e-9
        cen[i] = sum(row[b] * b for b in range(nb)) / tot / max(1, nb - 1)
        pr = [r / tot for r in row]
        spread_[i] = -sum(x * math.log(x + 1e-9) for x in pr) / math.log(nb)
        flux_[i] = 0.0 if prev is None else min(
            1.0, sum(max(0.0, row[b] - prev[b]) for b in range(nb)) / tot)
        prev = row
    ref = sorted(loud)[int(n * 0.95)]
    loud = [round(x - ref, 2) for x in loud]           # 0 = the song's loudest

    # the target curve: this song's own long-term average spectrum
    target = [round(sum(mixn[b]) / n, 4) for b in range(nb)]
    tsum = sum(target) or 1e-9
    target = [round(x / tsum, 4) for x in target]
    dev = [0.0] * n                                   # deviation from that target
    for i in range(n):
        row = [mixn[b][i] for b in range(nb)]
        tot = sum(row) or 1e-9
        dev[i] = sum(abs(row[b] / tot - target[b]) for b in range(nb))

    # crest: a proxy, from stem peak against stem rms
    crest = [0.0] * n
    for i in range(n):
        q = i * step
        pk = mx = 0.0
        for tr in env["tracks"].values():
            P, R = tr["peak"], tr["rms"]
            if q < len(P):
                pk = max(pk, P[q])
                mx += R[q] * R[q]
        mx = math.sqrt(mx)
        crest[i] = round(20.0 * math.log10((pk + 1e-6) / (mx + 1e-6)), 2)

    # ── harmony, from every MIDI track at once ─────────────────────────────
    allnotes = sorted(x for v in notes.values() if len(v) >= MIN_NOTES for x in v)
    chords, changes = [], []
    last = None
    ons = [x[0] for x in allnotes]
    for i in range(0, n, max(1, rate // 6)):          # 6 Hz is plenty for chords
        t = i / rate
        hi = bisect.bisect_right(ons, t)
        live = [(p, v) for on, off, p, v in allnotes[max(0, hi - 96):hi] if on <= t < off]
        if not live:
            continue
        pcs = frozenset(p % 12 for p, _ in live)
        nm = name_chord(set(pcs), min(p for p, _ in live) % 12)
        if nm and nm != last:
            chords.append([round(t, 3), nm])
            changes.append(t)
            last = nm

    sec_times = [s["start_sec"] for s in sections if 0 <= s["start_sec"] <= dur]

    panel = {
        "tempo": {"bpm": [round(x, 2) for x in bpm],
                  "tapped": [round(x, 2) for x in tapped],
                  "lo": round(min(bpm), 1), "hi": round(max(bpm), 1)},
        "grid": {"bar": bar_no, "beat": beat_no,
                 "bars_total": max(bar_no) if bar_no else 0},
        "mix": {"bands": [[round(v, 4) for v in m] for m in mixn],
                "target": target,
                "loud": loud, "centroid": [round(x, 3) for x in cen],
                "spread": [round(x, 3) for x in spread_],
                "flux": [round(x, 3) for x in flux_],
                "crest": crest, "deviation": [round(x, 4) for x in dev]},
        "chords": chords,
    }
    panel["readouts"] = [
        {"id": "tempo", "label": "TEMPO", "unit": "BPM",
         "interest": novelty(bpm, rate, 0.25, 4.0)},
        {"id": "tonal", "label": "TONAL BALANCE", "unit": "",
         "interest": novelty(dev, rate, 0.4, 6.0)},
        {"id": "loud", "label": "LOUDNESS", "unit": "dB rel",
         "interest": novelty(loud, rate, 0.5, 7.0)},
        {"id": "crest", "label": "CREST", "unit": "dB",
         "interest": novelty(crest, rate, 0.5, 7.0)},
        {"id": "chord", "label": "HARMONY", "unit": "",
         "interest": event_interest(changes, n, rate, 1.4)},
        {"id": "bar", "label": "BAR", "unit": "",
         "interest": event_interest(phrases, n, rate, 1.1)},
        {"id": "section", "label": "SECTION", "unit": "",
         "interest": event_interest(sec_times, n, rate, 3.0)},
    ]
    return panel



# ═══════════════════════════════════════════════════════════════════════════
# VISEMES — what the mouth is doing
#
# There is no phoneme aligner here and no need for one: the lyric sheet is
# timed to real vocal onsets already, so the word boundaries are right. What
# is missing is what happens INSIDE a word, and English spelling is a good
# enough guide to that if you only need a mouth shape rather than a
# transcription.
#
# Each grapheme maps to four lip numbers — how open, how wide, how rounded,
# how much teeth — and a separate tongue gesture describes how visible the
# tongue is and whether the articulation is front/dental, alveolar, neutral,
# or back/velar. A word is a sequence of those distributed across its own span,
# with vowels given more of the time because that is where the duration
# actually goes. The result is not a phonetic transcription and should not be
# read as one. It is a puppet, and it is right often enough to look like
# someone singing.
# ═══════════════════════════════════════════════════════════════════════════

#                     open  wide  round teeth  weight
VISEME = {
    "a":   (0.95, 0.78, 0.05, 0.00, 1.6),
    "aa":  (1.00, 0.80, 0.05, 0.00, 1.9),
    "ai":  (0.80, 0.90, 0.05, 0.10, 1.8),
    "e":   (0.55, 0.95, 0.00, 0.20, 1.5),
    "ea":  (0.60, 0.95, 0.00, 0.15, 1.8),
    "ee":  (0.35, 1.00, 0.00, 0.30, 1.8),
    "i":   (0.42, 0.90, 0.00, 0.25, 1.4),
    "o":   (0.75, 0.18, 0.92, 0.00, 1.6),
    "oo":  (0.40, 0.08, 1.00, 0.00, 1.8),
    "ou":  (0.65, 0.15, 0.95, 0.00, 1.8),
    "ow":  (0.70, 0.20, 0.90, 0.00, 1.8),
    "oi":  (0.65, 0.55, 0.60, 0.05, 1.8),
    "u":   (0.48, 0.12, 0.92, 0.00, 1.5),
    "y":   (0.45, 0.85, 0.05, 0.20, 1.2),
    # consonants
    "m":   (0.02, 0.48, 0.15, 0.00, 0.7),
    "b":   (0.05, 0.50, 0.15, 0.00, 0.6),
    "p":   (0.04, 0.50, 0.15, 0.00, 0.6),
    "f":   (0.18, 0.62, 0.05, 0.90, 0.8),
    "v":   (0.18, 0.62, 0.05, 0.85, 0.8),
    "th":  (0.26, 0.72, 0.00, 0.80, 0.9),
    "s":   (0.14, 0.88, 0.00, 0.88, 0.9),
    "z":   (0.16, 0.86, 0.00, 0.85, 0.9),
    "sh":  (0.34, 0.34, 0.70, 0.40, 1.0),
    "ch":  (0.32, 0.36, 0.68, 0.45, 0.9),
    "j":   (0.32, 0.40, 0.62, 0.40, 0.9),
    "t":   (0.28, 0.70, 0.05, 0.45, 0.6),
    "d":   (0.30, 0.68, 0.05, 0.40, 0.6),
    "n":   (0.26, 0.66, 0.05, 0.35, 0.7),
    "l":   (0.38, 0.62, 0.05, 0.30, 0.9),
    "r":   (0.40, 0.34, 0.58, 0.10, 1.0),
    "w":   (0.30, 0.10, 0.95, 0.00, 1.0),
    "k":   (0.36, 0.56, 0.10, 0.10, 0.6),
    "g":   (0.36, 0.56, 0.10, 0.10, 0.6),
    "h":   (0.45, 0.55, 0.10, 0.00, 0.5),
    "c":   (0.32, 0.62, 0.08, 0.30, 0.6),
    "q":   (0.30, 0.12, 0.92, 0.00, 0.6),
    "x":   (0.20, 0.80, 0.00, 0.70, 0.8),
}
DIGRAPHS = ("th", "sh", "ch", "ph", "wh", "ck", "ng", "qu",
            "oo", "ee", "ea", "ou", "ow", "oi", "oy", "ai", "ay", "au", "aw")
DIGRAPH_AS = {"ph": "f", "wh": "w", "ck": "k", "ng": "n", "qu": "w",
              "oy": "oi", "ay": "ai", "au": "ow", "aw": "ow"}
# How much tongue to show, and where its tip/body sits: +1 is at the teeth,
# 0 is central, -1 is retracted. Dental /th/, alveolar /t d n l s z/, and
# velar /k g/ are deliberately distinct; vowels carry only a low interior
# suggestion so the tongue reads as articulation, not a permanent extra lip.
TONGUE = {
    "th": (1.00, 0.92),
    "l":  (0.88, 0.76),
    "t":  (0.54, 0.68), "d": (0.54, 0.68), "n": (0.48, 0.64),
    "s":  (0.34, 0.58), "z": (0.34, 0.58),
    "r":  (0.46, -0.05),
    "sh": (0.24, 0.18), "ch": (0.28, 0.22), "j": (0.28, 0.20),
    "k":  (0.38, -0.76), "g": (0.38, -0.76),
    "a":  (0.12, -0.10), "aa": (0.14, -0.12),
    "e":  (0.12, 0.42), "ea": (0.12, 0.46), "ee": (0.12, 0.52),
    "i":  (0.10, 0.48), "y": (0.10, 0.42),
    "o":  (0.10, -0.42), "oo": (0.10, -0.52),
    "ou": (0.10, -0.46), "ow": (0.10, -0.44), "u": (0.10, -0.50),
}
REST = (0.06, 0.50, 0.20, 0.00, 0.00, 0.00)  # mouth between phrases


def spell_visemes(word):
    """A word -> (open, wide, round, teeth, tongue, tongue_pos, weight)."""
    w = "".join(c for c in word.lower() if c.isalpha())
    out, i = [], 0
    while i < len(w):
        two = w[i:i + 2]
        if two in DIGRAPHS:
            key = DIGRAPH_AS.get(two, two)
            i += 2
        else:
            key = w[i]
            i += 1
        # a trailing silent e mostly just opens the vowel before it
        if key == "e" and i >= len(w) and len(out) > 1:
            continue
        v = VISEME.get(key)
        if v:
            tongue, tongue_pos = TONGUE.get(key, (0.0, 0.0))
            out.append((*v[:4], tongue, tongue_pos, v[4]))
    if out:
        return out
    v = VISEME["a"]
    tongue, tongue_pos = TONGUE["a"]
    return [(*v[:4], tongue, tongue_pos, v[4])]


def mouth_track(words, rate, n, dur):
    """Words -> six continuous articulation series on the export grid.

    Each word gets the span up to the next word (capped, so a gap between
    phrases returns the mouth to rest rather than holding the last shape for
    four seconds). Within that span the visemes take time in proportion to
    their weight — vowels get most of it, stops get very little, which is
    roughly how singing works.

    Then the whole thing is followed with a short time constant, because a
    real mouth has mass: it cannot snap between shapes, and the smoothing is
    what stops this reading as a flicker book.
    """
    tgt = [list(REST) for _ in range(n)]
    for k, (wt, text) in enumerate(words):
        nxt = words[k + 1][0] if k + 1 < len(words) else wt + 0.45
        span = min(max(0.10, nxt - wt), 0.95)
        vs = spell_visemes(text)
        tot = sum(v[6] for v in vs) or 1.0
        acc = 0.0
        for v in vs:
            t0 = wt + span * (acc / tot)
            acc += v[6]
            t1 = wt + span * (acc / tot)
            i0, i1 = int(t0 * rate), max(int(t0 * rate) + 1, int(t1 * rate))
            for i in range(max(0, i0), min(n, i1)):
                tgt[i] = list(v[:6])
    # mass: the mouth follows, it does not jump
    out = [[0.0] * n for _ in range(6)]
    cur = list(REST)
    k = 1.0 - math.exp(-1.0 / (rate * 0.055))
    for i in range(n):
        for c in range(6):
            cur[c] += (tgt[i][c] - cur[c]) * k
            out[c][i] = round(cur[c], 4)
    return {"open": out[0], "wide": out[1], "round": out[2], "teeth": out[3],
            "tongue": out[4], "tongue_pos": out[5]}


VOCAL_SIGNAL_RATE = 720


def vocal_signal(project, filename, delta, dur, rate=VOCAL_SIGNAL_RATE):
    """Actual lead-vocal waveform, aligned to mix time and safe to animate.

    The renderer only needs the part of the waveform it can turn into visible
    motion. Band-limit the real stem to 55–280 Hz, then sample it at the same
    effective rate as a 30 fps / blur-x24 render. This preserves polarity and
    cycle-to-cycle irregularity — it is the singer, not a sine oscillator —
    without feeding ultrasonic aliases into temporal supersampling.

    Values are signed bytes in JSON. At roughly 150k samples for this record,
    that is enough temporal detail for the lips while remaining a small part
    of stage/data.json.
    """
    if not zipfile.is_zipfile(project):
        raise ValueError(f"waveform extraction needs a packed DAWproject: {project}")
    with tempfile.TemporaryDirectory() as td, zipfile.ZipFile(project) as z:
        member = next((p for p in z.namelist()
                       if pathlib.PurePosixPath(p).name == filename), None)
        if not member:
            raise FileNotFoundError(f"{filename} is not embedded in {project.name}")
        z.extract(member, td)
        wav = pathlib.Path(td) / member
        cmd = [
            "ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1",
            "-af", "highpass=f=55:poles=2,lowpass=f=280:poles=2",
            "-ar", str(rate), "-f", "s16le", "-",
        ]
        raw = subprocess.run(cmd, capture_output=True, check=True).stdout

    pcm = array.array("h")
    pcm.frombytes(raw[:len(raw) // 2 * 2])
    if sys.byteorder != "little":
        pcm.byteswap()

    total = int(dur * rate) + 2
    shift = round(delta * rate)       # stem_time = mix_time + delta
    aligned = [pcm[i + shift] if 0 <= i + shift < len(pcm) else 0
               for i in range(total)]
    active = sorted(abs(v) for v in aligned if abs(v) > 32)
    ref = active[min(len(active) - 1, int(len(active) * 0.985))] \
        if active else 32767
    ref = max(256, ref)
    drive = 1.18
    denom = math.tanh(drive)
    signal = [max(-127, min(127,
                  round(127 * math.tanh(drive * v / ref) / denom)))
              for v in aligned]
    print(f"  vocal waveform {rate} Hz × {len(signal)} samples  "
          f"55–280 Hz  ref {ref}")
    return signal


# ═══════════════════════════════════════════════════════════════════════════
# SECTION PALETTES
#
# An archetype was a set of behaviours; now it is also a set of colours. Each
# one gets its own hue family, chosen so that neighbouring sections in this
# song read as a change of register rather than a change of hue for its own
# sake — verses cool and narrow, choruses warm and wide, the turn hostile, the
# unravel desaturated and drifting.
#
# `intro` is the effect that introduces the section: the renderer plays it
# across the whole frame at the boundary. Names match the effects in stage.py.
# ═══════════════════════════════════════════════════════════════════════════
# `bg` is the colour of the air itself — a wide radial wash behind everything,
# `bg2` the deeper edge it falls off into. These are what actually make a
# chorus feel like a chorus from across the room, before you have read a
# single element in the frame. They are held deliberately dark: the beams are
# additive, so a bright background does not tint the picture, it erases it.
PALETTE = {
    "emerge":   {"hues": [0.52, 0.58, 0.46, 0.62, 0.50, 0.66],
                 "sat": 0.62, "val": 0.52, "intro": "iris",
                 "bg": [0.020, 0.062, 0.090], "bg2": [0.004, 0.012, 0.028]},
    "drive":    {"hues": [0.06, 0.55, 0.94, 0.12, 0.60, 0.02],
                 "sat": 0.74, "val": 0.55, "intro": "sweep",
                 "bg": [0.028, 0.030, 0.086], "bg2": [0.010, 0.006, 0.026]},
    "bloom":    {"hues": [0.90, 0.04, 0.12, 0.86, 0.08, 0.96],
                 "sat": 0.80, "val": 0.60, "intro": "rings",
                 "bg": [0.082, 0.022, 0.050], "bg2": [0.026, 0.004, 0.016]},
    "hold":     {"hues": [0.48, 0.44, 0.54, 0.40, 0.58, 0.36],
                 "sat": 0.48, "val": 0.48, "intro": "fade",
                 "bg": [0.014, 0.048, 0.046], "bg2": [0.004, 0.014, 0.014]},
    "surge":    {"hues": [0.10, 0.02, 0.14, 0.96, 0.06, 0.18],
                 "sat": 0.86, "val": 0.62, "intro": "burst",
                 "bg": [0.094, 0.040, 0.011], "bg2": [0.032, 0.009, 0.003]},
    "rupture":  {"hues": [0.00, 0.02, 0.98, 0.05, 0.01, 0.97],
                 "sat": 0.92, "val": 0.58, "intro": "shock",
                 "bg": [0.140, 0.012, 0.016], "bg2": [0.048, 0.002, 0.006]},
    "dissolve": {"hues": [0.72, 0.66, 0.78, 0.60, 0.84, 0.56],
                 "sat": 0.38, "val": 0.50, "intro": "scatter",
                 "bg": [0.058, 0.036, 0.098], "bg2": [0.018, 0.010, 0.034]},
}



# ═══════════════════════════════════════════════════════════════════════════
# THE DIRECTOR
#
# Ranking actors by salience every frame is not direction, it is a meter. It
# gives the stage to whatever is loudest, which means the same two players
# hold it for three minutes and the viewer stops looking. A director decides
# in ADVANCE, and decides for reasons a meter does not have:
#
#   EXPOSITION   an actor that has never had the stage gets it, properly,
#                once — introduced, held long enough to be understood, then
#                moved aside. Novelty is worth more than volume.
#   FATIGUE      holding the lead costs you. Every consecutive window a player
#                keeps the stage, its score drops, so the show hands over
#                before the eye gets tired rather than after.
#   HYSTERESIS   a lead is held for a minimum span. Nothing is worse than two
#                players trading the frame every two bars.
#   DEPTH        exactly one lead, at most one support. Everyone else is
#                background — small, back, and quiet — or gone. Competition
#                for the centre is what makes a frame unreadable.
#   REWARD       a scattering of brief peripheral cameos, scheduled when the
#                lead is stable enough to spare the attention. They are not
#                meant to be caught on a first viewing.
#
# The plan is computed on a four-bar grid, which is the shortest unit that
# reads as a phrase in this song, and emitted as a role per sample so the
# renderer only has to look it up.
# ═══════════════════════════════════════════════════════════════════════════

OFF, BACKGROUND, SUPPORT, LEAD = 0, 1, 2, 3
MIN_LEAD_WINDOWS = 2          # never hand the stage over faster than this
FATIGUE = 0.115               # score lost per consecutive window in the lead
DEBUT_BONUS = 0.42            # what an unseen actor is worth over a loud one
RETURN_BONUS = 0.16           # ... and a player who has been away a while
SUPPORT_FLOOR = 0.30
BACKGROUND_FLOOR = 0.16
GATE_VETO = 0.55        # below this a player is too quiet to be cast at all
ATTENTION_SILENCE = 1.10
ATTENTION_PRE = 0.42
ATTENTION_HOLD = 1.05


def attention_cues(actors, beats, rate, dur):
    """Find real entrances that deserve a brief, pulse-timed spotlight.

    MIDI actors use their exact note-ons. Audio actors use the first audible
    sample after a genuine silence, snapped to the nearest beat only when it
    is already close. This is intentionally event-sized rather than another
    phrase plan: the four-bar director still decides the lasting hierarchy;
    these cues make the eye notice a player arriving before that hierarchy
    resumes.
    """
    events = []

    def nearest_beat(t):
        if not beats:
            return t
        i = bisect.bisect_left(beats, t)
        cand = beats[max(0, i - 1):min(len(beats), i + 1)]
        best = min(cand, key=lambda x: abs(x - t)) if cand else t
        return best if abs(best - t) <= 0.14 else t

    for name, act in actors.items():
        if act["figure"] == "comb":
            continue
        sal = act.get("salience", [])
        notes = act.get("notes") or []
        times = []
        if notes:
            last_end = -99.0
            for on, length, _pitch, vel in notes:
                if vel > 0.20 and on - last_end >= ATTENTION_SILENCE:
                    times.append(on)       # exact performance time: do not quantise it
                last_end = max(last_end, on + length)
        else:
            amp, attack = act.get("amp", []), act.get("attack", [])
            last_live = -int(99 * rate)
            for i, level in enumerate(amp):
                atk = attack[i] if i < len(attack) else 0.0
                live = level > 0.085 or atk > 0.26
                if live:
                    if i - last_live >= int(ATTENTION_SILENCE * rate):
                        times.append(nearest_beat(i / rate))
                    last_live = i

        # A chattering threshold must not create repeat introductions. The
        # silence test above is the main guard; this two-second spacing is the
        # final deterministic one.
        keep = []
        for t in times:
            if 0.6 <= t <= dur - 0.35 and (not keep or t - keep[-1] >= 2.0):
                keep.append(t)
        for t in keep:
            i = min(len(sal) - 1, max(0, round(t * rate))) if sal else 0
            events.append({"t": t, "actor": name,
                           "score": sal[i] if sal else 0.0})

    # If several players enter on the same pulse, give the single strongest
    # arrival the look. Two simultaneous leads would defeat the purpose.
    events.sort(key=lambda x: (x["t"], -x["score"], x["actor"]))
    out = []
    for e in events:
        if out and e["t"] - out[-1]["t"] < 0.22:
            if e["score"] > out[-1]["score"]:
                out[-1] = e
            continue
        out.append(e)
    return [{"t": round(e["t"], 4), "pre": ATTENTION_PRE,
             "dur": ATTENTION_HOLD, "actor": e["actor"]} for e in out]


def direct(actors, bars, beats, rate, n, dur):
    """Plan the whole performance. -> per-actor role series, plus the cue sheet."""
    names = [k for k, v in actors.items() if v["figure"] != "comb"]
    kit = [k for k, v in actors.items() if v["figure"] == "comb"]
    if not names:
        return {"roles": {}, "cues": [], "debuts": {}, "eggs": []}

    # four-bar windows, from the real bar grid
    edges = [b["t"] for b in bars if 0 <= b["t"] <= dur]
    win = [(edges[i], edges[min(len(edges) - 1, i + 4)])
           for i in range(0, len(edges) - 1, 4)]
    win = [(a, b) for a, b in win if b > a + 0.5]

    def mean_sal(name, t0, t1):
        v = actors[name]["salience"]
        i0, i1 = int(t0 * rate), max(int(t0 * rate) + 1, int(t1 * rate))
        seg = v[max(0, i0):min(len(v), i1)]
        return sum(seg) / len(seg) if seg else 0.0

    def mean_gate(name, t0, t1):
        v = actors[name].get("gate")
        if not v:
            return 1.0
        i0, i1 = int(t0 * rate), max(int(t0 * rate) + 1, int(t1 * rate))
        seg = v[max(0, i0):min(len(v), i1)]
        return sum(seg) / len(seg) if seg else 1.0

    led = {k: 0 for k in names}        # windows spent leading, ever
    last_seen = {k: -99 for k in names}
    run = 0
    cur_lead = None
    cues, debuts, eggs = [], {}, []
    plan = []                          # (t0, t1, {name: role})

    for wi, (t0, t1) in enumerate(win):
        # A player who is silent for most of a window cannot lead it. This
        # started life as a weighting, which was not enough — a high-salience
        # part could still be cast as the lead across a stretch where the gate
        # had it muted, and the result was a stage with nobody downstage on it.
        # It is a veto now.
        gate_w = {k: mean_gate(k, t0, t1) for k in names}
        base = {k: (mean_sal(k, t0, t1) if gate_w[k] >= GATE_VETO else 0.0)
                for k in names}
        score = {}
        for k in names:
            sc = base[k]
            if led[k] == 0:
                sc += DEBUT_BONUS                       # never had the stage
            elif wi - last_seen[k] > 6:
                sc += RETURN_BONUS                      # been away a while
            if k == cur_lead:
                sc -= FATIGUE * run                     # you have had it a while
            score[k] = sc
        order = sorted(names, key=lambda k: -score[k])
        eligible = [k for k in order if gate_w[k] >= GATE_VETO]
        want = eligible[0] if eligible else order[0]

        # hold the lead — unless the incumbent has gone quiet, in which case
        # holding it means holding an empty stage
        if (cur_lead is not None and want != cur_lead and run < MIN_LEAD_WINDOWS
                and gate_w.get(cur_lead, 1.0) >= GATE_VETO):
            want = cur_lead                             # not yet
        if want == cur_lead:
            run += 1
        else:
            if want not in debuts and led[want] == 0:
                debuts[want] = round(t0, 3)
            cur_lead, run = want, 1
        led[cur_lead] += 1
        last_seen[cur_lead] = wi

        roles = {k: OFF for k in names}
        roles[cur_lead] = LEAD
        sup = next((k for k in eligible if k != cur_lead
                    and base[k] > SUPPORT_FLOOR), None)
        if sup:
            roles[sup] = SUPPORT
            last_seen[sup] = wi
        for k in names:
            if roles[k] == OFF and base[k] > BACKGROUND_FLOOR:
                roles[k] = BACKGROUND

        # a reward for looking away from the middle: every so often, when the
        # lead is settled, someone who is otherwise off appears briefly at the
        # edge of frame. Deterministic, so it survives a re-render.
        if wi % 4 == 2:
            cand = [k for k in order if roles[k] == OFF]
            if cand:
                who = cand[wi % len(cand)]
                eggs.append({"t": round(t0 + (t1 - t0) * 0.42, 3),
                             "dur": 1.7, "actor": who})

        plan.append((t0, t1, roles))
        cues.append({"t0": round(t0, 3), "t1": round(t1, 3), "lead": cur_lead,
                     "support": sup or "", "run": run})

    # Anyone the plan never featured gets their best window taken from whoever
    # had it. An actor that appears in the mix and never once gets the frame is
    # a hole in the show, not a decision.
    for k in names:
        if led[k]:
            continue
        best = max(range(len(plan)),
                   key=lambda i: mean_sal(k, plan[i][0], plan[i][1])
                   * (1.0 if mean_gate(k, plan[i][0], plan[i][1]) >= GATE_VETO else 0.0))
        t0, t1, roles = plan[best]
        for other in roles:
            if roles[other] == LEAD:
                roles[other] = SUPPORT
        roles[k] = LEAD
        debuts[k] = round(t0, 3)
        cues[best]["lead"] = k
        cues[best]["forced"] = True

    # -> a role per sample, plus the drum kit which is the room and always on
    roles_out = {k: [OFF] * n for k in names}
    for t0, t1, roles in plan:
        i0, i1 = int(t0 * rate), min(n, int(t1 * rate))
        for k, r in roles.items():
            for i in range(max(0, i0), i1):
                roles_out[k][i] = r
    for e in eggs:
        k = e["actor"]
        i0 = int(e["t"] * rate)
        for i in range(max(0, i0), min(n, i0 + int(e["dur"] * rate))):
            if roles_out[k][i] == OFF:
                roles_out[k][i] = BACKGROUND
    for k in kit:
        roles_out[k] = [BACKGROUND] * n

    return {"roles": roles_out, "cues": cues, "debuts": debuts, "eggs": eggs,
            "spotlights": attention_cues(actors, beats, rate, dur),
            "windows": len(win)}



# ═══════════════════════════════════════════════════════════════════════════
# LINER NOTES
#
# Eight annotations across three and a half minutes, aimed squarely at
# somebody who opens DAWs for a living. The rule I set myself: every one has
# to be a fact this file can actually compute from the project — no
# hand-typed numbers that drift out of date the next time the arrangement
# changes — and every one has to land at a moment where you can SEE the thing
# it is describing. A note about a tempo ramp lands on the tempo ramp.
#
# Eight is the budget. There is a version of this feature that annotates
# everything and turns the piece into a lecture; the interesting one is
# closer to a good sleeve note, where somebody points at four or five things
# and then leaves you alone.
#
# Anything that cannot be computed is dropped rather than guessed at.
# ═══════════════════════════════════════════════════════════════════════════

def liner_notes(root, bm, env, panel, actors, lanes, chords, markers, dur):
    out = []

    def add(t, head, body, hold=5.6):
        if 12.0 < t < dur - 22.0:
            out.append({"t": round(t, 3), "dur": hold, "head": head, "body": body})

    # ── the cue markers ARE the lyric sheet ────────────────────────────────
    nm = len(markers)
    if nm > 20:
        add(19.5, "TIMING",
            f"The lyric sheet is {nm} cue markers dropped into the arrangement. "
            f"Lines come from those. The words inside them are placed on the "
            f"vocal's own onsets.")

    # ── the part that plays through everything ────────────────────────────
    best = None
    for name, a in actors.items():
        ns = a.get("notes") or []
        if len(ns) < 40:
            continue
        span = ns[-1][0] - ns[0][0]
        if best is None or span > best[1]:
            best = (name, span, ns)
    if best:
        name, span, ns = best
        pits = [x[2] for x in ns]
        longest = max(x[1] for x in ns)
        add(31.9, name.upper(),
            f"{len(ns)} notes over {span:.0f} seconds — the only part that plays "
            f"the whole record. {max(pits) - min(pits)} semitones of range, "
            f"longest note {longest:.1f}s.")

    # ── what is actually on the master ────────────────────────────────────
    plugs = []
    for d in root.iter():
        if d.tag in ("Vst3Plugin", "ClapPlugin"):
            n = d.get("deviceName") or d.get("name") or ""
            if n and n not in plugs:
                plugs.append(n)
    # the mastering and metering plugins are the interesting ones to name —
    # a channel strip is a channel strip, but Tonal Balance and Insight on the
    # master is somebody who was watching the spectrum while they worked
    PRIORITY = ("Ozone", "Tonal Balance", "Insight", "Neutron")
    izo = sorted([x for x in plugs if any(k in x for k in PRIORITY)],
                 key=lambda x: next(i for i, k in enumerate(PRIORITY) if k in x))
    if len(izo) >= 3:
        add(68.5, "ON THE MASTER",
            ", ".join(izo[:3]) + (f" and {len(izo) - 3} more. " if len(izo) > 3
                                  else ". ") +
            "The panel on this stage is reading the same spectrum they are.")

    # ── tempo: automated, not quantised ───────────────────────────────────
    tm = bm.get("tempo_map", [])
    bpm = panel["tempo"]["bpm"]
    tap = panel["tempo"]["tapped"]
    if len(tm) > 100 and bpm:
        rate = 30
        W = int(4 * rate)
        worst, wt = 0.0, 0.0
        for i in range(0, len(bpm) - W, 5):
            dv = bpm[i + W] - bpm[i]
            if abs(dv) > abs(worst):
                worst, wt = dv, i / rate
        add(max(14.0, wt - 0.4), "TEMPO",
            f"{len(tm)} linear tempo points, {min(bpm):.0f} to {max(bpm):.0f} BPM. "
            f"This ramp moves {abs(worst):.0f} BPM in four seconds. Tap along and "
            f"you would still call it {(min(tap) + max(tap)) / 2:.0f}.")

    # ── a part that appears once and never returns ────────────────────────
    cameo = None
    for name, a in actors.items():
        ns = a.get("notes") or []
        if not (10 <= len(ns) <= 80):
            continue
        span = ns[-1][0] - ns[0][0]
        if ns[-1][0] > dur - 45 or span > 70:
            continue
        if cameo is None or span < cameo[1]:
            cameo = (name, span, ns)
    if cameo:
        name, span, ns = cameo
        fmt = "a CLAP plugin" if any(d.tag == "ClapPlugin" and
                                     (d.get("deviceName") or "") in name
                                     for d in root.iter()) else "one instrument"
        add(ns[0][0] + 0.4, name.upper(),
            f"{fmt}, {len(ns)} notes across {span:.0f} seconds — and then it "
            f"never plays again.")

    # ── the harmony is smaller than it sounds ─────────────────────────────
    if len(chords) > 30:
        hist = {}
        for _, nm2 in chords:
            hist[nm2] = hist.get(nm2, 0) + 1
        top = sorted(hist.items(), key=lambda x: -x[1])[:3]
        share = sum(v for _, v in top) / len(chords)
        add(129.5, "HARMONY",
            f"{len(chords)} chord changes, {len(hist)} distinct shapes. "
            f"{', '.join(k for k, _ in top)} account for "
            f"{share * 100:.0f}% of them.")

    # ── the fastest automation move in the project ────────────────────────
    fast = None
    for l in lanes:
        if l["dead"] or l["label"] != "Send":
            continue
        dt_ = l["t1"] - l["t0"]
        rng = l["hi"] - l["lo"]
        if dt_ < 2.0 and rng > 0.8 and (fast is None or dt_ < fast["t1"] - fast["t0"]):
            fast = l
    if fast:
        add(fast["t0"] - 0.3, "SEND",
            f"The {fast['track']} send goes from nothing to full in "
            f"{fast['t1'] - fast['t0']:.1f} seconds. "
            f"{fast['n_points']} breakpoints, and that is the whole move.")

    # ── the room opening at the end ───────────────────────────────────────
    rv = [l for l in lanes if not l["dead"] and "raum" in l["track"].lower()
          and l["label"] in ("Decay", "Feedback")]
    if rv:
        t0 = min(l["t0"] for l in rv if l["t0"] > 10) if any(
            l["t0"] > 10 for l in rv) else min(l["t0"] for l in rv)
        add(max(t0 + 18.0, dur - 30.0), "RAUM",
            f"Decay and feedback start climbing at {int(t0)//60}:{int(t0)%60:02d} "
            f"and never come back down. The room opens for the last "
            f"{dur - t0:.0f} seconds of the record.")

    out.sort(key=lambda x: x["t"])
    # never let two overlap
    keep = []
    for nt in out:
        if keep and nt["t"] < keep[-1]["t"] + keep[-1]["dur"] + 2.0:
            continue
        keep.append(nt)
    return keep


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rate", type=int, default=30, help="grid rate for every series")
    ap.add_argument("-o", "--out", type=pathlib.Path,
                    default=ROOT / "stage" / "data.json")
    a = ap.parse_args()

    bm = load(ROOT / "analysis" / "beatmap.json")
    env = load(ROOT / "analysis" / "envelopes.json")
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    try:
        lyrics = load(ROOT / "analysis" / "lyrics.json")["lines"]
    except FileNotFoundError:
        lyrics = []
    style_path = ROOT / "shots" / "stage_style.json"
    style = load(style_path) if style_path.exists() else DEFAULT_STYLE

    dur = bm["duration_sec"]
    rate = a.rate
    n = int(dur * rate) + 2
    band_names = env.get("bands", [])

    # --- the DAWproject: notes and automation -------------------------------
    proj = next(iter(sorted((ROOT / "source").glob("*.dawproject"))), None) \
        or (ROOT / "source" / "project.xml")
    root = read_project_xml(proj)
    curve = TempoCurve([(p["beat"], p["bpm"], p.get("interpolation", "linear"))
                        for p in bm["tempo_map"]])
    zero_sec = curve.sec(bm["zero_beat"])
    notes = load_notes(root, curve, zero_sec)
    lanes = load_lanes(root, curve, zero_sec)

    # A lane whose every breakpoint sits before the master clip, or whose
    # value never moves, is not a performance — it is a setting. Mark those
    # dead so the renderer can fall back to a derived feature instead of
    # binding a whole visual channel to something that never moves.
    lane_out = []
    for l in lanes:
        span_dead = l["pts"][-1][0] < 0.05
        flat = abs(max(v for _, v in l["pts"]) - min(v for _, v in l["pts"])) < 1e-4
        lane_out.append({
            "dead": bool(span_dead or flat),
            "track": short(l["track"]) if l["track"] else "",
            "label": l["label"],
            "unit": l["unit"],
            "n_points": len(l["pts"]),
            "t0": round(l["pts"][0][0], 3),
            "t1": round(l["pts"][-1][0], 3),
            "lo": round(min(v for _, v in l["pts"]), 4),
            "hi": round(max(v for _, v in l["pts"]), 4),
            "v": [round(x, 4) for x in resample_lane(l, rate, n)],
        })

    # --- bars, beats, sections ---------------------------------------------
    bars = [{"n": b["bar"], "t": round(b["sec"], 5)} for b in bm["bars"]
            if -0.001 <= b["sec"] <= dur + 4]
    beats = [round(x, 5) for b in bm["bars"] for x in b["beats"]
             if -0.001 <= x <= dur + 1]
    secs = []
    for s in sections:
        name = style.get(s["id"], "drive")
        arch = ARCHETYPES.get(name, ARCHETYPES["drive"])
        pal = PALETTE.get(name, PALETTE["drive"])
        secs.append({"id": s["id"], "arch": name,
                     "hues": pal["hues"], "sat": pal["sat"], "val": pal["val"],
                     "intro": pal["intro"], "bg": pal["bg"], "bg2": pal["bg2"],
                     "t0": round(s["start_sec"], 4), "t1": round(s["end_sec"], 4),
                     "tint": list(arch["tint"]),
                     **{k: arch[k] for k in PARAM_KEYS}})

    # --- the kit ------------------------------------------------------------
    kit = next((v for k, v in env["tracks"].items() if "drum" in k.lower()), None)
    hits = kit_hits(kit, band_names, env["rate"]) if kit else \
        {"kick": [], "snare": [], "hat": []}
    hits = {k: [[round(t, 4), round(m, 3)] for t, m in v if 0 <= t <= dur]
            for k, v in hits.items()}

    # --- the actors ---------------------------------------------------------
    # Match each audio stem to its MIDI track by name, so a figure's shape
    # (from the spectrum) and its skeleton (from the notes) are the same part.
    def match_notes(stem_name):
        s = stem_name.lower()
        best, score = None, 0
        for k in notes:
            ks = short(k).lower()
            w = len(set(ks.split()) & set(s.split()))
            if ks in s or s in ks:
                w += 2
            if w > score:
                best, score = k, w
        return notes.get(best, []) if score else []

    actors = {}
    for name, tr in env["tracks"].items():
        sn = short(name)
        nt = match_notes(sn)
        if len(nt) < MIN_NOTES:
            nt = []
        act = {
            "kind": "audio",
            "figure": figure_for(sn, "audio"),
            "delta": round(tr["delta_sec"], 5),
            **features(tr, band_names, env["rate"], rate, n,
                       tr["delta_sec"]),
            "notes": [[round(on, 4), round(off - on, 4), p, round(v, 3)]
                      for on, off, p, v in nt if -1 <= on <= dur + 1],
        }
        if nt:
            act.update(note_features(nt, rate, n))
        # the six-band profile, kept per-actor: this is what deforms the line
        act["bands"] = {
            b: aligned_series(tr.get("bands", {}).get(b, []), env["rate"],
                              rate, n, tr["delta_sec"])
                        for b in band_names}
        act["salience"], act["lead"] = salience(act["amp"], act["attack"], rate)
        act["gate"] = silence_gate(act["amp"], rate, n)
        actors[sn] = act

    # MIDI tracks are actors in their own right, not decoration on a stem.
    # Three of them carry real parts here, and none of them corresponds to an
    # audio stem — the stems are Suno separations, the MIDI is what was played
    # on top. Giving them their own figures roughly doubles the cast.
    claimed = {n for a in actors.values() for n in ([a.get("_src")] if a.get("_src") else [])}
    for tname, nt in notes.items():
        if len(nt) < MIN_NOTES or tname in claimed:
            continue
        sn = short(tname)
        if sn in actors:
            sn = sn + " (midi)"
        act = {
            "kind": "midi",
            "figure": figure_for(sn, "midi"),
            "delta": 0.0, "norm": 1.0,
            "notes": [[round(on, 4), round(off - on, 4), p, round(v, 3)]
                      for on, off, p, v in nt if -1 <= on <= dur + 1],
            "bands": {},
        }
        act.update(note_features(nt, rate, n))
        # a MIDI part has no spectrum, so amp/attack come from the notes: the
        # envelope of what is sounding, with an attack spike on every onset
        amp, atk = [0.0] * n, [0.0] * n
        a_, k_ = 0.0, 0.0
        ons = [x[0] for x in nt]
        for i in range(n):
            t = i / rate
            live = [(o, d_, p, v) for o, d_, p, v in act["notes"] if o <= t < o + d_]
            tgt = min(1.0, sum(v for *_x, v in live) * 0.55) if live else 0.0
            a_ += (tgt - a_) * 0.30
            nh = bisect.bisect_right(ons, t) - bisect.bisect_left(ons, t - 1.0 / rate)
            k_ = max(k_ * 0.84, min(1.0, nh * 0.9))
            amp[i], atk[i] = round(a_, 3), round(k_, 3)
        act["amp"], act["attack"] = amp, atk
        act["centroid"] = [round(min(1.0, max(0.0, (m - 36) / 52.0)), 3)
                           for m in act["meanpitch"]]
        act["flux"] = act["density"]
        act["spread"] = [round(min(1.0, a / 24.0), 3) for a in act["ambitus"]]
        act["tilt"] = [round(c * 2 - 1, 3) for c in act["centroid"]]
        act["salience"], act["lead"] = salience(act["amp"], act["attack"], rate)
        act["gate"] = silence_gate(act["amp"], rate, n)
        actors[sn] = act

    # --- words --------------------------------------------------------------
    words = []
    try:
        from stage import word_onsets
        vox = next((v for k, v in env["tracks"].items()
                    if "lead vocal" in k.lower()), None)
        if vox and lyrics:
            wmap = word_onsets(lyrics, vox, env["rate"], vox["delta_sec"])
            for ln in lyrics:
                for w, wt in wmap.get(ln["id"], []):
                    words.append([round(wt, 4), w])
            words.sort()
    except Exception as e:                                    # noqa: BLE001
        print(f"  words skipped: {e}")

    panel = build_panel(bm, env, actors, notes, rate, n, dur, band_names, sections)
    mouth = mouth_track(words, rate, n, dur)
    vox = next((v for k, v in env["tracks"].items()
                if "lead vocal" in k.lower()), None)
    if vox:
        try:
            mouth["signal_rate"] = VOCAL_SIGNAL_RATE
            mouth["signal"] = vocal_signal(
                proj, vox["file"], vox["delta_sec"], dur, VOCAL_SIGNAL_RATE)
        except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as e:
            print(f"  vocal waveform skipped: {e}")
    direction = direct(actors, bars, beats, rate, n, dur)

    title = song_title(root, env, bm)
    notes_out = liner_notes(root, bm, env, panel, actors, lane_out,
                            panel["chords"], bm.get("markers", []), dur)

    data = {
        "title": title,
        "liner": notes_out,
        "duration": round(dur, 5), "rate": rate, "n": n,
        "panel": panel,
        "mouth": mouth,
        "direction": direction,
        "bands": band_names, "band_hz": env.get("band_hz", []),
        "bars": bars, "beats": beats, "sections": secs, "hits": hits,
        "actors": actors, "lanes": lane_out,
        "lines": [{"t": round(l["sec"], 4), "t1": round(l["end_sec"], 4),
                   "text": l["text"]} for l in lyrics],
        "words": words,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    save(a.out, data)

    live_lanes = [l for l in lane_out if not l["dead"]]
    print(f"  {len(actors)} actors @ {rate} Hz × {n} samples")
    for sn, act in actors.items():
        extra = (f"{len(act['notes'])} notes" if act["notes"] else "spectrum only")
        sal = act.get("salience", [])
        on = 100.0 * sum(1 for x in sal if x > 0.45) / max(1, len(sal))
        print(f"      {sn:20s} {act['kind']:6s} {act['figure']:10s} {extra:14s}"
              f" in contention {on:4.0f}%")
    print(f"  {len(lane_out)} automation lanes, {len(live_lanes)} of them live")
    for l in lane_out:
        span = f"{l['t0']:7.1f}–{l['t1']:7.1f}s"
        who = (l["track"] or "—")[:18]
        mark = "  " if not l["dead"] else " ×"
        print(f"    {mark}{who:20s} {l['label']:12s} {l['n_points']:3d} pts  {span}"
              f"  [{l['lo']:.2f}..{l['hi']:.2f}]")
    if len(live_lanes) < len(lane_out):
        print("      × = never moves after the master clip starts — the renderer")
        print("          falls back to a derived feature for that channel.")
    print(f"  {sum(len(v) for v in hits.values())} strikes · {len(words)} words")
    nv = sum(len(spell_visemes(w[1])) for w in words)
    talk = 100.0 * sum(1 for x in mouth["open"] if x > 0.18) / max(1, n)
    print(f"  mouth: {nv} visemes from {len(words)} words · "
          f"open {talk:.0f}% of the song")
    print(f"  title: {title!r}")
    print(f"  liner notes: {len(notes_out)}")
    for nt in notes_out:
        print(f"      {int(nt['t'])//60}:{int(nt['t'])%60:02d}  {nt['head']:18s} "
              f"{nt['body'][:58]}...")
    for sn, act in actors.items():
        g = act.get("gate")
        if g:
            off = 100.0 * sum(1 for x in g if x < 0.5) / len(g)
            if off > 1:
                print(f"      {sn:20s} gated off {off:4.0f}% of the song")
    d = data["direction"]
    print(f"  direction: {d['windows']} four-bar windows · "
          f"{len(d['debuts'])} debuts · {len(d['eggs'])} peripheral cameos")
    hold = {}
    for c in d["cues"]:
        hold[c["lead"]] = hold.get(c["lead"], 0) + 1
    for k, v in sorted(hold.items(), key=lambda x: -x[1]):
        deb = d["debuts"].get(k)
        print(f"      {k:20s} leads {v:3d} windows"
              + (f" · debut {deb:6.1f}s" if deb is not None else ""))
    print("  section palettes: " + ", ".join(
        f"{x['id']}={x['arch']}/{x['intro']}" for x in secs[:4]) + " ...")
    pn = data["panel"]
    bp = pn["tempo"]["bpm"]
    tp = pn["tempo"]["tapped"]
    print(f"  panel: {min(bp):.1f}-{max(bp):.1f} BPM written "
          f"({min(tp):.1f}-{max(tp):.1f} as tapped) · "
          f"{pn['grid']['bars_total']} bars · {len(pn['chords'])} chord changes")
    for r in pn["readouts"]:
        iv = r["interest"]
        on = sum(1 for x in iv if x > 0.34) / max(1, len(iv))
        print(f"      {r['label']:15s} on stage {100*on:4.0f}% of the song")
    print(f"  wrote {a.out.relative_to(ROOT)}  "
          f"({a.out.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
