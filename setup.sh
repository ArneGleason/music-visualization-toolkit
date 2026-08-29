#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

say() { printf "\n\033[1m▸ %s\033[0m\n" "$1"; }
fail() { printf "\n\033[31m✗ %s\033[0m\n" "$1"; exit 1; }

say "Checking prerequisites"
command -v python3 >/dev/null || fail "python3 not found"
command -v ffmpeg >/dev/null || fail "ffmpeg not found"
command -v ffprobe >/dev/null || fail "ffprobe not found"

say "Creating Python environment"
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip install --quiet --retries 5 --timeout 60 -r requirements.txt
./.venv/bin/python3 -c "import mido, PIL, playwright"

say "Installing Playwright Chromium"
./.venv/bin/python3 -m playwright install chromium

say "Creating project directories"
mkdir -p audio midi lyrics source analysis shots prompts refs \
  clips/inbox clips/raw board/frames board/refs board/refpacks board/rejects \
  build out

say "Ready"
echo "  Add your project inputs, then read README.md for the timing and render loops."
