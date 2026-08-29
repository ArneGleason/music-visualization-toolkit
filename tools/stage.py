#!/usr/bin/env python3
"""
"The Stage" — the arrangement as performers who enter, take focus, and leave.

    ./run.sh stage                  whole song, 60fps
    ./run.sh stage turn             one section
    ./run.sh stage turn 30          one section at 30fps (faster to render)

Three layers, back to front:

  * THE ROOM — the drum kit is not a soloist and not a blob. It is the TUNNEL.
    Every kick and snare in the song is detected up front, so each strike can
    launch a ring more than a second EARLY, out at depth, timed to arrive on
    its own beat and then blow past the frame — five or six always in flight,
    receding. Hi-hats never touch the middle: they seed sparks out at the
    periphery that shoot outward and off. And underneath it all the field
    PAINTS THE FRAME. The six-band split separates kick (bottom two bands) from snare
    (crack plus body), and both are read as transients rather than levels —
    a level-follower sits pinned high because cymbals sustain, and the whole
    frame washes out. The field rests at deep indigo, the kick lifts it and
    swells up from below, and a snare strike throws the entire frame to
    process blue for a fifth of a second.
  * THE ARRIVALS — note tracks introduce themselves out of the depth. Not a
    lane and not a game: no guides, no hit line, no impact. Notes gather high
    and shallow when they are far off, fan forward and bow to their own side as
    their moment approaches, swell softly when they sound, then keep going past
    the viewer and dissolve. Rounded capsules, coloured by pitch class, longer
    notes taller.
  * THE PLAYERS — audio stems as SPECTRAL ROSES. Overall size is the track's own
    RMS; the silhouette is its six-band spectrum wrapped around the circle, bass
    at the bottom and air at the top. A kick and a hi-hat are the same instrument
    here and look completely different. Their positions ride a slow 64-second
    orbit, so the stage is never static.

Over the top: TYPE THAT SINGS. Line starts come from the Bitwig markers
(exact) and each WORD is placed on a real attack transient found in the
lead-vocal stem's envelope. But the words do not merely highlight — every
CHARACTER samples that envelope a few milliseconds behind the one before it,
so amplitude travels through the word as a wave. Loud syllables physically
lift their letters and swell them. The singer deforms the type.

Everything composites with real alpha — ImageDraw.Draw(img, "RGBA") — so glows
add light instead of painting the background colour over whatever is behind
them. Blending toward black was what buried the kit and muddied every overlap.

Automation is continuous, not just events: the Raum feedback lane drives visual
feedback (frame trails), the decay lane drives how long ripples live, and send
levels draw a halo on whichever performer is being ridden.

Sections have identity: each carries an archetype from shots/stage_style.json
that sets a background tint and an entrance effect chosen to match what that
section DOES — an iris for something emerging, a flash and shake for a hard
turn, a scatter for something coming apart. Edit that file freely; it is the
creative dial.

Focus = energy weighted by novelty, so nothing sits on stage doing nothing.
Slots are held rather than recomputed, or the whole stage collapses inward.

A listening tool — and deliberately a sketch of the expressiveness each
section wants from the real video.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import colorsys
import math
import pathlib
import random
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load, save  # noqa: E402
from animatic import Grid, font, tc, report_fonts  # noqa: E402
from dawproject import TempoCurve, read_project_xml  # noqa: E402

BG = (10, 11, 14)
INK = (238, 236, 230)
DIM = (96, 104, 112)

PALETTE = [
    (236, 170, 92), (108, 178, 214), (214, 118, 132), (128, 200, 150),
    (176, 148, 224), (232, 210, 120), (120, 208, 208), (222, 138, 96),
]

PITCH_COLORS = [tuple(int(c * 255) for c in colorsys.hsv_to_rgb(i / 12.0, 0.60, 1.0))
                for i in range(12)]

# tracks whose name matches these live in the background layer, not the
# spotlight rotation — a drum kit is the room, not a soloist
BACKGROUND_MATCH = ("drum", "perc")
ORBIT_PERIOD = 64.0        # seconds for one full slow orbit
LOOK_AHEAD = 4.6           # seconds of arrivals visible ahead of "now"

# The kit paints the room rather than sitting in it. Kick lives in the low
# bands, snare in the crack up top, so the six-band split separates them
# without touching the audio again.
INDIGO = (24, 20, 56)
INDIGO_LIFT = (46, 38, 104)      # where the kick pushes it
PROCESS_BLUE = (0, 133, 202)     # where the snare throws it

# Each archetype is a full ATTRIBUTE SET, not just a colour. Every element
# reads its behaviour from here, and the whole set cross-dissolves across a
# section boundary, so two contrasting sections genuinely behave differently
# and the change is a transition rather than a cut.
#
#   glow   halo intensity on the players      gamma  silhouette exaggeration
#   orbit  orbit speed multiplier             spread orbit radius
#   tunnel kick/snare ring strength           sparks hi-hat particle density
#   notes  arrival capsule size               lift   how hard the vocal
#   trail  extra frame feedback                      deforms the type
ARCHETYPES = {
    "emerge":   {"tint": (16, 32, 44), "effect": "iris",
                 "glow": 1.45, "gamma": 1.45, "orbit": 0.45, "spread": 1.22,
                 "tunnel": 0.50, "sparks": 0.55, "notes": 0.90, "lift": 0.70,
                 "trail": 0.35},
    "drive":    {"tint": (30, 24, 19), "effect": "sweep",
                 "glow": 0.90, "gamma": 2.20, "orbit": 1.00, "spread": 1.00,
                 "tunnel": 1.30, "sparks": 1.20, "notes": 1.10, "lift": 1.00,
                 "trail": 0.05},
    "bloom":    {"tint": (40, 24, 34), "effect": "rings",
                 "glow": 1.65, "gamma": 1.80, "orbit": 1.45, "spread": 1.15,
                 "tunnel": 1.00, "sparks": 1.50, "notes": 1.25, "lift": 1.30,
                 "trail": 0.20},
    "hold":     {"tint": (16, 26, 30), "effect": "fade",
                 "glow": 1.10, "gamma": 2.65, "orbit": 0.30, "spread": 0.85,
                 "tunnel": 0.55, "sparks": 0.35, "notes": 0.95, "lift": 0.80,
                 "trail": 0.32},
    "surge":    {"tint": (46, 30, 18), "effect": "burst",
                 "glow": 1.30, "gamma": 2.00, "orbit": 1.85, "spread": 1.25,
                 "tunnel": 1.55, "sparks": 1.80, "notes": 1.40, "lift": 1.50,
                 "trail": 0.10},
    "rupture":  {"tint": (48, 17, 17), "effect": "shock",
                 "glow": 0.70, "gamma": 2.90, "orbit": 2.30, "spread": 0.90,
                 "tunnel": 1.45, "sparks": 1.65, "notes": 1.20, "lift": 1.60,
                 "trail": 0.00},
    "dissolve": {"tint": (24, 19, 42), "effect": "scatter",
                 "glow": 1.55, "gamma": 1.30, "orbit": 0.75, "spread": 1.32,
                 "tunnel": 0.70, "sparks": 1.00, "notes": 0.85, "lift": 0.60,
                 "trail": 0.50},
}
XFADE = 2.6          # seconds, centred on the boundary
PARAM_KEYS = ("glow", "gamma", "orbit", "spread", "tunnel", "sparks",
              "notes", "lift", "trail")


def blend_params(a, b, f):
    """Cross-dissolve two attribute sets."""
    out = {k: a[k] + (b[k] - a[k]) * f for k in PARAM_KEYS}
    out["tint"] = mix(a["tint"], b["tint"], f)
    return out

DEFAULT_STYLE = {
    "intro": "emerge", "verse-1": "drive", "chorus-1": "bloom",
    "verse-2": "drive", "chorus-2": "bloom", "verse-3": "hold",
    "recap": "surge", "turn": "rupture", "unravel": "dissolve",
    "final-chorus": "surge", "end": "hold",
}


def short(name):
    if "(" in name and ")" in name:
        name = name[name.index("(") + 1:name.index(")")]
    for junk in ("[bleed-cleaned]", "[restored]", "[restored no-dereverb]"):
        name = name.replace(junk, "")
    return name.strip() or "track"


def mix(c0, c1, f):
    f = max(0.0, min(1.0, f))
    return tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))


def A(color, alpha):
    """RGBA fill. Drawn through ImageDraw.Draw(img, "RGBA") this BLENDS with
    whatever is already there, instead of painting the background colour over
    it — which is what was muddying every overlap and burying the kit."""
    return (color[0], color[1], color[2], max(0, min(255, int(alpha * 255))))


def lighten(color, f):
    """Push toward white — bright timbres should read brighter."""
    return mix(color, (255, 252, 244), max(0.0, min(0.85, f)))


class Performer:
    def __init__(self, name, kind, color):
        self.name, self.kind, self.color = name, kind, color
        self.smooth = 0.0
        self.bright = 0.0
        self.onset = self.last_change = -1e9
        self.on_stage = False
        self.since = -1e9
        self.alpha = 0.0
        self.x = self.y = 0.0
        self.slot = -1
        self.ripples = []
        self.halo = 0.0
        self.norm = 700.0
        self.bnorm = []
        self.src = None
        self.layer = "stage"     # stage | background | highway
        self.drift = 0.0
        self.kick = self.snare = 0.0
        self.low_slow = self.hi_slow = 0.0

    def focus(self, t):
        novelty = math.exp(-(t - self.onset) / 3.5) \
            + 0.8 * math.exp(-(t - self.last_change) / 1.6)
        return self.smooth * (0.30 + 0.70 * min(1.5, novelty))


# ------------------------------------------------------------------ inputs ---

def load_notes(root, curve, zero_sec):
    names = {t.get("id"): (t.get("name") or "") for t in root.iter("Track")}
    out = collections.defaultdict(list)
    for lanes in root.iter("Lanes"):
        tid = lanes.get("track")
        if not tid:
            continue
        for clip in lanes.iter("Clip"):
            if clip.get("contentTimeUnit") == "seconds":
                continue
            base = float(clip.get("time", 0) or 0)
            pstart = float(clip.get("playStart", 0) or 0)
            for n in clip.iter("Note"):
                b = base + float(n.get("time", 0)) - pstart
                dur = float(n.get("duration", 0.25) or 0.25)
                out[names.get(tid, tid)].append((
                    curve.sec(b) - zero_sec, curve.sec(b + dur) - zero_sec,
                    int(n.get("key", 60)), float(n.get("vel", 0.8) or 0.8)))
    return {k: sorted(v) for k, v in out.items() if v}


def load_lanes(root, curve, zero_sec):
    """-> [{track, label, unit, pts:[(sec,val)]}] for every automation lane."""
    names = {t.get("id"): (t.get("name") or "") for t in root.iter("Track")}
    parent = {c: p for p in root.iter() for c in p}
    labels = {e.get("id"): (e.get("name") or e.tag) for e in root.iter() if e.get("id")}
    lanes = []
    for pts in root.iter("Points"):
        tgt = pts.find("Target")
        if tgt is None:
            continue
        vals = []
        for e in pts:
            if not e.tag.endswith("Point") or e.get("value") is None:
                continue
            try:
                vals.append((curve.sec(float(e.get("time"))) - zero_sec,
                             float(e.get("value"))))
            except (TypeError, ValueError):
                continue
        if len(vals) < 2:
            continue
        node, tid = pts, None
        while node in parent:
            node = parent[node]
            if node.tag == "Lanes" and node.get("track"):
                tid = node.get("track")
                break
        lanes.append({
            "track": names.get(tid, ""),
            "label": labels.get(tgt.get("parameter") or "", tgt.get("expression") or "auto"),
            "unit": pts.get("unit", "linear"),
            "pts": sorted(vals),
            "times": sorted(v[0] for v in vals),
        })
    return lanes


def word_onsets(lines, vox, rate, delta):
    """Tie each word to a real vocal onset.

    The line already has an exact start from the Bitwig marker. Inside that
    line we look at the LEAD VOCAL stem's own peak envelope, find the attack
    transients, and hand them out to the words in order — so "We be, be we be"
    lights up on the syllables rather than on a stopwatch. If a line has fewer
    clean onsets than words (slurred, held, or buried), that line falls back to
    even spacing across its span.
    """
    pk = vox["peak"]
    out = {}
    minsep = max(1, int(0.085 * rate))
    for ln in lines:
        words = ln["text"].split()
        if not words:
            continue
        t0 = ln["sec"]
        t1 = min(ln["end_sec"], t0 + 6.0)
        i0, i1 = int((t0 + delta) * rate), int((t1 + delta) * rate)
        seg = pk[max(0, i0):max(0, i1)]
        cands = []
        for k in range(2, len(seg) - 1):
            rise = seg[k] - seg[k - 2]
            if rise > 40 and seg[k] > 60 and seg[k] >= seg[k + 1] * 0.88:
                cands.append((rise, k))
        cands.sort(key=lambda c: -c[0])
        chosen = []
        for _, k in cands:
            if all(abs(k - c) >= minsep for c in chosen):
                chosen.append(k)
            if len(chosen) >= len(words):
                break
        chosen.sort()
        if len(chosen) >= len(words):
            out[ln["id"]] = [(w, t0 + k / rate)
                             for w, k in zip(words, chosen[:len(words)])]
        else:
            span = max(0.35, (t1 - t0) * 0.72)
            out[ln["id"]] = [(w, t0 + span * i / max(1, len(words)))
                             for i, w in enumerate(words)]
    return out


def lane_value(lane, t):
    pts = lane["pts"]
    i = bisect.bisect_right(lane["times"], t) - 1
    if i < 0:
        return pts[0][1]
    if i >= len(pts) - 1:
        return pts[-1][1]
    (t0, v0), (t1, v1) = pts[i], pts[i + 1]
    f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
    return v0 + (v1 - v0) * f


# ----------------------------------------------------------------- drawing ---

def profile(bands, gamma=2.1):
    """Normalise the spectrum to its own peak, then exaggerate.

    Absolute band levels make every rose a similar round lump. What separates
    a synth bass from a lead vocal is the SHAPE — where the energy is, not how
    much. So divide by the loudest band and raise to a power: strong bands stay
    near 1, weak ones collapse toward 0, and the silhouette gets deep notches
    and real lobes."""
    m = max(bands) or 1e-6
    return [max(0.03, (b / m) ** gamma) for b in bands]


def rose(d, cx, cy, r0, r1, bands, color, alpha, n=88, base=None):
    """Polar spectrum: bass at the bottom, air at the top, symmetric."""
    nb = len(bands)
    if nb < 2:
        d.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], fill=A(color, alpha))
        return
    pts = []
    for k in range(n):
        ang = 2 * math.pi * k / n
        f = abs(((ang / math.pi) % 2.0) - 1.0)         # 0 at bottom, 1 at top
        x = f * (nb - 1)
        i = min(nb - 2, int(x))
        g = x - i
        g = g * g * (3 - 2 * g)
        v = bands[i] * (1 - g) + bands[i + 1] * g
        rr = r0 + (r1 - r0) * v
        pts.append((cx + rr * math.sin(ang), cy - rr * math.cos(ang)))
    d.polygon(pts, fill=A(color, alpha))


def roll(d, cx, cy, w, h, notes, t, span, alpha, s, base=BG):
    x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=mix(base, (18, 20, 25), alpha * 0.8))
    win = [n for n in notes if n[1] > t - span / 2 and n[0] < t + span / 2]
    if win:
        lo, hi = min(n[2] for n in win), max(n[2] for n in win)
        rng = max(6, hi - lo)
        for on, off, pitch, vel in win:
            nx0 = x0 + w * ((on - (t - span / 2)) / span)
            nx1 = x0 + w * ((off - (t - span / 2)) / span)
            ny = y0 + h - h * ((pitch - lo + 1) / (rng + 2))
            live = on <= t < off
            col = PITCH_COLORS[pitch % 12]
            al = alpha * (1.0 if live else 0.35) * (0.55 + 0.45 * vel)
            th = (4.5 if live else 3.0) * s
            d.rectangle([max(x0, nx0), ny - th, min(x0 + w, nx1), ny + th],
                        fill=mix(base, lighten(col, 0.3 if live else 0.0), al))
    px = x0 + w / 2
    d.rectangle([px - s, y0, px + s, y0 + h], fill=mix(base, INK, alpha * 0.65))


def split_kit(bands):
    """-> (low, high) raw band sums. Kick lives low, snare and hats live high."""
    return (min(1.0, bands[0] * 1.05 + bands[1] * 0.55),
            min(1.0, bands[4] * 1.00 + bands[5] * 0.75 + bands[3] * 0.30))


def kit_transients(kit, low, high, dt):
    """Hits, not levels.

    Following the level fails: cymbals and hats sustain, so a level-follower
    sits pinned high and the whole frame stays washed in process blue. Instead
    track a slow average per band group and take only the RISE above it — that
    is a transient detector, and it fires on strikes.
    """
    kit.low_slow += (low - kit.low_slow) * (1 - math.exp(-dt / 0.28))
    kit.hi_slow += (high - kit.hi_slow) * (1 - math.exp(-dt / 0.32))
    kick_hit = max(0.0, low - kit.low_slow) * 2.6
    snare_hit = max(0.0, high - kit.hi_slow) * 3.2
    kit.kick = max(min(1.0, kick_hit), kit.kick - dt / 0.26)
    kit.snare = max(min(1.0, snare_hit), kit.snare - dt / 0.17)
    return max(0.0, kit.kick), max(0.0, kit.snare)


def transient_series(vals, rate, slow_tau, gain, thresh, min_sep, norm):
    """Scan a band series once and return every strike as (time, strength).

    Same trick as the live detector — slow average, take the rise above it —
    but run over the whole song up front, so hits can be scheduled AHEAD of
    time. That is what lets a tunnel ring launch early and arrive exactly on
    the beat instead of appearing after it."""
    out, slow, last = [], 0.0, -1e9
    dt = 1.0 / rate
    a = 1 - math.exp(-dt / slow_tau)
    for i, v in enumerate(vals):
        x = v / norm
        slow += (x - slow) * a
        rise = max(0.0, x - slow) * gain
        tt = i * dt
        if rise > thresh and tt - last >= min_sep:
            out.append((tt, min(1.0, rise)))
            last = tt
    return out


def kit_hits(src, band_names, rate):
    """-> {'kick': [...], 'snare': [...], 'hat': [...]} in MIX time."""
    b = src.get("bands", {})
    if not b:
        return {"kick": [], "snare": [], "hat": []}
    n = len(next(iter(b.values())))
    g = lambda k: b.get(k, [0] * n)
    mixes = {
        "kick":  [g("sub")[i] * 1.05 + g("low")[i] * 0.55 for i in range(n)],
        "snare": [g("himid")[i] + g("air")[i] * 0.75 + g("mid")[i] * 0.30 for i in range(n)],
        "hat":   [g("air")[i] + g("himid")[i] * 0.35 for i in range(n)],
    }
    cfg = {"kick": (0.30, 2.6, 0.18, 0.10), "snare": (0.32, 3.0, 0.20, 0.09),
           "hat": (0.22, 3.4, 0.16, 0.055)}
    out = {}
    delta = src["delta_sec"]
    for k, series in mixes.items():
        vv = sorted(x for x in series if x > 4)
        norm = max(60.0, vv[int(len(vv) * 0.96)] if vv else 600.0)
        tau, gain, thresh, sep = cfg[k]
        out[k] = [(tt - delta, mag)
                  for tt, mag in transient_series(series, rate, tau, gain,
                                                  thresh, sep, norm)]
    return out


def draw_tunnel(d, hits, t, W, H, s, lead, strength=1.0):
    """Rings launched from a point in depth, arriving exactly on the strike.

    Each hit is scheduled `lead` seconds early and travels toward the viewer,
    landing at radius R on its beat, then blowing past the frame. Kick rings
    are indigo and heavy; snare rings go process blue and thin."""
    cx, cy = W * 0.5, H * 0.47
    R = max(W, H) * 0.34
    for kind, colour, weight in (("kick", INDIGO_LIFT, 1.0),
                                 ("snare", PROCESS_BLUE, 0.62)):
        arr = hits[kind]
        i = bisect.bisect_left([h[0] for h in arr], t - 0.42)
        while i < len(arr) and arr[i][0] < t + lead:
            th, mag = arr[i]
            i += 1
            age = t - th                      # <0 approaching, >0 past
            if age < -lead or age > 0.42:
                continue
            if age <= 0:
                q = -age / lead               # 1 far, 0 arriving
                r = R * (1.0 - q) ** 2.4 + R * 0.03
                al = (1.0 - q) ** 2.1 * mag * 0.55 * strength
                wdt = max(1, int((2 + 11 * (1 - q)) * s * weight))
            else:
                e = age / 0.42
                r = R * (1.0 + 2.6 * e * e)
                al = (1.0 - e) ** 1.6 * mag * 0.45 * strength
                wdt = max(1, int((13 - 9 * e) * s * weight))
            if al < 0.015:
                continue
            rx, ry = r, r * 0.74
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                      outline=A(colour, al), width=wdt)


class Sparks:
    """Hi-hats as glints in the corner of your eye.

    They never appear centre-frame: each hat strike seeds particles out at the
    periphery and they shoot outward and off. Count and brightness come from
    the strike, so a busy 16th pattern shimmers and an open hat throws."""

    def __init__(self, seed=11):
        self.rnd = random.Random(seed)
        self.live = []
        self.i = 0

    def feed(self, hits, t, dt, W, H, density=1.0):
        arr_t = [h[0] for h in hits]
        j = bisect.bisect_left(arr_t, t)
        while j < len(hits) and hits[j][0] < t + dt:
            _, mag = hits[j]
            j += 1
            n = int(3 + 14 * mag)
            for _ in range(n):
                if len(self.live) > 320:
                    break
                # bias toward the sides, never the middle
                ang = self.rnd.uniform(0, 2 * math.pi)
                side = abs(math.cos(ang))
                if side < 0.45 and self.rnd.random() < 0.75:
                    continue
                r = min(W, H) * self.rnd.uniform(0.34, 0.62)
                sp = min(W, H) * self.rnd.uniform(0.85, 2.1) * (0.5 + mag)
                self.live.append([ang, r, sp, 0.0,
                                  self.rnd.uniform(0.28, 0.62), mag])

    def step(self, dt):
        for p in self.live:
            p[1] += p[2] * dt
            p[3] += dt
        self.live = [p for p in self.live if p[3] < p[4]]

    def draw(self, d, W, H, s):
        cx, cy = W * 0.5, H * 0.47
        for ang, r, _sp, age, life, mag in self.live:
            e = 1.0 - age / life
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang) * 0.80
            if x < -40 or x > W + 40 or y < -40 or y > H + 40:
                continue
            rad = (2.2 + 6.0 * mag) * s * (0.35 + 0.65 * e)
            al = e * e * (0.55 + 0.65 * mag)
            for k, ga in ((3.4, 0.16), (2.0, 0.30), (1.0, 1.0)):
                d.ellipse([x - rad * k, y - rad * k, x + rad * k, y + rad * k],
                          fill=A((214, 236, 255), al * ga))


def field_colour(section_tint, kick, snare):
    """The room's colour. Indigo at rest, lifted by the kick, thrown all the way
    to process blue by the snare."""
    base = mix(INDIGO, section_tint, 0.34)
    base = mix(base, INDIGO_LIFT, min(0.75, kick * 0.70))
    return mix(base, PROCESS_BLUE, min(0.55, (snare ** 1.4) * 0.62))


def draw_kick_swell(d, kick, snare, W, H, s):
    """Low weight from below — the meat the colour change alone can't carry."""
    if kick > 0.03:
        for j in range(7, 0, -1):
            rx = W * (0.30 + 0.13 * j) * (0.65 + 0.55 * kick)
            ry = H * (0.16 + 0.085 * j) * (0.65 + 0.55 * kick)
            d.ellipse([W / 2 - rx, H * 1.02 - ry, W / 2 + rx, H * 1.02 + ry],
                      fill=A(INDIGO_LIFT, 0.055 * kick * (1.0 - j / 9.0)))
    if snare > 0.05:
        h = H * (0.05 + 0.10 * snare)
        for j in range(5, 0, -1):
            d.rectangle([0, H * 0.46 - h * j * 0.5, W, H * 0.46 + h * j * 0.5],
                        fill=A(PROCESS_BLUE, 0.045 * snare * (1.0 - j / 7.0)))


def arrival_path(lat, dt, W, H):
    """Where a note sits, given how many seconds until its moment.

    Not a lane. Notes gather high and shallow when they are far off, fan out
    and come forward as their moment approaches, then keep going past the
    viewer and dissolve. Each one bows slightly to its own side so the paths
    read as drifting rather than as a track.
    """
    q = max(-0.40, min(1.0, dt / LOOK_AHEAD))
    depth = q / (q + 0.78) if q >= 0 else q * 1.25
    near_x, near_y = (0.5 + 0.410 * lat) * W, 0.690 * H
    far_x, far_y = (0.5 + 0.070 * lat) * W, 0.275 * H
    bow = 0.055 * W * lat * math.sin(math.pi * max(0.0, min(1.0, q)))
    return (near_x + (far_x - near_x) * depth + bow,
            near_y + (far_y - near_y) * depth,
            max(0.10, 1.0 - 0.78 * max(0.0, depth)) * (1.0 - 1.1 * min(0.0, depth)))


def capsule(d, cx, cy, w, h, color, alpha):
    r = max(1.0, min(w, h) * 0.48)
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                        radius=r, fill=A(color, alpha))


def draw_arrivals(players, t, W, H, s, layer_d, size=1.0):
    """Notes introducing themselves out of the depth, blooming, dissolving."""
    drawn = []
    for p in players:
        if p.alpha < 0.01:
            continue
        lo, hi = p.pitch_lo, p.pitch_hi
        rng = max(4, hi - lo)
        i = bisect.bisect_left(p.note_on, t - 1.1)
        while i < len(p.src) and p.src[i][0] < t + LOOK_AHEAD:
            on, off, pitch, vel = p.src[i]
            i += 1
            age = t - on
            if age > 0.95:
                continue
            lat = 2.0 * ((pitch - lo) / rng) - 1.0
            x, y, sc = arrival_path(lat, on - t, W, H)
            # fade in far away, hold through the moment, dissolve after
            fin = min(1.0, (LOOK_AHEAD - (on - t)) / (0.30 * LOOK_AHEAD))
            fout = 1.0 if age <= 0.0 else max(0.0, 1.0 - age / 0.95)
            al = p.alpha * max(0.0, min(1.0, fin)) * fout * (0.55 + 0.45 * vel)
            if al < 0.02:
                continue
            bloom = 1.0 + 0.55 * math.exp(-max(0.0, age) / 0.11)
            dur = max(0.06, min(1.6, off - on))
            w = 46 * s * sc * (0.7 + 0.3 * vel) * bloom * size
            h = w * (0.62 + 1.15 * dur)
            drawn.append((sc, x, y, w, h, PITCH_COLORS[pitch % 12], al, age))
    # far first, so near notes sit in front
    drawn.sort(key=lambda c: c[0])
    for sc, x, y, w, h, col, al, age in drawn:
        for j in range(5, 0, -1):
            k = 1.0 + 0.34 * j
            capsule(layer_d, x, y, w * k, h * (1 + (k - 1) * 0.42),
                    col, al * 0.085 * (1.0 - j / 7.0))
        capsule(layer_d, x, y, w, h, lighten(col, 0.18), al)
        if 0.0 <= age < 0.55:                 # soft swell at its moment
            e = 1.0 - age / 0.55
            rw = w * (1.5 + 2.6 * (1 - e))
            rh = h * (1.3 + 1.7 * (1 - e))
            layer_d.rounded_rectangle([x - rw / 2, y - rh / 2, x + rw / 2, y + rh / 2],
                                      radius=min(rw, rh) * 0.48,
                                      outline=A(lighten(col, 0.45), al * e * 0.55),
                                      width=max(1, int(2.5 * s)))


def draw_lyrics(d, line, words, t, W, H, s, vox_amp, lift=1.0):
    """The line rides the lead vocal.

    Each character samples the vocal envelope a few milliseconds behind the one
    before it, so amplitude travels through the word as a wave: letters lift,
    swell and settle. Loud syllables physically push their letters up and make
    them bigger. Nothing here is a stopwatch — it is the singer's own envelope
    deforming the type.
    """
    if not line:
        return
    base = int(58 * s)
    fnt = font("bold", base)
    yc = H - int(96 * s)
    parts = words or [(w, line["sec"]) for w in line["text"].split()]

    space = d.textlength(" ", font=fnt)
    metrics, total = [], 0.0
    for w, wt in parts:
        chars = [(ch, d.textlength(ch, font=fnt)) for ch in w]
        wide = sum(c[1] for c in chars)
        metrics.append((w, wt, chars, wide))
        total += wide + space
    total -= space

    x = (W - total) / 2
    for wi, (w, wt, chars, wide) in enumerate(metrics):
        lit = t >= wt
        nxt = metrics[wi + 1][1] if wi + 1 < len(metrics) else line["end_sec"]
        active = lit and t < nxt + 0.30
        heat = max(0.0, 1.0 - (t - wt) / 0.28) if lit else 0.0
        for ci, (ch, cw) in enumerate(chars):
            if active:
                amp = vox_amp(t - ci * 0.016)
            elif lit:
                amp = 0.10
            else:
                amp = 0.0
            size = max(8, int(base * (1.0 + 0.34 * amp * lift)))
            f2 = font("bold", size)
            dy = int((-46 * amp * lift + 6 * math.sin(ci * 0.9 + t * 1.7) * amp) * s)
            if lit:
                col = A(mix(INK, (255, 226, 150), heat), 1.0)
            else:
                col = A(INK, 0.22)
            d.text((x + cw / 2, yc + dy), ch, font=f2, fill=col, anchor="mm")
            x += cw
        x += space


def section_effect(d, kind, prog, W, H, s, rnd):
    """prog 0..1 through the entrance. Returns a (dx,dy) shake."""
    e = 1.0 - prog
    if kind == "iris":
        r = (0.10 + 1.35 * prog) * max(W, H)
        for k in range(6):
            rr = r + k * 14 * s
            d.ellipse([W / 2 - rr, H / 2 - rr, W / 2 + rr, H / 2 + rr],
                      outline=A((70, 120, 155), e * 0.55), width=int(14 * s))
    elif kind == "sweep":
        x = -0.3 * W + 1.6 * W * prog
        for k in range(5):
            xx = x - k * 44 * s
            d.rectangle([xx, 0, xx + 12 * s, H],
                        fill=A((170, 140, 105), e * 0.40 / (k + 1)))
    elif kind == "rings":
        for k in range(4):
            rr = max(W, H) * (prog * 0.95 + k * 0.14)
            d.ellipse([W / 2 - rr, H / 2 - rr, W / 2 + rr, H / 2 + rr],
                      outline=A((225, 130, 165), e * 0.42), width=int(7 * s))
    elif kind == "burst":
        for k in range(28):
            ang = 2 * math.pi * k / 28
            r0 = max(W, H) * 0.12 * prog
            r1 = r0 + max(W, H) * 0.55 * prog
            d.line([W / 2 + r0 * math.cos(ang), H / 2 + r0 * math.sin(ang),
                    W / 2 + r1 * math.cos(ang), H / 2 + r1 * math.sin(ang)],
                   fill=A((240, 180, 105), e * 0.45), width=max(1, int(3 * s)))
    elif kind == "shock":
        if prog < 0.16:
            d.rectangle([0, 0, W, H], fill=A((235, 215, 195), min(0.85, (0.16 - prog) * 4.2)))
        k = e * e * 26 * s
        return (rnd.uniform(-k, k), rnd.uniform(-k, k))
    elif kind == "scatter":
        for _ in range(90):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            d.rectangle([x, y, x + 3 * s, y + 3 * s],
                        fill=A((165, 150, 225), e * 0.5))
    return (0.0, 0.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", type=pathlib.Path, default=ROOT / "out" / "stage.mp4")
    ap.add_argument("--audio", type=pathlib.Path, default=ROOT / "audio" / "song.wav")
    ap.add_argument("--section")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--max-on-stage", type=int, default=5)
    ap.add_argument("--blur", type=int, default=4,
                    help="sub-frames averaged per output frame (motion blur)")
    ap.add_argument("--ss", type=float, default=1.0,
                    help="spatial supersample before downscaling")
    ap.add_argument("--draft", action="store_true",
                    help="1280 wide, no blur — for fast iteration")
    a = ap.parse_args()
    if a.draft:
        a.width, a.blur, a.ss = 1280, 1, 1.0

    report_fonts()
    bm = load(ROOT / "analysis" / "beatmap.json")
    env = load(ROOT / "analysis" / "envelopes.json")
    sections = load(ROOT / "shots" / "sections.json")["sections"]
    band_names = env.get("bands", [])
    band_hz = env.get("band_hz", [])

    style_path = ROOT / "shots" / "stage_style.json"
    if style_path.exists():
        style = load(style_path)
    else:
        style = {x["id"]: DEFAULT_STYLE.get(x["id"], "drive") for x in sections}
        save(style_path, style)

    proj = next(iter(sorted((ROOT / "source").glob("*.dawproject"))), None) \
        or (ROOT / "source" / "project.xml")
    root = read_project_xml(proj)
    curve = TempoCurve([(p["beat"], p["bpm"], p.get("interpolation", "linear"))
                        for p in bm["tempo_map"]])
    zero_sec = curve.sec(bm["zero_beat"])
    notes = load_notes(root, curve, zero_sec)
    lanes = load_lanes(root, curve, zero_sec)
    try:
        lyric_lines = load(ROOT / "analysis" / "lyrics.json")["lines"]
    except FileNotFoundError:
        lyric_lines = []

    feedback = next((l for l in lanes if "Feedback" in l["label"]), None)
    decay_lane = next((l for l in lanes if "Decay" in l["label"]), None)
    sends = [l for l in lanes if l["label"] == "Send" and l["track"]]
    events = []
    for l in lanes:
        for (_, v0), (tb, v1) in zip(l["pts"], l["pts"][1:]):
            if abs(v1 - v0) > 0.05:
                events.append((tb, l["track"], abs(v1 - v0)))
    events.sort()
    ev_t = [e[0] for e in events]

    t0, t1 = 0.0, bm["duration_sec"]
    if a.section:
        s_ = next((x for x in sections if x["id"] == a.section), None)
        if not s_:
            raise SystemExit("sections: " + ", ".join(x["id"] for x in sections))
        t0, t1 = s_["start_sec"], s_["end_sec"]

    perf, ci = {}, 0
    for name in env["tracks"]:
        p = Performer(short(name), "audio", PALETTE[ci % len(PALETTE)])
        p.src = env["tracks"][name]
        vals = sorted(v for v in p.src["rms"] if v > 5)
        p.norm = max(60.0, vals[int(len(vals) * 0.95)] if vals else 700.0)
        for bn in band_names:
            bv = sorted(v for v in p.src.get("bands", {}).get(bn, []) if v > 3)
            p.bnorm.append(max(25.0, bv[int(len(bv) * 0.97)] if bv else 300.0))
        if any(m in p.name.lower() for m in BACKGROUND_MATCH):
            p.layer = "background"
        perf[name] = p
        ci += 1
    for name in notes:
        if len(notes[name]) < 5:
            continue
        p = Performer(short(name), "notes", PALETTE[ci % len(PALETTE)])
        p.src = notes[name]
        p.layer = "highway"
        perf[name] = p
        ci += 1

    rate = env["rate"]

    # highway performers need their pitch range and a sorted onset index
    for p in perf.values():
        if p.layer == "highway":
            p.pitch_lo = min(n[2] for n in p.src)
            p.pitch_hi = max(n[2] for n in p.src)
            p.note_on = [n[0] for n in p.src]

    vox = next((v for k, v in env["tracks"].items() if "lead vocal" in k.lower()), None)
    vox_norm = 700.0
    if vox:
        vv = sorted(x for x in vox["peak"] if x > 5)
        vox_norm = max(120.0, vv[int(len(vv) * 0.93)] if vv else 700.0)
    words = {}
    if lyric_lines and vox:
        words = word_onsets(lyric_lines, vox, rate, vox["delta_sec"])
        n_real = sum(1 for ln in lyric_lines
                     if len(words.get(ln["id"], [])) == len(ln["text"].split())
                     and len(ln["text"].split()) > 1)
        print(f"  words     {sum(len(v) for v in words.values())} placed from "
              f"lead-vocal onsets across {n_real} lines")
    lyric_times = [ln["sec"] for ln in lyric_lines]

    def vox_amp(tt):
        if not vox:
            return 0.0
        i = int((tt + vox["delta_sec"]) * rate)
        if not (0 <= i < len(vox["peak"])):
            return 0.0
        return min(1.0, vox["peak"][i] / max(120.0, vox_norm))

    def bands_at(p, t):
        i = int((t + p.src["delta_sec"]) * rate)
        out = []
        for k, bn in enumerate(band_names):
            arr = p.src.get("bands", {}).get(bn)
            v = arr[i] if arr and 0 <= i < len(arr) else 0
            out.append(min(1.0, v / p.bnorm[k]))
        return out

    def sample(p, t, key):
        i = int((t + p.src["delta_sec"]) * rate)
        if not (0 <= i < len(p.src[key])):
            return 0.0
        return min(1.25, p.src[key][i] / p.norm)

    def energy_at(p, t):
        if p.kind == "audio":
            return sample(p, t, "rms")
        live = [n for n in p.src if n[0] <= t < n[1] + 0.25]
        return 0.0 if not live else min(1.0, 0.28 * len(live) + 0.5 * max(n[3] for n in live))

    OUT_W = a.width
    OUT_H = int(OUT_W * 9 / 16) // 2 * 2
    W = int(OUT_W * a.ss) // 2 * 2
    H = int(OUT_H * a.ss) // 2 * 2
    s = W / 1920
    fps = a.fps
    dt = 1.0 / (fps * max(1, a.blur))      # simulation runs at the sub-frame rate
    g = Grid(bm["bars"])
    rnd = random.Random(7)

    # slot 0 holds the centre and drifts gently; the rest ride a slow ellipse
    SLOT_SCALE = [1.00, 0.62, 0.62, 0.52, 0.52, 0.44]
    SLOT_ANGLE = [0.0, -0.62, 0.62, -2.36, 2.36, math.pi]
    SLOT_RAD = [0.0, 1.00, 1.00, 0.92, 0.92, 0.80]

    def slot_pos(k, phase, spread, tt):
        if k == 0:
            return (0.50 * W + 0.018 * W * math.sin(tt * 0.21),
                    0.455 * H + 0.020 * H * math.sin(tt * 0.147 + 1.1))
        ang = SLOT_ANGLE[k] + phase
        return (0.50 * W + 0.335 * W * SLOT_RAD[k] * spread * math.sin(ang),
                0.455 * H - 0.300 * H * SLOT_RAD[k] * spread * math.cos(ang))
    stage = [None] * len(SLOT_SCALE)
    MIN_DWELL = 1.8
    # frame-rate independent easing, so 30fps and 60fps move at the same speed
    k_pos = 1 - math.exp(-dt / 0.13)
    k_alpha = 1 - math.exp(-dt / 0.20)
    k_up = 1 - math.exp(-dt / 0.035)
    k_dn = 1 - math.exp(-dt / 0.13)

    a.out = a.out.resolve()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = a.out.with_name(f".{a.out.stem}.partial{a.out.suffix}")
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{OUT_W}x{OUT_H}", "-r", str(fps), "-i", "-"]
    if a.audio.exists():
        cmd += ["-ss", f"{t0:.4f}", "-i", str(a.audio), "-c:a", "aac", "-b:a", "192k",
                "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    kit = next((q for q in perf.values() if q.layer == "background"), None)
    hits = kit_hits(kit.src, band_names, rate) if kit else \
        {"kick": [], "snare": [], "hat": []}
    if kit:
        print(f"  kit       {len(hits['kick'])} kicks, {len(hits['snare'])} snares, "
              f"{len(hits['hat'])} hats detected")
    sparks = Sparks()
    TUNNEL_LEAD = 1.25          # long enough that 4-6 rings are always in flight

    sec_starts = [x["start_sec"] for x in sections]
    arch_for = [ARCHETYPES.get(style.get(x["id"], "drive"), ARCHETYPES["drive"])
                for x in sections]

    def params_at(tt):
        """Attribute set now, cross-dissolved across the boundary."""
        i = max(0, bisect.bisect_right(sec_starts, tt) - 1)
        cur = arch_for[i]
        half = XFADE / 2.0
        if i > 0 and tt < sec_starts[i] + half:
            f = 0.5 + (tt - sec_starts[i]) / XFADE
            return blend_params(arch_for[i - 1], cur, max(0.0, min(1.0, f))), cur, i
        if i + 1 < len(sections) and tt > sec_starts[i + 1] - half:
            f = (tt - (sec_starts[i + 1] - half)) / XFADE
            return blend_params(cur, arch_for[i + 1], max(0.0, min(1.0, f))), cur, i
        return blend_params(cur, cur, 0.0), cur, i
    prev_img = None
    n_frames = int(round((t1 - t0) * fps))
    N = max(1, a.blur)
    orbit_phase = 0.0
    acc, held = None, 0
    downscale = (W, H) != (OUT_W, OUT_H)

    # The simulation runs at the SUB-frame rate and every N sub-frames are
    # averaged into one output frame. That is real accumulation motion blur:
    # fast things smear along their actual path instead of strobing.
    for f in range(n_frames * N):
        t = t0 + f * dt
        pos = g.at(t)
        P, arche, sec_i = params_at(t)
        sec = sections[sec_i]
        orbit_phase += 2 * math.pi * dt / ORBIT_PERIOD * P["orbit"]
        into = t - sec["start_sec"]

        for p in perf.values():
            e = energy_at(p, t)
            was = p.smooth
            p.smooth += (e - p.smooth) * (k_up if e > p.smooth else k_dn)
            if p.smooth > 0.10 and was <= 0.10:
                p.onset = t
            if abs(p.smooth - was) > 0.045 * (60 * dt):
                p.last_change = t
            if p.kind == "audio" and band_names:
                b = bands_at(p, t)
                tot = sum(b) or 1e-6
                cen = sum(v * hz for v, hz in zip(b, band_hz)) / tot
                target = min(1.0, math.log10(max(cen, 40) / 40) / 2.4)
                p.bright += (target - p.bright) * k_dn

        i = bisect.bisect_left(ev_t, t)
        while i < len(events) and events[i][0] < t + dt:
            p = perf.get(events[i][1])
            if p is not None:
                p.ripples.append((t, min(1.0, events[i][2] * 2.2)))
                p.last_change = t
            i += 1

        fb = max(0.0, min(1.0, lane_value(feedback, t))) if feedback else 0.0
        dc = max(0.0, min(1.0, lane_value(decay_lane, t))) if decay_lane else 0.3
        for l in sends:
            p = perf.get(l["track"])
            if p is not None:
                p.halo += (max(0.0, min(1.0, lane_value(l, t))) - p.halo) * k_dn

        players = [q for q in perf.values() if q.layer == "stage"]
        ranked = sorted(players, key=lambda q: -q.focus(t))
        rank = {p: k for k, p in enumerate(ranked)}
        n_slots = min(a.max_on_stage, len(SLOT_SCALE))
        for k, p in enumerate(stage):
            if p is None:
                continue
            if (p.smooth < 0.04 or rank[p] >= n_slots + 2) and t - p.since > MIN_DWELL:
                p.on_stage, stage[k] = False, None
        for p in ranked:
            if p.on_stage or p.smooth <= 0.07 or None not in stage[:n_slots]:
                continue
            k = stage.index(None)
            stage[k], p.on_stage, p.since, p.slot = p, True, t, k
            if p.x == 0 and p.y == 0:
                p.x, p.y = slot_pos(k, orbit_phase, P["spread"], t)
        lead = stage[0]
        top = next((p for p in ranked if p.on_stage), None)
        if top is not None and top is not lead and t - top.since > 1.0:
            if lead is None or top.focus(t) > 1.3 * max(lead.focus(t), 1e-6):
                k = stage.index(top)
                stage[0], stage[k] = top, lead
                top.slot, top.since = 0, t
                if lead is not None:
                    lead.slot, lead.since = k, t
        on_stage_now = [p for p in stage[:n_slots] if p is not None]
        for p in perf.values():
            want_on = p.on_stage or p.layer in ("background", "highway")
            if p.layer == "background":
                want_on = p.smooth > 0.03
            elif p.layer == "highway":
                # visible while notes are APPROACHING, not only while sounding —
                # otherwise the lane blinks out between phrases
                j = bisect.bisect_left(p.note_on, t - 1.2)
                want_on = j < len(p.note_on) and p.note_on[j] < t + LOOK_AHEAD
            p.alpha += ((1.0 if want_on else 0.0) - p.alpha) * k_alpha
            if p.on_stage and p.slot >= 0:
                sx, sy = slot_pos(min(p.slot, len(SLOT_SCALE) - 1),
                                  orbit_phase, P["spread"], t)
                p.x += (sx - p.x) * k_pos
                p.y += (sy - p.y) * k_pos

        # ---------------------------------------------------------------- draw
        kick = snare = 0.0
        if kit is not None:
            low, high = split_kit(bands_at(kit, t))
            kick, snare = kit_transients(kit, low, high, dt)
        bgc = field_colour(P["tint"], kick, snare)
        img = Image.new("RGB", (W, H), bgc)
        d = ImageDraw.Draw(img, "RGBA")

        shake = (0.0, 0.0)
        if into < 1.35:
            shake = section_effect(d, arche["effect"], into / 1.35, W, H, s, rnd)

        pulse = (1.0 - pos["phase"]) ** 2.5
        d.rectangle([0, 0, W, int(5 * s)],
                    fill=A((225, 190, 125), pulse * (1.0 if pos["beat"] == 1 else 0.4)))
        fy = H * 0.90
        d.ellipse([-W * 0.35, fy - H * 0.30, W * 1.35, fy + H * 0.42],
                  outline=A((255, 255, 255), 0.055), width=max(1, int(2 * s)))

        # --- back to front: the room, then the notes, then the players ------
        draw_kick_swell(d, kick, snare, W, H, s)
        draw_tunnel(d, hits, t, W, H, s, TUNNEL_LEAD, P["tunnel"])
        sparks.feed(hits["hat"], t, dt, W, H, P["sparks"])
        sparks.step(dt)
        sparks.draw(d, W, H, s)

        draw_arrivals([q for q in perf.values() if q.layer == "highway"],
                      t, W, H, s, d, P["notes"])

        for p in sorted((q for q in perf.values() if q.layer == "stage"),
                        key=lambda q: -(q.slot if q.slot >= 0 else 9)):
            if p.alpha < 0.01:
                continue
            scale = SLOT_SCALE[min(max(p.slot, 0), len(SLOT_SCALE) - 1)]
            px, py = p.x + shake[0], p.y + shake[1]
            r0 = 15 * s * scale
            r1 = r0 + 285 * s * scale * max(p.smooth, 0.02)
            col = lighten(p.color, 0.45 * p.bright)

            life = 1.0 + 1.8 * dc
            p.ripples = [(rt, rm) for rt, rm in p.ripples if t - rt < life]
            for rt, rm in p.ripples:
                age = (t - rt) / life
                rr = r1 + 300 * s * scale * age
                d.ellipse([px - rr, py - rr, px + rr, py + rr],
                          outline=A(col, p.alpha * rm * (1 - age) * 0.85),
                          width=max(1, int(5 * s * (1 - age))))
            if p.halo > 0.02:
                hr = r1 * (1.35 + 0.9 * p.halo)
                d.ellipse([px - hr, py - hr, px + hr, py + hr],
                          outline=A(col, p.alpha * p.halo * 0.5),
                          width=max(1, int(3 * s)))

            b = profile(bands_at(p, t), P["gamma"])
            for j in range(9, 0, -1):
                k = 1.0 + 0.20 * j
                rose(d, px, py, r0 * k, r1 * k, b, p.color,
                     p.alpha * 0.042 * P["glow"] * (1.0 - j / 11.0))
            rose(d, px, py, r0, r1, b, col, p.alpha)

            # low performers put their name above the shape, or it lands in
            # the lyric line
            if py > 0.63 * H:
                d.text((px, py - r1 - 10 * s * scale), p.name,
                       font=font("bold", max(11, int(28 * s * scale))),
                       fill=A(INK, p.alpha * 0.9), anchor="md")
            else:
                d.text((px, py + r1 + 22 * s * scale), p.name,
                       font=font("bold", max(11, int(28 * s * scale))),
                       fill=A(INK, p.alpha * 0.9), anchor="ma")

        li = bisect.bisect_right(lyric_times, t) - 1
        cur_line = None
        if 0 <= li < len(lyric_lines) and t < lyric_lines[li]["end_sec"]:
            cur_line = lyric_lines[li]
        if cur_line:
            draw_lyrics(d, cur_line, words.get(cur_line["id"]), t, W, H, s,
                        vox_amp, P["lift"])

        d.text((int(50 * s), int(38 * s)),
               f"{sec['id'].replace('-', ' ').upper()}   ·   {style.get(sec['id'], '')}",
               font=font("bold", int(32 * s)), fill=A(INK, 0.50))
        d.text((W - int(50 * s), int(38 * s)),
               f"{tc(t, fps)}   {pos['bar']}.{pos['beat']}",
               font=font("mono", int(30 * s)), fill=A(DIM, 0.9), anchor="ra")

        # reverb feedback -> visual feedback
        trail = min(0.72, 0.62 * fb + P["trail"])
        if prev_img is not None and trail > 0.02:
            img = Image.blend(img, prev_img, trail)
        prev_img = img

        acc = img if acc is None else Image.blend(acc, img, 1.0 / (held + 1))
        held += 1
        if held >= N:
            out = acc.resize((OUT_W, OUT_H), Image.LANCZOS) if downscale else acc
            proc.stdin.write(out.tobytes())
            acc, held = None, 0
        if f % (fps * N * 15) == 0:
            print(f"\r  {t - t0:6.1f}s / {t1 - t0:.1f}s", end="", flush=True)

    proc.stdin.close()
    err = proc.stderr.read().decode()[-1500:]
    if proc.wait() != 0:
        print("\n" + err)
        raise SystemExit("ffmpeg failed")
    tmp.replace(a.out)
    print(f"\rwrote {a.out}   {t1 - t0:.2f}s   {OUT_W}x{OUT_H} @ {fps}fps   "
          f"blur x{N}" + (f"  ss {a.ss:g}" if downscale else "")
          + f"   {len(perf)} performers")


if __name__ == "__main__":
    main()
