# KAIST VIO Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `kaist_vio`
- Tier: `1`
- Domain: `vehicle_visual_inertial`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_bag`
- Status: `candidate`

## Candidate URLs

- https://github.com/url-kaist/kaistviodataset

## Expected sensors

- stereo_camera
- imu

## Timing questions to investigate

- vehicle_camera_imu_sync
- bag_record_time_vs_header_stamp

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
