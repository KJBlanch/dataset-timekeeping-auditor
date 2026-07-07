from __future__ import annotations

import argparse
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

from .common import base_result, describe_numeric, monotonic_flags, ns_to_s, write_json


def audit_ros2(path: str, dataset: str, max_messages: int) -> Dict[str, Any]:
    p = Path(path)
    result = base_result(dataset, "ros2_bag", "L1", str(p))
    dbs = [p] if p.suffix == ".db3" else sorted(p.glob("*.db3"))
    if not dbs:
        result["errors"].append("No ROS 2 sqlite .db3 files found. Pass a .db3 file or bag directory.")
        return result

    stats = defaultdict(lambda: {
        "message_count": 0,
        "storage_times_s": [],
        "types": set(),
        "serialization_format": set(),
    })

    for db in dbs:
        con = sqlite3.connect(db)
        cur = con.cursor()
        topic_rows = cur.execute("SELECT id, name, type, serialization_format FROM topics").fetchall()
        topic_by_id = {row[0]: row[1:] for row in topic_rows}
        for topic_id, timestamp_ns, data in cur.execute("SELECT topic_id, timestamp, data FROM messages ORDER BY timestamp"):
            name, typ, ser = topic_by_id[topic_id]
            s = stats[name]
            if s["message_count"] >= max_messages:
                continue
            s["message_count"] += 1
            s["storage_times_s"].append(ns_to_s(timestamp_ns))
            s["types"].add(typ)
            s["serialization_format"].add(ser)
        con.close()

    result["topics"] = []
    for topic, s in sorted(stats.items()):
        result["topics"].append({
            "topic": topic,
            "message_count_sampled": s["message_count"],
            "message_types": sorted(s["types"]),
            "serialization_format": sorted(s["serialization_format"]),
            "has_storage_timestamp": True,
            "has_header_stamp_count": None,
            "note": "This SQLite-only audit reports ROS 2 storage timestamps. Use MCAP or a ROS 2 runtime deserializer to compare embedded header.stamp.",
            "storage_time_monotonic": monotonic_flags(s["storage_times_s"]),
            "storage_time_step_s": describe_numeric([b - a for a, b in zip(s["storage_times_s"], s["storage_times_s"][1:]) if a is not None and b is not None]),
        })

    result["summary"] = {
        "db_files": [str(x) for x in dbs],
        "topic_count": len(result["topics"]),
        "total_messages_sampled": sum(t["message_count_sampled"] for t in result["topics"]),
        "limitation": "Embedded header.stamp is not decoded by this lightweight SQLite auditor.",
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Lightweight ROS 2 SQLite bag timing audit.")
    ap.add_argument("path")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-messages-per-topic", type=int, default=10000)
    args = ap.parse_args()
    write_json(args.output, audit_ros2(args.path, args.dataset, args.max_messages_per_topic))


if __name__ == "__main__":
    main()
