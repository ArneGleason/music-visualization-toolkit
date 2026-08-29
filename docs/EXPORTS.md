# What to export from Bitwig

## The one that matters: DAWproject

**File → Export DAWproject** → `source/<Song>.dawproject`

This is the timing ground truth, and it is not interchangeable with a MIDI
export. A Standard MIDI File's `set_tempo` is a **step function** — the MIDI
spec has no linear tempo ramp. A project with real tempo automation either
gets subdivided into many small steps on export, or silently flattened.

Measured on this project (944 tempo points, 119–133 bpm, 118 bars):

| timing source | total length | error by the outro |
|---|---|---|
| exact ramp integration (DAWproject) | 224.975s | — |
| step approximation (what MIDI gives you) | 225.196s | 221 ms |
| fixed 124.948 bpm | 226.654s | **1.7 s** |

`tools/dawproject.py` integrates the ramps in closed form:

    t = 60 · Δbeats · ln(T₁/T₀) / (T₁ − T₀)

No stepping, no accumulated error. It also reads your **cue markers**, which
in this project already are the timed lyric sheet — 74 lines pinned to exact
bar/beat positions, plus structural markers. That replaces hand-marking
lyrics entirely.

## The mix comes from the project too

Keep the bounced master on a muted track in the project — here it's a track
named **Project Master**. `dawproject.py` finds it, extracts nothing, but reads
two things off it that matter enormously:

**Where it starts.** This bounce sits at **beat 14**, not bar 1 — its sample 0
is 6.7243s into project time. A master bounce almost never starts at bar 1; it
starts where the music starts. The importer zeroes the entire grid there, so
beatmap time 0 = WAV sample 0 = video frame 0. Without that, every single cut
in the video would be 6.7 seconds out — and it would look like a tempo problem,
which is the worst kind of bug to chase.

**How long it is.** 215.393s, which cross-checks against the WAV's own header.
If `audio/song.wav` doesn't match the bounce length, the importer says so.

Pull the WAV out of the project rather than re-exporting, so the file and the
timing provably come from the same place:

    unzip -o -j source/*.dawproject "audio/<bounce>.wav" -d /tmp && cp /tmp/<bounce>.wav audio/song.wav

Override the detection with `--master-track <substring>` or `--zero-at <beat>`
if the track is named something else, or `--no-zero` to stay in project time.

**`refs/cover.png`** — the album cover at the highest resolution you have.

## Optional, later

**`audio/vocal.wav`** — the isolated lead vocal. Only if you eventually want
word-level timing for per-word visual hits (see `ALIGNMENT.md`). The
DAWproject already embeds a `(Lead Vocal) [restored]` stem, so this is a
`unzip -j` away if you ever need it.

## Sanity check

```bash
./run.sh timing
```

Auto-detects the `.dawproject` in `source/`, rebuilds the grid, re-reads the
lyrics, and renders `build/clickcheck.wav` — a click generated from the parsed
tempo curve, mixed under your track.

**Then listen.** Start, middle, and the last chorus. There is one assumption
in that integration: that Bitwig ramps tempo linearly against *beats* rather
than against *time*. The file says `timeUnit="beats"`, which is why the
formula is written the way it is — but a spec is not an ear. If the click
locks to your drums all the way to 3:41, the grid is exact and every cut
downstream is frame-accurate. If it drifts late, tell me and I'll flip the
assumption.
