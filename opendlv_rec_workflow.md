# OpenDLV / libcluon `.rec` workflow

This toolkit does not attempt to decode binary `.rec` files directly in Python. Instead, use the canonical libcluon/OpenDLV ecosystem to expose the recording as CSV and then audit the CSV structure.

## Option A: mount/export using `cluon-rec2fuse`

The `cluon-rec2fuse` tool maps a `.rec` file into CSV files, including envelope/message timestamps such as `sent`, `received`, and `sample time point` where available.

Conceptual workflow:

```bash
mkdir -p mnt
# Exact image/tag and arguments may vary by your installed libcluon tooling.
# Provide the relevant .odvd message specification when required.
cluon-rec2fuse --rec myrecording.rec --odvd opendlv.odvd mnt

python -m dataset_time_auditor.audit_opendlv_rec_export mnt \
  --dataset my_opendlv_recording \
  --output results/my_opendlv_recording.json
```

## Option B: convert to CSV with existing OpenDLV tooling

If you already use a project-specific `.rec` to CSV converter, point the auditor at the output directory:

```bash
python -m dataset_time_auditor.audit_opendlv_rec_export exported_csv/ \
  --dataset my_opendlv_recording \
  --output results/my_opendlv_recording.json
```

## What the auditor checks

For each CSV file, the auditor looks for columns corresponding to:

- `sent` time
- `received` time
- `sample time point`

It then reports monotonicity and differences such as:

- `received - sent`
- `received - sample`
- `sent - sample`

## Interpretation notes

- `received` is usually a middleware reception/recording-side time, not necessarily sensor acquisition time.
- `sent` is closer to publisher-side middleware time, but still not always sensor acquisition time.
- `sample time point`, when present and correctly populated by the message producer, is usually the most relevant semantic field for sensor measurements.
- `.rec` replay can preserve envelope timing, but the paper should explicitly distinguish replay timing from original sample/acquisition timing.
