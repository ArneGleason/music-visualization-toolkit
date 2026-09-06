# Rough v03 feedback and sync audit

2026-09-05. Owner likes the rough's structure, content and musical effects.
Some generated motion is strange and will be marked for selective replacement.
Remove the global flash on the next pass. Lip sync is inconsistent compared
with earlier previews. Investigate assembly first, before regenerating assets.
This pass is diagnosis and planning only: no assembler changes or new movie.

## Confirmed assembly defect: 30 fps footage playing frame-for-frame at 24 fps

The Blender assembler imports movies without a time-preserving frame-rate
conversion. A direct test with the installed Blender 5.2.1 and s003's source
reports 30 fps, 239 source frames, and 239 timeline frames in a 24 fps scene.
That makes roughly 7.97 seconds of source occupy roughly 9.96 seconds before
cut trimming. Performance advances at 80% of its intended speed.

Actual rough frames were matched against decoded source images using normalized
grayscale correlation, excluding lyrics. This confirms the problem in the
rendered picture, not just the import metadata:

| Shot | Absolute song frame | Observed source frame | Required at real-time speed | Correlation |
| --- | ---: | ---: | ---: | ---: |
| s003 | 179 | 24 | 30 | 0.99770 |
| s003 | 227 | 72 | 90 | 0.99248 |
| s003 | 275 | 120 | 150 | 0.99769 |
| s034 | 2764 | 81 | 101 | 0.99559 |
| s034 | 2812 | 128 | 161 | 0.99512 |
| s034 | 2848 | 164 | 206 | 0.99421 |

s003 is approximately one second behind after five seconds. A constant offset
cannot correct this growing error. s034 also begins too early inside its source
because the in-point is calculated at output fps and applied to source frames.
Its later-frame matches are within one frame of that faulty frame-for-frame
prediction. Image correlation on similar neighboring frames is not phoneme QA.

Affected assignments: s003, s005, s007, s012, s014, s026, s031, s033, s034,
s042, s045, s046. All use 30 fps Kling files. New outro takes are already
normalized to 24 fps, so this specific mismatch does not apply there. Spot
matches on o06 are within 1-2 source frames of the expected mapping, but do
not establish exact mouth/audio sync or justify a blanket offset.

The seven rendered parts have exactly 720/720/720/720/720/720/462 frames.
The final has 4782 frames and one continuous master track. There is no evidence
of accumulated missing section frames. All assigned speeds are 1.0.

The previous preflight checked source duration but did not check Blender's
playback interpretation. The completed render therefore passed coverage checks
while still containing an assembly sync defect. Fix that validation gap.

## Other findings and uncertainties

- The global flash is an additive full-frame strip in `tools/blender_comp.py`,
  named `beat_pulse`. Peaks are 0.55 at section starts, 0.30 on downbeats,
  0.12 on other beats. This is distinct from the accepted local light/bloom FX.
  Owner wants the global layer removed, not those intentional local effects.
- Handoff notes say early Kling guides were eight-second vocal excerpts beginning
  at the cut, without intentional pre-roll. This supports investigating clipped
  first phonemes, but it does not prove Kling startup failure in each clip.
- s033/s034 used the entire vocal excerpt on Character 1. Speaker separation
  remains a known independent issue; correcting playback cannot fix wrong mouths.
- Earlier handoff reports strong audio correlation between downloads and guides.
  That establishes file identity, not that the face is synchronized to each word.
- Generated-motion oddities should be logged by shot/time during the owner's
  review. Do not infer an exhaustive regeneration list from this timing audit.

## Next pass, in order

1. Disable the global beat-pulse layer by default, keeping local FX untouched.
2. Preserve original Kling files. Derive silent 24 fps constant-frame-rate
   assembly proxies using timestamp-based resampling, never reinterpret 30 frames
   as one 24 fps second. Keep duration/song origin, with any end-frame padding
   explicit and no audio time stretch. Resolve source in-points in seconds on
   the normalized timeline. Record source/proxy mapping and verify in/out points.
3. Add regression checks: a synthetic numbered 30 fps clip must advance by
   30 source frames per second in a 24 fps assembly, including a nonzero in-point.
   Preflight must reject unhandled fps mismatches instead of only checking length.
4. Render short no-flash comparisons of s003 and a nonzero-in-point shot such as
   s034 or s042. Compare early, middle and late mouth landmarks with the guide
   and original preview. Fix clock/rate before considering a per-take offset.
5. For residual constant error, compare the source's embedded guide, uploaded
   guide and master vocal placement. Store any justified offset once per take,
   in frames, applying it consistently across every return. Never globally shift
   the soundtrack or disturb accepted FX/lyric timing to repair one face.
6. For error restricted to the first word, try an existing earlier part of the
   continuous take. If new sync is needed, test 0.5-1.0 seconds of genuine earlier
   performance and matching guide audio. Do not insert silence and call it lead-in.
   Record guide origin, visual origin and pre-roll explicitly, then cut into the
   synced result at the editorial boundary. This is an explicit exception to the
   simple exit-only handle workflow, not a silent shift of the song clock.
7. If lips are still wrong after rate and alignment corrections, handle those
   as performance/model failures. Split the duet guides by speaker and regenerate
   selectively. Avoid regenerating otherwise good clips prematurely.
8. Rebuild the full 720p rough with a fresh filename and fresh segment cache.
   The current segmented runner skips existing parts by filename, so reusing the
   v03 name could accidentally reuse the faulty render. Review the whole arc.

## Review log format

For each issue record: shot ID, rough timestamp, symptom (motion / rate drift /
constant offset / first-word onset / wrong speaker), intended change, status,
source take and affected returns. Keep original media as spares. Use a broad
review pass, then targeted tests, rather than polishing one clip repeatedly.
