#!/usr/bin/env bash
# The iterate loop. Re-plan, re-slate, re-render, open it.
#
#   ./run.sh              beat-HUD animatic, opens when done  <- the everyday one
#   ./run.sh cut          the actual cut (footage where it exists, slates elsewhere)
#   ./run.sh final        1080p with the grade applied
#   ./run.sh status       what's shot and what isn't
#   ./run.sh prompts      regenerate prompts/prompts.md
#   ./run.sh board        rebuild the shot score + storyboard work order
#   ./run.sh timing       rebuild the beat grid + sections from source
#   ./run.sh stems        extract stem envelopes from the DAWproject (once)
#   ./run.sh world        export data + serve the 3D world, live with the audio
#   ./run.sh laser        export data + serve the VECTOR STAGE, live with audio
#   ./run.sh laserdraft                        whole song, low-fi, ~2 min
#   ./run.sh laserfinal [sec]                  THE MASTER: 1080p60, 32x
#   ./run.sh lasertest [from] [dur]            15s at master settings
#   ./run.sh laserprobe  [sec] [fps] [N]       time 40 frames of the vector stage
#   ./run.sh laserrender [sec|all] [fps] [N]   offline render (N defaults to 24)
#   ./run.sh capturebench [page] [w] [N]      time every frame-capture path
#   ./run.sh worldprobe  [sec] [fps] [N]       time 40 frames, report the real cost
#   ./run.sh worldrender [sec|all] [fps] [N]   offline render, N-sample motion blur
#   ./run.sh stage [sec|all] [fps] [draft|N]   the arrangement visualiser
#        default: 1920x1080, 60fps, 4x motion blur (slow — a final render)
#        draft:   1280x720, no blur (fast — for iterating)
#        N:       temporal supersampling factor, e.g. 8
#
# No venv activation needed — this uses .venv/bin/python3 directly.
set -e
cd "$(dirname "$0")"
PY=./.venv/bin/python3
[ -x "$PY" ] || { echo "no .venv — run: bash setup.sh"; exit 1; }

say() { printf "\n\033[1m▸ %s\033[0m\n" "$1"; }

# macOS keeps a stale handle on a file it already has open, so a re-render
# shows up as a black frozen video. Close the old window before writing.
close_player() {
  osascript -e 'tell application "System Events" to (name of processes) contains "QuickTime Player"' 2>/dev/null | grep -q true \
    && osascript -e 'tell application "QuickTime Player" to close every document' >/dev/null 2>&1 || true
}
show() { command -v open >/dev/null && open "$1" || true; }

case "${1:-cut}" in
  timing)
    close_player
    DP=$(ls source/*.dawproject 2>/dev/null | head -1)
    if [ -n "$DP" ]; then
      say "Beat grid (DAWproject: $DP)"
      $PY tools/dawproject.py "$DP" --compare --no-lyrics
    else
      say "Beat grid (MIDI)"
      $PY tools/beatmap.py midi/song.mid --audio audio/song.wav
    fi
    say "Lyrics";     $PY tools/lyrics.py lyrics/lyrics.md
    say "Click check"; $PY tools/clickcheck.py
    echo
    echo "  Now LISTEN to build/clickcheck.wav — start, middle, last chorus."
    show build/clickcheck.wav
    ;;
  plan)
    $PY tools/shotplan.py --merge >/dev/null
    $PY tools/plan_report.py
    ;;
  section)
    [ -n "$2" ] || { echo "usage: ./run.sh section <name>   (see ./run.sh plan)"; exit 1; }
    close_player
    say "Shot list"; $PY tools/shotplan.py --merge
    say "Animatic";  $PY tools/animatic.py --section "$2" --out "out/_$2.mp4"
    show "out/_$2.mp4"
    ;;
  cut)
    close_player
    say "Shot list"; $PY tools/shotplan.py --merge
    say "Slates";    $PY tools/previz.py >/dev/null && echo "wrote slates"
    say "Render";    $PY tools/render.py --proxy --out out/cut.mp4
    show out/cut.mp4
    ;;
  stems)
    DP=$(ls source/*.dawproject 2>/dev/null | head -1)
    [ -n "$DP" ] || { echo "no .dawproject in source/"; exit 1; }
    say "Stem envelopes"; $PY tools/stems.py "$DP"
    ;;
  stage)
    close_player
    [ -f analysis/envelopes.json ] || { echo "run ./run.sh stems first"; exit 1; }
    SEC="${2:-}"
    FPS=${3:-60}
    Q="${4:-}"
    EXTRA=""
    case "$Q" in
      draft) EXTRA="--draft" ;;
      ''|*[!0-9]*) ;;                      # not a number: leave defaults
      *) EXTRA="--blur $Q" ;;              # a number: temporal supersampling
    esac
    case "$SEC" in all|-|"") SEC="" ;; esac
    if [ -n "$SEC" ]; then
      say "Stage: $SEC @ ${FPS}fps ${Q:-default}"
      $PY tools/stage.py --section "$SEC" --fps "$FPS" $EXTRA --out "out/stage_$SEC.mp4"
      show "out/stage_$SEC.mp4"
    else
      say "Stage: whole song @ ${FPS}fps ${Q:-default}"
      $PY tools/stage.py --fps "$FPS" $EXTRA --out out/stage.mp4
      show out/stage.mp4
    fi
    ;;
  world)
    say "Exporting the musical substrate"; $PY tools/world_export.py
    say "Shot score";                      $PY tools/world_shots.py
    say "Serving"
    ( sleep 1; command -v open >/dev/null && open "http://127.0.0.1:8747/world/" ) &
    $PY tools/serve.py 8747
    ;;
  laser)
    say "Musical substrate (notes, lanes, features)"; $PY tools/stage_export.py
    say "Serving"
    ( sleep 1; command -v open >/dev/null && open "http://127.0.0.1:8748/stage/" ) &
    $PY tools/serve.py 8748
    ;;
  capturebench)
    [ -f stage/data.json ] || $PY tools/stage_export.py >/dev/null
    say "Timing every way of getting a frame out of the browser"
    $PY tools/capture_bench.py --page "${2:-stage}" --width "${3:-1920}" \
        --blur "${4:-8}"
    ;;
  laserdraft)
    # a whole-song look in a couple of minutes: half resolution, 24fps, light
    # blur. Not for judging the vibration — for judging the staging.
    say "Draft render (854x480, 24fps, 2x)"
    $PY tools/stage_export.py >/dev/null
    close_player
    $PY tools/world_render.py --page stage --fps 24 --blur 2 --width 854 \
        --jpeg 82 --port 8755 --out out/laser_draft.mp4 && show out/laser_draft.mp4
    ;;
  laserfinal)
    # The master. 1080p60, 32x temporal supersampling — which the lyric
    # vibration and the bass shimmer both need to resolve rather than alias —
    # a near-lossless JPEG intermediate, and x264 at CRF 15 on the slow preset
    # because smooth glow on black bands long before it loses detail.
    #   ./run.sh laserfinal            the whole song
    #   ./run.sh laserfinal chorus-1   one section, same quality
    say "Musical substrate"; $PY tools/stage_export.py
    SEC="${2:-}"
    close_player
    ARGS="--page stage --fps 60 --blur 32 --width 1920 --jpeg 97 --crf 15 \
          --preset slow --abr 320k --port 8757"
    if [ -n "$SEC" ] && [ "$SEC" != "all" ]; then
      say "Final render: $SEC"
      $PY tools/world_render.py $ARGS --section "$SEC" \
          --out "out/visualization_$SEC.mp4" && show "out/visualization_$SEC.mp4"
    else
      say "Final render: whole song (expect 10-20 min)"
      $PY tools/world_render.py $ARGS --out out/visualization.mp4 && show out/visualization.mp4
    fi
    ;;
  lasertest)
    # Fifteen seconds at EXACTLY the master settings — same resolution, same
    # 32x supersampling, same encoder — so what you see is what the full run
    # will give you. Default window straddles the verse-1 -> chorus-1 boundary
    # at 0:39.7, which exercises a section change, a name-card debut, the
    # lyrics and the MIDI in one go.
    #   ./run.sh lasertest            34s, 15 seconds
    #   ./run.sh lasertest 96 20      from 1:36, 20 seconds
    say "Musical substrate"; $PY tools/stage_export.py >/dev/null
    FROM="${2:-34}"; DUR="${3:-15}"
    close_player
    say "Test render at FINAL quality: ${FROM}s +${DUR}s (1080p60, 32x)"
    $PY tools/world_render.py --page stage --fps 60 --blur 32 --width 1920 \
        --jpeg 97 --crf 15 --preset slow --abr 320k --port 8758 \
        --from "$FROM" --dur "$DUR" --out out/visualization_test.mp4 \
      && show out/visualization_test.mp4
    ;;
  laserprobe)
    [ -f stage/data.json ] || { say "Musical substrate"; $PY tools/stage_export.py; }
    say "Probing the vector stage (40 frames)"
    $PY tools/world_render.py --page stage --section "${2:-chorus-1}" \
        --fps "${3:-60}" --blur "${4:-8}" --probe 40 --port 8753
    ;;
  laserrender)
    say "Rendering the vector stage"
    $PY tools/stage_export.py >/dev/null
    # the lyric vibration runs near audio rate, so it needs real temporal
    # supersampling to resolve — 24 is the floor for it to read as a smear
    # rather than a jitter. The GPU is 0.4ms a sub-frame; this is affordable.
    SEC="${2:-}"; FPS="${3:-60}"; N="${4:-24}"
    close_player
    if [ -n "$SEC" ] && [ "$SEC" != "all" ]; then
      $PY tools/world_render.py --page stage --section "$SEC" --fps "$FPS" \
          --blur "$N" --port 8754 --out "out/laser_$SEC.mp4" \
        && show "out/laser_$SEC.mp4"
    else
      $PY tools/world_render.py --page stage --fps "$FPS" --blur "$N" \
          --port 8754 --out out/laser.mp4 && show out/laser.mp4
    fi
    ;;
  worldprobe)
    say "Probing render speed (40 frames)"
    $PY tools/world_render.py --section "${2:-turn}" --fps "${3:-60}" \
        --blur "${4:-8}" --probe 40 --port 8752
    ;;
  worldrender)
    say "Rendering the world"
    $PY tools/world_export.py >/dev/null && $PY tools/world_shots.py >/dev/null
    SEC="${2:-}"; FPS="${3:-60}"; N="${4:-8}"
    close_player
    if [ -n "$SEC" ] && [ "$SEC" != "all" ]; then
      $PY tools/world_render.py --section "$SEC" --fps "$FPS" --blur "$N" \
          --out "out/world_$SEC.mp4" && show "out/world_$SEC.mp4"
    else
      $PY tools/world_render.py --fps "$FPS" --blur "$N" --out out/world.mp4 \
        && show out/world.mp4
    fi
    ;;
  status)
    $PY tools/ingest.py --status
    ;;
  prompts)
    $PY tools/prompts.py
    show prompts/prompts.md
    ;;
  board)
    say "Shot score";   $PY tools/world_shots.py
    say "Work order";   $PY tools/board_prompts.py
    say "Galleries";    $PY tools/board_gallery.py both
    show board/refs.html
    ;;
  final)
    close_player
    say "Shot list"; $PY tools/shotplan.py --merge
    say "Slates";    $PY tools/previz.py
    say "Render";    $PY tools/render.py --grade throwback --out out/cut.mp4
    show out/cut.mp4
    ;;
  *)
    close_player
    say "Shot list"; $PY tools/shotplan.py --merge
    say "Animatic";  $PY tools/animatic.py --out out/animatic.mp4
    show out/animatic.mp4
    ;;
esac
