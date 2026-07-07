# Candidate datasets for the middleware timekeeping survey

This file defines the first practical polling set for the MASS-oriented dataset timekeeping survey. The goal is not to download every dataset. The goal is to run a low-cost, reproducible audit in three stages:

- **L0 documentation audit:** inspect README, paper, dataset page, and metadata for timing terms and claims.
- **L1 sample audit:** inspect one small bag/log/sample where available.
- **L2 representative sequence audit:** inspect a full sequence only when necessary.

The canonical machine-readable list is `candidate_datasets.yaml`.


## Bootstrapping documentation folders

If `candidate_docs/` is empty, the audit script now creates registry-note placeholders automatically. These files are useful for CI sanity checks, but they are explicitly marked as **not source documentation** and should not be cited as evidence in the paper.

```bash
bash ./scripts/audit_candidate_docs.sh
```

To try a lightweight web fetch of candidate pages without downloading raw datasets:

```bash
bash ./scripts/audit_candidate_docs.sh --fetch
```

To fetch what can be fetched and create registry-note placeholders for the rest:

```bash
bash ./scripts/audit_candidate_docs.sh --fetch --seed-missing
```

For a strict paper-evidence run, add real README/page/paper notes under `candidate_docs/<dataset_id>/` and run:

```bash
bash ./scripts/audit_candidate_docs.sh --no-auto-seed --fail-if-empty
```

## First L0 pass

Run documentation audits for every Tier 1 and Tier 2 candidate before downloading raw data. Store copied README/paper text or manually extracted timing notes under:

```text
candidate_docs/<dataset_id>/
```

Then run:

```bash
bash ./scripts/audit_candidate_docs.sh
```

The script writes one JSON per dataset under:

```text
results/candidate_docs/
```

and then generates:

```text
tables/candidate_docs_summary.csv
tables/candidate_docs_summary.md
tables/candidate_docs_summary.tex
```

## First L1 download shortlist

Prioritize these for one-sample downloads:

1. `ar_table` — tiny ROS 1 bag sanity check.
2. `tum_vi` — canonical VIO ROS bag with strong timing expectations.
3. `uzh_event_camera` — asynchronous event timestamps.
4. `viode` — simulated-time ROS bag.
5. `autoware_jkk_ouster_mcap` — ROS 2/MCAP plus lidar timing semantics.
6. `cartographer_deutsches_museum` — classic lidar/IMU mapping bag.
7. `koide_lidar_imu_mapping` — compact lidar/IMU case.
8. `mit_marine_perception_robowhaler` — direct maritime ASV / MASS anchor.
9. `autoferry_sensor_fusion` or `seepersea` — maritime tracking/perception, depending on available format.
10. `hilti_slam_2021` — complex multi-sensor ROS bag.

## Maritime / MASS emphasis

The MASS-facing argument should not rely only on automotive and indoor VIO datasets. At least three maritime or maritime-adjacent candidates should be audited at L0, and at least one should be audited at L1 if a manageable sample exists:

- `mit_marine_perception_robowhaler`
- `autoferry_sensor_fusion`
- `seepersea`
- `usvtrack`
- `mulran` as a radar-heavy non-maritime comparator

## Inclusion criteria

A dataset is a good candidate when at least one of these is true:

- It provides ROS 1 bags, ROS 2 bags, MCAP, OpenDLV `.rec`, LCM logs, CyberRT records, PCAP plus decoder, or a middleware replay/conversion tool.
- It provides enough metadata to distinguish sensor acquisition time from middleware/logging time.
- It contains a maritime, field-robotics, radar, lidar, GNSS/INS, or multi-agent perception timing problem relevant to MASS.
- It has a small sample or single sequence suitable for L1 inspection.

## Exclusion or defer criteria

Defer datasets that are image-only with no timestamps, have no public documentation, require full multi-terabyte downloads for basic metadata, or do not expose any middleware/logging semantics.
