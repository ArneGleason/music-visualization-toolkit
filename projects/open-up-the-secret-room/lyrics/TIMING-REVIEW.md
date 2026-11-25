# Lyric timing review

The [first animatic](../generated/animatic/Open-Up-the-Secret-Room-lyric-timing-v001.mp4) uses the full master and the Bitwig bar and beat grid at 24 fps. The highlight follows the proposed word edges. Listen for the attack and release of each word before using it for a cut. The [author sheet](author.txt) preserves all 57 lines and the [editable register](../timeline.json) records 56 placed lines and 326 word timing candidates.

The timing pass compared independent local Whisper runs on the master and the loop-matched de-echoed vocal, then aligned the supplied wording against both sources with Wav2Vec2 acoustic scores. The master recovered phrases missing from the vocal-only Whisper pass. Timing uses elapsed time from the master start, which is Bitwig `4.3.1.00`. Text guesses in machine transcripts are retained as evidence in `generated/transcription/`. The authored wording is used in the edit.

## Playback checks

| Master time | Check |
| --- | --- |
| 0:19–0:27 | The end of “Time still staring at the room” and the first “here on the moon” rely partly on the master because the de-echoed vocal loses that material. Check the held “moon”. |
| 0:38–0:44 | The lyric sheet says “Nev”. The master pass heard “Never”. Check the “here” repeats and the article before “moon”. |
| 1:09–1:13, 2:14–2:18, 3:12–3:15 | Check the group timing of the “oh” echoes. The animatic shows an approximate window for each group. |
| 1:42–1:45 | The master pass heard “Hearts” where the sheet says “Parts”. |
| 1:51–1:56, 2:29–2:33 | Check the “shelf” and “self” tails and the later “show” repeats. |
| 3:01.60–3:02.50 | Line 46, “Secret room”, remains unplaced. The master pass heard an “ooh” in this window. The animatic shows the line as a review cue. |
| 3:21–3:28 | Check “You make a great escape”, the doubled “here” and the held “moon”. The word choices in the machine transcript differed. |
| 3:36–3:39 | Check the tail of “room” before the final “I gotta sign off”. |

To render the next revision after editing the register, choose a new version number. The editable register uses master-relative word times and DAWproject bar, beat and tick positions. Existing renders are kept as review references.

```powershell
./.venv/Scripts/python.exe projects/open-up-the-secret-room/production/render_lyric_review.py projects/open-up-the-secret-room/project.json --version 2
```
