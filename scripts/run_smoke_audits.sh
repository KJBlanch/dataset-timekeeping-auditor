#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SMOKE_DIR="${SMOKE_DIR:-smoke}"
RESULTS_DIR="${RESULTS_DIR:-results/smoke}"

mkdir -p "$RESULTS_DIR"
python scripts/generate_smoke_datasets.py --output-dir "$SMOKE_DIR"

python -m dataset_time_auditor.audit_docs \
  "$SMOKE_DIR/docs/synthetic_mass_good_readme.txt" \
  --dataset smoke_docs_good \
  --output "$RESULTS_DIR/smoke_docs_good.json"

python -m dataset_time_auditor.audit_docs \
  "$SMOKE_DIR/docs/synthetic_mass_undocumented_readme.txt" \
  --dataset smoke_docs_undocumented \
  --output "$RESULTS_DIR/smoke_docs_undocumented.json"

python -m dataset_time_auditor.audit_opendlv_rec_export \
  "$SMOKE_DIR/opendlv/opendlv_good" \
  --dataset smoke_opendlv_good \
  --output "$RESULTS_DIR/smoke_opendlv_good.json"

python -m dataset_time_auditor.audit_opendlv_rec_export \
  "$SMOKE_DIR/opendlv/opendlv_bad" \
  --dataset smoke_opendlv_bad \
  --output "$RESULTS_DIR/smoke_opendlv_bad.json"

if [[ -f "$SMOKE_DIR/mcap/synthetic_mass_log.mcap" ]]; then
  python -m dataset_time_auditor.audit_mcap \
    "$SMOKE_DIR/mcap/synthetic_mass_log.mcap" \
    --dataset smoke_mcap \
    --output "$RESULTS_DIR/smoke_mcap.json" \
    --max-messages-per-topic 100
fi

python -m dataset_time_auditor.summarize "$RESULTS_DIR/*.json" \
  --csv "$RESULTS_DIR/timing_summary.csv" \
  --markdown "$RESULTS_DIR/timing_summary.md" \
  --latex "$RESULTS_DIR/timing_summary.tex"

python - <<'PY'
from __future__ import annotations
import json
from pathlib import Path

results = Path('results/smoke')
good = json.loads((results / 'smoke_docs_good.json').read_text())
bad = json.loads((results / 'smoke_docs_undocumented.json').read_text())
assert good['summary']['total'] > bad['summary']['total'], 'good docs should score higher than undocumented docs'

opendlv_good = json.loads((results / 'smoke_opendlv_good.json').read_text())
opendlv_bad = json.loads((results / 'smoke_opendlv_bad.json').read_text())
assert opendlv_good['summary']['files_with_sent_time'] == 1
assert opendlv_good['summary']['files_with_received_time'] == 1
assert opendlv_good['summary']['files_with_sample_time_point'] == 1

good_offset = opendlv_good['topics'][0]['received_minus_sample_s']['mean']
bad_offset = opendlv_bad['topics'][0]['received_minus_sample_s']['mean']
assert bad_offset > good_offset, 'bad OpenDLV export should have larger receive-sample offset'

mcap_path = results / 'smoke_mcap.json'
if mcap_path.exists():
    mcap = json.loads(mcap_path.read_text())
    assert mcap['summary']['topic_count'] == 1
    assert mcap['summary']['total_messages_sampled'] == 20

print('Smoke assertions passed')
PY

cat "$RESULTS_DIR/timing_summary.md"
