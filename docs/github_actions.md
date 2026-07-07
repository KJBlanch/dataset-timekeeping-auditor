# GitHub Actions automation

This repository includes two workflows:

- `.github/workflows/audit-examples.yml` runs a conservative timing-audit smoke test on the committed example files. It produces JSON, CSV, Markdown, and LaTeX outputs as downloadable workflow artifacts.
- `.github/workflows/docker-build.yml` verifies that the Docker image builds and can run the documentation auditor inside the container.

## Why the default workflow only audits examples

The survey is intended to avoid accidental multi-gigabyte downloads in CI. The default workflow therefore audits only small committed examples. For real datasets, prefer one of these patterns:

1. Download a deliberately small sample bag/log manually and commit only a metadata stub or checksum.
2. Store sample files in an external object store and require `workflow_dispatch` to download a specific file.
3. Run the auditors locally or on an institutional runner with access to a mounted dataset cache.
4. Upload the resulting `results/*.json` files to the repository, then let GitHub Actions summarize them.

## Manual run

Open the repository on GitHub, go to **Actions**, select **Audit examples**, then choose **Run workflow**.

## Local equivalent

```bash
python -m pip install -e .
./scripts/run_example_audits.sh
```

## Adding a real dataset audit job

For a small public file, add a separate workflow step that downloads the file and calls the relevant auditor. Keep the file size bounded and make the download opt-in where possible.

Example skeleton:

```yaml
- name: Download small sample
  if: github.event_name == 'workflow_dispatch'
  run: |
    mkdir -p data
    curl -L --fail --max-time 600 \
      -o data/sample.bag \
      "$SAMPLE_URL"

- name: Audit ROS 1 sample
  if: github.event_name == 'workflow_dispatch'
  run: |
    python -m dataset_time_auditor.audit_ros1_bag \
      data/sample.bag \
      --dataset my_dataset_sample \
      --output results/my_dataset_sample.json
```

## OpenDLV `.rec` files

The GitHub workflow does not attempt to parse binary `.rec` files directly. Export `.rec` files to CSV using the OpenDLV/libcluon workflow described in `opendlv_rec_workflow.md`, then run:

```bash
python -m dataset_time_auditor.audit_opendlv_rec_export \
  exported.csv \
  --dataset my_opendlv_dataset \
  --output results/my_opendlv_dataset.json
```
