# UTBM Robocar / EU Long-term Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `utbm_robocar`
- Tier: `2`
- Domain: `autonomous_vehicle_multisensor`
- MASS relevance: `medium`
- Expected format: `ros1_bag`
- Target audit level: `L0`
- Download policy: `docs_first`
- Status: `candidate`

## Candidate URLs

- https://epan-utbm.github.io/utbm_robocar_dataset/

## Expected sensors

- lidar
- radar
- cameras
- gnss
- imu

## Timing questions to investigate

- long_duration_clock_drift_documentation
- multi_sensor_sync_and_rosbag_time

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
