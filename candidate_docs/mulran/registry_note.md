# MulRan

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `mulran`
- Tier: `2`
- Domain: `radar_lidar_gnss_imu_mapping`
- MASS relevance: `medium`
- Expected format: `raw_files_plus_ros_player`
- Target audit level: `L0`
- Download policy: `docs_and_player_semantics_first`
- Status: `candidate`

## Candidate URLs

- https://sites.google.com/view/mulran-pr/download

## Expected sensors

- radar
- lidar
- gnss
- imu

## Timing questions to investigate

- ros_player_timestamp_semantics
- radar_scan_time_vs_lidar_gnss_time
- conversion_loss_of_timing_metadata

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
