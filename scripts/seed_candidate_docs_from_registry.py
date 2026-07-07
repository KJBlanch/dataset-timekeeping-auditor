#!/usr/bin/env python3
"""Create lightweight registry-note documentation folders for candidate datasets.

These files are deliberately marked as registry-derived notes. They are useful for
CI plumbing and for checking that the documentation-audit pipeline runs end-to-end,
but they are not a substitute for source documentation copied/fetched from dataset
pages, papers, or READMEs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def fmt_list(values: Any) -> str:
    if not values:
        return "- unknown\n"
    if not isinstance(values, list):
        values = [values]
    return "".join(f"- {v}\n" for v in values)


def main() -> None:
    ap = argparse.ArgumentParser(description="Seed candidate_docs/<dataset_id>/registry_note.md from candidate_datasets.yaml")
    ap.add_argument("--registry", default="candidate_datasets.yaml")
    ap.add_argument("--out-dir", default="candidate_docs")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    registry_path = Path(args.registry)
    out_root = Path(args.out_dir)
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    candidates = registry.get("candidates", [])

    created = 0
    skipped = 0
    for cand in candidates:
        dataset_id = cand["id"]
        doc_dir = out_root / dataset_id
        doc_dir.mkdir(parents=True, exist_ok=True)
        note_path = doc_dir / "registry_note.md"
        if note_path.exists() and not args.overwrite:
            skipped += 1
            continue

        text = f"""# {cand.get('name', dataset_id)}

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `{dataset_id}`
- Tier: `{cand.get('tier', 'unknown')}`
- Domain: `{cand.get('domain', 'unknown')}`
- MASS relevance: `{cand.get('mass_relevance', 'unknown')}`
- Expected format: `{cand.get('format_expected', 'unknown')}`
- Target audit level: `{cand.get('audit_level_target', 'unknown')}`
- Download policy: `{cand.get('download_policy', 'unknown')}`
- Status: `{cand.get('status', 'unknown')}`

## Candidate URLs

{fmt_list(cand.get('candidate_urls'))}
## Expected sensors

{fmt_list(cand.get('sensors_expected'))}
## Timing questions to investigate

{fmt_list(cand.get('timing_questions'))}
## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
"""
        note_path.write_text(text, encoding="utf-8")
        created += 1

    print(f"Seeded registry notes: created={created}, skipped={skipped}, out_dir={out_root}")


if __name__ == "__main__":
    main()
