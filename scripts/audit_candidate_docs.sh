#!/usr/bin/env bash
set -euo pipefail

AUTO_SEED=1
SEED_MISSING=0
FETCH=0
FAIL_IF_EMPTY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fetch)
      FETCH=1
      shift
      ;;
    --seed-missing)
      SEED_MISSING=1
      shift
      ;;
    --no-auto-seed)
      AUTO_SEED=0
      shift
      ;;
    --fail-if-empty)
      FAIL_IF_EMPTY=1
      shift
      ;;
    -h|--help)
      cat <<'EOF'
Usage: bash ./scripts/audit_candidate_docs.sh [options]

Options:
  --fetch           Best-effort lightweight fetch of candidate URL text/HTML before auditing.
  --seed-missing    Create registry-note placeholders for missing candidate_docs folders.
  --no-auto-seed    Do not auto-seed registry notes when candidate_docs is empty.
  --fail-if-empty   Exit non-zero if no documentation folders can be audited.

Default behavior: if candidate_docs contains no candidate folders, registry-note
placeholders are generated so the workflow produces a pipeline sanity result.
These placeholders are explicitly marked as not source documentation.
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

mkdir -p results/candidate_docs tables

if [ ! -f candidate_datasets.yaml ]; then
  echo "candidate_datasets.yaml not found. Run from repository root." >&2
  exit 1
fi

if [ "$FETCH" -eq 1 ]; then
  python ./scripts/fetch_candidate_docs.py || true
fi

EXISTING_COUNT=$(python - <<'PY'
from pathlib import Path
import yaml
registry = yaml.safe_load(Path('candidate_datasets.yaml').read_text(encoding='utf-8'))
ids = [c['id'] for c in registry.get('candidates', [])]
print(sum(1 for i in ids if (Path('candidate_docs') / i).exists()))
PY
)

if [ "$SEED_MISSING" -eq 1 ]; then
  python ./scripts/seed_candidate_docs_from_registry.py
elif [ "$AUTO_SEED" -eq 1 ] && [ "$EXISTING_COUNT" -eq 0 ]; then
  echo "No candidate documentation folders found. Seeding registry-note placeholders for CI sanity checks."
  echo "These are not source documentation; replace them with real README/paper/page notes for the survey."
  python ./scripts/seed_candidate_docs_from_registry.py
fi

python - <<'PY'
from pathlib import Path
import subprocess
import sys
import yaml

registry = yaml.safe_load(Path('candidate_datasets.yaml').read_text(encoding='utf-8'))
candidates = registry.get('candidates', [])
outputs = []
missing = []
registry_note_only = []

for cand in candidates:
    dataset_id = cand['id']
    doc_dir = Path('candidate_docs') / dataset_id
    if not doc_dir.exists():
        missing.append(dataset_id)
        continue
    text_files = []
    for pattern in ('*.md', '*.txt', '*.rst', '*.yaml', '*.yml'):
        text_files.extend(doc_dir.rglob(pattern))
    if not text_files:
        missing.append(dataset_id)
        continue
    non_registry_files = [p for p in text_files if p.name != 'registry_note.md']
    if not non_registry_files:
        registry_note_only.append(dataset_id)
    out = Path('results/candidate_docs') / f'{dataset_id}.json'
    subprocess.check_call([
        sys.executable, '-m', 'dataset_time_auditor.audit_docs',
        str(doc_dir), '--dataset', dataset_id, '--output', str(out)
    ])
    outputs.append(str(out))

if outputs:
    subprocess.check_call([
        sys.executable, '-m', 'dataset_time_auditor.summarize',
        *outputs,
        '--csv', 'tables/candidate_docs_summary.csv',
        '--markdown', 'tables/candidate_docs_summary.md',
        '--latex', 'tables/candidate_docs_summary.tex',
    ])
    print(f'Audited {len(outputs)} candidate documentation folders.')
else:
    print('No candidate documentation folders found. Add files under candidate_docs/<dataset_id>/.')

if registry_note_only:
    print('Registry-note-only folders audited as placeholders, not evidence:')
    for dataset_id in registry_note_only:
        print(f'  - {dataset_id}')

if missing:
    print('Missing documentation folders skipped:')
    for dataset_id in missing:
        print(f'  - {dataset_id}')
PY

if [ "$FAIL_IF_EMPTY" -eq 1 ] && [ ! -f tables/candidate_docs_summary.csv ]; then
  exit 1
fi
