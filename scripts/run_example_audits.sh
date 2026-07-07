#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p results

python -m dataset_time_auditor.audit_docs \
  examples/example_dataset_readme.txt \
  --dataset example_docs \
  --output results/example_docs.json

python -m dataset_time_auditor.audit_opendlv_rec_export \
  examples/example_opendlv_export.csv \
  --dataset example_opendlv \
  --output results/example_opendlv.json

python -m dataset_time_auditor.summarize 'results/*.json' \
  --csv results/timing_summary.csv \
  --markdown results/timing_summary.md \
  --latex results/timing_summary.tex
