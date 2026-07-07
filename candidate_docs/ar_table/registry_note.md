# AR Table Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `ar_table`
- Tier: `1`
- Domain: `indoor_visual_inertial_rgbd`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_small_bag`
- Status: `candidate`

## Candidate URLs

- https://github.com/rpng/ar_table_dataset

## Expected sensors

- rgbd_camera
- imu

## Timing questions to investigate

- real_sense_header_stamp_vs_bag_record_time
- imu_camera_timestamp_alignment
- whether_clock_source_is_documented

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
