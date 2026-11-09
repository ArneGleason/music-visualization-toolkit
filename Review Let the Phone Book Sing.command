#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
./.venv/bin/python3 projects/let-the-phone-book-sing/production/open_review.py
