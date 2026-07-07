# RoboCup 2023-2024 ROSbag Dataset

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `robocup_rosbag_2023_2024`
- Tier: `1`
- Domain: `service_robotics_hri_navigation`
- MASS relevance: `low`
- Expected format: `ros1_bag`
- Target audit level: `L1`
- Download policy: `one_bag_if_available`
- Status: `candidate`

## Candidate URLs

- https://pmc.ncbi.nlm.nih.gov/articles/PMC11615538/

## Expected sensors

- mobile_robot_sensors
- task_data

## Timing questions to investigate

- task_event_time_vs_sensor_time
- rosbag_record_time_vs_message_header_time

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
