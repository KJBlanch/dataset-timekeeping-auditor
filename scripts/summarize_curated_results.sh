#!/usr/bin/env bash
set -euo pipefail

RESULTS_GLOB="${1:-results/curated/*.json}"
mkdir -p tables
python -m dataset_time_auditor.summarize "$RESULTS_GLOB" \
  --csv tables/timing_summary.csv \
  --markdown tables/timing_summary.md \
  --latex tables/timing_summary.tex
