# UZH FPV Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `uzh_fpv`
- Tier: `1`
- Domain: `aggressive_visual_inertial_event_camera`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_short_sequence`
- Status: `candidate`

## Candidate URLs

- https://fpv.ifi.uzh.ch/datasets/

## Expected sensors

- event_camera
- frame_camera
- imu
- ground_truth

## Timing questions to investigate

- high_rate_imu_and_event_timestamp_semantics
- ground_truth_alignment

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
