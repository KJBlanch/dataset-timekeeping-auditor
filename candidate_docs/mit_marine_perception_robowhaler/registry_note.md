# MIT Sea Grant Marine Perception / RoboWhaler

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `mit_marine_perception_robowhaler`
- Tier: `1`
- Domain: `maritime_asv_perception`
- MASS relevance: `high`
- Expected format: `ros1_bag_or_extracted_timestamped_files`
- Target audit level: `L1`
- Download policy: `one_smallest_rosbag_or_timestamp_csv`
- Status: `candidate`

## Candidate URLs

- https://repository.library.noaa.gov/view/noaa/41894/noaa_41894_DS1.pdf

## Expected sensors

- rtk_ins
- lidar
- marine_radar
- visible_camera
- thermal_camera

## Timing questions to investigate

- radar_camera_lidar_ins_time_basis
- rosbag_timestamp_extraction_semantics
- gnss_or_ins_clock_discipline
- maritime_sensor_latency_documentation

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
