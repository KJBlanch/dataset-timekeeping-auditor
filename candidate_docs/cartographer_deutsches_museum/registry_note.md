# Cartographer Deutsches Museum

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `cartographer_deutsches_museum`
- Tier: `1`
- Domain: `lidar_imu_mapping`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_bag`
- Status: `candidate`

## Candidate URLs

- https://google-cartographer-ros.readthedocs.io/en/latest/data.html

## Expected sensors

- lidar
- imu

## Timing questions to investigate

- lidar_scan_time_semantics
- imu_time_alignment
- tf_timestamp_semantics

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
