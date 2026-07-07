#!/usr/bin/env bash
set -euo pipefail

mkdir -p results/candidate_docs tables

if [ ! -f candidate_datasets.yaml ]; then
  echo "candidate_datasets.yaml not found. Run from repository root." >&2
  exit 1
fi

python - <<'PY'
from pathlib import Path
import subprocess
import sys
import yaml

root = Path.cwd()
registry = yaml.safe_load(Path('candidate_datasets.yaml').read_text(encoding='utf-8'))
candidates = registry.get('candidates', [])
outputs = []
missing = []

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

if missing:
    print('Missing documentation folders skipped:')
    for dataset_id in missing:
        print(f'  - {dataset_id}')
PY
