# Synthetic smoke-test datasets

The repository includes a small generator for artificial timing datasets. These files are intended for CI and developer sanity checks, not for scientific evaluation.

## What is generated

`python scripts/generate_smoke_datasets.py --output-dir smoke` creates:

- `smoke/docs/synthetic_mass_good_readme.txt` — a maritime/MASS-style dataset README with explicit clock source, synchronization, timestamp semantics, and replay notes.
- `smoke/docs/synthetic_mass_undocumented_readme.txt` — a deliberately vague README that should receive a lower documentation score.
- `smoke/opendlv/opendlv_good/*.csv` — a tiny cluon-rec2fuse-style OpenDLV `.rec` export with monotonic `sample`, `sent`, and `received` timestamps.
- `smoke/opendlv/opendlv_bad/*.csv` — a tiny OpenDLV export with a deliberate timing irregularity and larger receive delay.
- `smoke/mcap/synthetic_mass_log.mcap` — a tiny MCAP file with one JSON-encoded topic, if the optional `mcap` Python package is installed.

## Local run

```bash
python -m pip install -e .
./scripts/run_smoke_audits.sh
```

The script regenerates the synthetic files, audits them, summarizes the outputs, and performs simple assertions:

- the well-documented README scores higher than the vague README;
- the OpenDLV export contains `sample`, `sent`, and `received` time fields;
- the deliberately bad OpenDLV export has a larger `received - sample` offset;
- the MCAP smoke file, when generated, contains one topic and 20 messages.

## Why this matters

The smoke tests let GitHub Actions verify the toolchain without downloading real robotic or maritime datasets. Real dataset audits can be run locally, on institutional storage, or on a self-hosted runner, while CI remains small and deterministic.


## GitHub Actions permission note

The workflow invokes the smoke script with `bash ./scripts/run_smoke_audits.sh` rather than relying on the executable bit. This avoids `Permission denied` failures when a script is copied onto Windows or committed without `chmod +x`. It is still safe to run locally as either:

```bash
bash ./scripts/run_smoke_audits.sh
# or, if executable permissions are preserved:
./scripts/run_smoke_audits.sh
```
