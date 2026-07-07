#!/usr/bin/env python3
"""Generate tiny synthetic datasets for CI smoke testing.

The generated files are deliberately small and artificial. They are not meant to
validate scientific timing quality; they verify that the auditors can parse the
expected structures and flag basic timing conditions.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def generate_docs(root: Path) -> None:
    good = """
    Synthetic MASS harbour perception dataset.

    Sensors: stereo camera, marine radar, AIS receiver, lidar, IMU, and GNSS.
    Clock source: GNSS-disciplined PTP grandmaster with PPS distributed to the
    acquisition computer. The lidar and camera are hardware triggered. IMU data
    uses sensor acquisition timestamps. ROS header.stamp represents acquisition
    time. Bag record time represents logger receipt time and must not be used as
    sensor time. Known synchronization uncertainty is below 2 ms for cameras and
    below 1 ms for IMU. rosbag replay should use /clock only for reproducing the
    original acquisition timeline.
    """
    bad = """
    Synthetic undocumented maritime robot dataset.

    Data were recorded during a harbour run using cameras, lidar, GNSS, IMU,
    AIS, and radar. Files are provided for convenience. Timestamps are included
    in the logs. Synchronization details are not available.
    """
    write_text(root / "synthetic_mass_good_readme.txt", good)
    write_text(root / "synthetic_mass_undocumented_readme.txt", bad)


def write_opendlv_csv(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sent.seconds",
        "sent.microseconds",
        "received.seconds",
        "received.microseconds",
        "sample time point.seconds",
        "sample time point.microseconds",
        "data.value",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def generate_opendlv_exports(root: Path) -> None:
    # Good case: sample < sent < received, monotonic, fixed 5 ms logger delay.
    good_rows = []
    base_s = 1_780_000_000
    for i in range(20):
        sample_us = i * 20_000
        sent_us = sample_us + 1_000
        recv_us = sample_us + 5_000
        good_rows.append({
            "sample time point.seconds": base_s,
            "sample time point.microseconds": sample_us,
            "sent.seconds": base_s,
            "sent.microseconds": sent_us,
            "received.seconds": base_s,
            "received.microseconds": recv_us,
            "data.value": i,
        })
    write_opendlv_csv(root / "opendlv_good" / "opendlv.proxy.GroundSpeedReading-0.csv", good_rows)

    # Bad case: one non-monotonic sample stamp and variable receive delay.
    bad_rows = []
    delays = [5_000, 6_000, 7_000, 80_000, 4_000, 3_000, 10_000, 11_000, 12_000, 13_000]
    for i, delay in enumerate(delays):
        sample_us = i * 20_000
        if i == 5:
            sample_us = 60_000  # deliberate backwards jump relative to previous 80 ms sample.
        sent_us = sample_us + 1_000
        recv_us = sample_us + delay
        bad_rows.append({
            "sample time point.seconds": base_s,
            "sample time point.microseconds": sample_us,
            "sent.seconds": base_s,
            "sent.microseconds": sent_us,
            "received.seconds": base_s,
            "received.microseconds": recv_us,
            "data.value": i,
        })
    write_opendlv_csv(root / "opendlv_bad" / "opendlv.proxy.GeodeticWgs84Reading-0.csv", bad_rows)


def generate_mcap(root: Path) -> None:
    """Generate a tiny JSON-schema MCAP file if the optional mcap package exists."""
    try:
        from mcap.writer import Writer
    except Exception as exc:  # pragma: no cover - depends on optional install state.
        marker = {
            "created": False,
            "reason": f"mcap package unavailable: {exc}",
            "note": "Install project dependencies, then rerun this script to generate synthetic.mcap.",
        }
        (root / "synthetic_mcap_skipped.json").write_text(json.dumps(marker, indent=2), encoding="utf-8")
        return

    path = root / "synthetic_mass_log.mcap"
    root.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        writer = Writer(f)
        writer.start()
        schema_id = writer.register_schema(
            name="synthetic/HeaderedScalar",
            encoding="jsonschema",
            data=json.dumps({
                "type": "object",
                "properties": {
                    "header": {
                        "type": "object",
                        "properties": {
                            "stamp": {
                                "type": "object",
                                "properties": {
                                    "sec": {"type": "integer"},
                                    "nanosec": {"type": "integer"},
                                },
                            },
                            "frame_id": {"type": "string"},
                        },
                    },
                    "value": {"type": "number"},
                },
            }).encode("utf-8"),
        )
        channel_id = writer.register_channel(
            topic="/synthetic/imu_scalar",
            message_encoding="json",
            schema_id=schema_id,
        )
        base_ns = 1_780_000_000_000_000_000
        for i in range(20):
            acquisition_ns = base_ns + i * 10_000_000
            publish_ns = acquisition_ns + 1_000_000
            log_ns = acquisition_ns + 4_000_000
            msg = {
                "header": {
                    "stamp": {
                        "sec": acquisition_ns // 1_000_000_000,
                        "nanosec": acquisition_ns % 1_000_000_000,
                    },
                    "frame_id": "base_link",
                },
                "value": float(i),
            }
            writer.add_message(
                channel_id=channel_id,
                log_time=log_ns,
                publish_time=publish_ns,
                data=json.dumps(msg).encode("utf-8"),
            )
        writer.finish()


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate tiny synthetic timing smoke-test datasets.")
    ap.add_argument("--output-dir", default="smoke", help="Directory to write synthetic files into.")
    ap.add_argument("--no-mcap", action="store_true", help="Skip synthetic MCAP generation.")
    args = ap.parse_args()

    root = Path(args.output_dir)
    root.mkdir(parents=True, exist_ok=True)
    generate_docs(root / "docs")
    generate_opendlv_exports(root / "opendlv")
    if not args.no_mcap:
        generate_mcap(root / "mcap")

    manifest = {
        "description": "Tiny synthetic datasets for dataset-timekeeping-auditor smoke tests.",
        "files": sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()),
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Generated {len(manifest['files'])} smoke-test files under {root}")


if __name__ == "__main__":
    main()
