# i.c.sens Visual-Inertial-LiDAR Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `icsens_visual_inertial_lidar`
- Tier: `3`
- Domain: `mobile_mapping`
- MASS relevance: `medium`
- Expected format: `ros1_bag`
- Target audit level: `L0`
- Download policy: `docs_first_due_to_10gb_bags`
- Status: `candidate`

## Candidate URLs

- https://data.uni-hannover.de/dataset/i-c-sens-visual-inertial-lidar-dataset

## Expected sensors

- camera
- lidar
- imu
- gnss_ins

## Timing questions to investigate

- gnss_ins_ground_truth_time_basis
- rosbag_record_time_vs_header_stamp

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
