# VIODE

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `viode`
- Tier: `1`
- Domain: `simulated_visual_inertial`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_sequence`
- Status: `candidate`

## Candidate URLs

- https://github.com/kminoda/VIODE

## Expected sensors

- stereo_camera
- imu
- odometry

## Timing questions to investigate

- simulated_time_vs_bag_record_time
- ros_clock_or_use_sim_time_semantics

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
