# Dataset Timekeeping Auditor

A starter toolkit for surveying timekeeping practices in robotic perception datasets that use middleware or middleware-like log containers.

The project is intentionally conservative: it reports what it can directly observe from logs and documents, and marks the rest as `unknown` rather than inferring clock discipline or synchronization quality.

## Supported audit targets

- ROS 1 bag files (`.bag`)
- ROS 2 bag directories / SQLite databases (`metadata.yaml`, `.db3`)
- MCAP files (`.mcap`)
- OpenDLV / libcluon `.rec` recordings via external `cluon-rec2fuse` CSV export, plus a lightweight metadata wrapper
- Dataset documentation files (`README.md`, `.txt`, extracted PDF text, web page dumps)

## Why OpenDLV `.rec` is handled differently

OpenDLV/libcluon recordings are dumps of exchanged `Envelope` messages. The most robust way to inspect them without reimplementing libcluon decoding in Python is to mount/export them using `cluon-rec2fuse`, which maps envelopes and messages into CSV files including `sent`, `received`, and `sample time point` timestamps. This toolkit therefore provides an auditor for the exported CSV directory, not a full binary `.rec` decoder.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m dataset_time_auditor.audit_docs examples/example_dataset_readme.txt \
  --dataset example_docs \
  --output results/example_docs.json

python -m dataset_time_auditor.summarize results/*.json \
  --csv results/timing_summary.csv \
  --markdown results/timing_summary.md \
  --latex results/timing_summary.tex
```

## Docker

```bash
docker build -t dataset-time-auditor .

docker run --rm -v "$PWD:/work" dataset-time-auditor \
  python -m dataset_time_auditor.audit_docs /work/examples/example_dataset_readme.txt \
  --dataset example_docs \
  --output /work/results/example_docs.json
```

## Typical workflow

1. Add candidate datasets to `datasets.yaml`.
2. Perform an L0 documentation audit using `audit_docs`.
3. Download only one small bag/sequence where possible.
4. Run the relevant empirical auditor.
5. Use `summarize` to generate paper tables.

## Audit levels

| Level | Download required | Output |
|---|---:|---|
| L0 documentation audit | none / docs only | claimed clock source, sync method, timestamp terms |
| L1 metadata/sample audit | small bag or exported metadata | topics, field availability, coarse timestamp ranges |
| L2 sequence audit | one sequence/log | quantitative record-vs-message timestamp offsets, gaps, monotonicity |

## Result schema

Each auditor emits JSON with these top-level fields:

```json
{
  "dataset_id": "...",
  "audit_type": "ros1_bag|ros2_bag|mcap|opendlv_rec_export|docs",
  "audit_level": "L0|L1|L2",
  "generated_at_utc": "...",
  "source": "...",
  "summary": {},
  "topics": [],
  "documentation": {},
  "warnings": [],
  "errors": []
}
```

## Conservative interpretation

A small `record_time - header_stamp` offset does **not** prove correct sensor time. It only proves that the middleware record timestamp and embedded message timestamp are close for the inspected sample. The paper should treat this as evidence of timestamp consistency, not absolute synchronization quality.

## GitHub automation

The repository includes GitHub Actions workflows under `.github/workflows/`:

- `audit-examples.yml` runs the documentation and OpenDLV export auditors on the committed example files, summarizes the outputs, and uploads JSON/CSV/Markdown/LaTeX artifacts.
- `docker-build.yml` builds the Docker image and runs a smoke test inside the container.

The default CI deliberately avoids downloading real datasets. This keeps the workflow cheap and prevents accidental multi-gigabyte CI jobs. For real datasets, run the auditors locally or on a self-hosted/institutional runner with a dataset cache, then commit or upload the resulting `results/*.json` files for summarization.

Local equivalent:

```bash
python -m pip install -e .
./scripts/run_example_audits.sh
```

See `docs/github_actions.md` for workflow extension patterns, including manual `workflow_dispatch` jobs for small sample downloads.

## Synthetic smoke tests

The repository can generate tiny synthetic datasets for CI and local sanity checks without downloading real robotic datasets:

```bash
python -m pip install -e .
./scripts/run_smoke_audits.sh
```

This creates a well-documented MASS-style README, an intentionally under-documented README, good/bad OpenDLV `.rec` CSV exports, and—when `mcap` is installed—a tiny MCAP log. The script audits them, summarizes the results, and runs assertions that catch basic parser regressions. See `docs/smoke_tests.md`.
