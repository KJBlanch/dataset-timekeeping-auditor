# Autoware / JKK Ouster MCAP Sample

> REGISTRY NOTE ONLY — NOT SOURCE DOCUMENTATION.
>
> This file was generated from `candidate_datasets.yaml` so the CI documentation-audit
> pipeline has something to process before source documentation has been added. Do not
> cite this file as evidence in the survey. Replace or supplement it with README text,
> dataset-page text, paper notes, or downloaded metadata from the source URLs below.

## Candidate metadata

- Dataset id: `autoware_jkk_ouster_mcap`
- Tier: `1`
- Domain: `autonomous_vehicle_lidar`
- MASS relevance: `medium`
- Expected format: `ros2_mcap_or_ros2_bag_plus_pcap`
- Target audit level: `L1`
- Download policy: `one_mcap_or_pcap_sample`
- Status: `candidate`

## Candidate URLs

- https://jkk-research.github.io/dataset/jkk_dataset_02/
- https://autowarefoundation.github.io/autoware-documentation/main/datasets/

## Expected sensors

- lidar

## Timing questions to investigate

- mcap_log_time_vs_publish_time_vs_header_stamp
- pcap_packet_time_vs_decoded_lidar_time

## Source-documentation TODO

Add one or more of the following files in this folder:

- `README.md` copied from the dataset repository or archive page.
- `dataset_page.txt` containing relevant text from the public dataset page.
- `paper_notes.txt` with manually extracted timing/synchronization statements from the dataset paper.
- `metadata_notes.txt` describing available bags/logs, timestamp fields, and sample download size.
