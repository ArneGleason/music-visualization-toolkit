# Word-level lyric timing (optional)

You almost certainly don't need this. Line-level timing from `[bar.beat]`
markers is enough to plan shots and put text on screen. Word-level only earns
its keep if you want per-word visual hits — a cut, flash or graphic landing on
one specific syllable.

If you do want it, you're in a good position: you already have an isolated
vocal stem, which is the hard part.

## Route

```bash
pip install stable-ts        # whisper wrapper with decent word timestamps
# or: pip install whisperx   # better alignment, heavier install

stable-ts audio/vocal.wav --model large-v3 \
  --output analysis/words.json --output_format json \
  --word_timestamps True
```

Feeding your known lyric text as a prior improves it substantially — both
tools accept a transcript to align against rather than transcribing blind.
Sung vocals, held notes and melisma are where automatic alignment gets vague;
a text prior removes most of that ambiguity.

Then snap to the grid:

```python
from mvlib import Beatmap
bm = Beatmap.load()
for w in words:
    w["sec"] = bm.snap(w["sec"], 0.5)   # nearest 8th note
```

Snapping matters more than raw accuracy. A word placed 60 ms off the grid
reads as sloppy; the same word snapped to the nearest eighth reads as
intentional, even when it's further from the true onset.

## If you skip the stem

`demucs` will separate a vocal from the mix if you ever need one you don't
have:

```bash
pip install demucs
demucs --two-stems=vocals audio/song.wav -o build/
```
