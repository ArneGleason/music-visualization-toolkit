# Timeline register

The timeline register is the project-level collaboration surface between the
DAW, a human editor, AI direction, and renderers. Editable data stays separate
from rendering code.

## Data flow

```text
DAWproject + final mix
        │
        ▼
generated/beatmap.json          exact ramped tempo; bar/beat ↔ seconds
        │
        ├──── generated/waveforms.json
        │                       silent peak/RMS editing references
        ├──── timeline.json     human/AI-authored musical positions
        │
        ▼
generated/timeline.compiled.json
                                integer-frame renderer register
```

`timeline.json` is version-controlled. Files under `generated/` and
`project.local.json` are not. The latter holds machine-specific absolute paths
to the DAWproject, mix, and stems.

## Musical positions and frame edges

Positions use `bar.beat` or `bar.beat.tick`, where a tick is measured using the
beatmap PPQ (normally 960). For example, `12.3.480` is halfway through beat 3
of bar 12.

The compiler resolves each position through the DAWproject tempo curve, rounds
the result to a frame, and derives display seconds back from that frame. This
keeps renderer edges deterministic; displayed seconds are never an independent
editing authority.

## Commands

```bash
python tools/timeline.py sync projects/rivers-of-mars/project.json
python tools/timeline.py validate projects/rivers-of-mars/project.json
python tools/timeline.py query projects/rivers-of-mars/project.json --bar 18.1
python tools/timeline_server.py --project projects/rivers-of-mars/project.json
```

`sync` rebuilds the project beatmap from the DAWproject, validates the editable
register, and compiles the renderer register. `query` returns active lyrics,
scenes, transitions, choreography, and driver references at a frame, second,
or musical position.

The editor opens at `http://127.0.0.1:8760/timeline/`. It supports audio
scrubbing, a bar-primary ruler, parallel tracks, overlapping clips,
dragging/resizing with musical snapping, unplaced lyric intake, natural-language
direction, performance-only improv lyrics, driver references, AI suggestion
status, and atomic save/compile. Improv cues retain `lyricOrigin: "improv"` so
renderers can distinguish performed additions from the source lyric sheet.

Configured master/stem sources are reduced to compact peak/RMS arrays by
`tools/waveforms.py`. The browser receives no stem audio—only the visual
envelopes—and plays the master through the existing transport. Reference rows
are aligned from each file's DAW clip origin and grouped into a collapsible
block above the annotation tracks. This makes lead/backing vocal phrases,
drum-driven transition points, overall song density, and bass motion visible
without turning the editor into a multitrack audio player.

## Renderer integration

Python renderers can load the compiled file with:

```python
from timeline import TimelineRegister

register = TimelineRegister.load(compiled_path)
state = register.at(frame=frame_number)
scene = state["scene"]
lyric = state["lyric"]
drivers = state["drivers"]
```

Overlapping scenes and transitions remain available in `scenes` and
`transitions`; the singular values select the final active item in track order.
This lets renderers blend deliberately without embedding edit logic in a scene.

## AI collaboration

An AI can read a selected range, add or modify structured items, and mark them
with `ai.status: "suggestion"`. Suggestions remain visibly dashed in the editor
until accepted. The same validation and frame compilation applies to human and
AI changes.
