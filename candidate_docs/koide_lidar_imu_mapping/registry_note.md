# Koide LiDAR-IMU Mapping Test Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `koide_lidar_imu_mapping`
- Tier: `1`
- Domain: `lidar_inertial_mapping`
- MASS relevance: `medium`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_bag`
- Status: `candidate`

## Candidate URLs

- https://zenodo.org/records/6836915

## Expected sensors

- lidar
- imu

## Timing questions to investigate

- lidar_scan_time_vs_imu_sample_time
- header_stamp_vs_record_time

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
