from __future__ import annotations

import argparse
from collections import defaultdict
from typing import Any, Dict

from .common import base_result, describe_numeric, monotonic_flags, write_json


def _ros_time_to_sec(t: Any) -> float:
    if hasattr(t, "to_sec"):
        return float(t.to_sec())
    return float(getattr(t, "secs", 0)) + float(getattr(t, "nsecs", 0)) * 1e-9


def _header_stamp(msg: Any):
    header = getattr(msg, "header", None)
    if header is None:
        return None
    stamp = getattr(header, "stamp", None)
    if stamp is None:
        return None
    return _ros_time_to_sec(stamp)


def audit_ros1(path: str, dataset: str, max_messages: int) -> Dict[str, Any]:
    try:
        import rosbag  # type: ignore
    except Exception as e:
        result = base_result(dataset, "ros1_bag", "L2", path)
        result["errors"].append(f"Could not import rosbag. Run inside a ROS 1 environment or use the Docker/host that has rosbag installed: {e}")
        return result

    result = base_result(dataset, "ros1_bag", "L2", path)
    stats = defaultdict(lambda: {
        "message_count": 0,
        "types": set(),
        "record_times_s": [],
        "header_times_s": [],
        "record_minus_header_s": [],
        "has_header_stamp_count": 0,
        "zero_nsec_count": 0,
    })

    with rosbag.Bag(path, "r") as bag:
        info = bag.get_type_and_topic_info()
        result["summary"]["bag_start_s"] = bag.get_start_time()
        result["summary"]["bag_end_s"] = bag.get_end_time()
        result["summary"]["bag_duration_s"] = bag.get_end_time() - bag.get_start_time()
        for topic, msg, t in bag.read_messages():
            s = stats[topic]
            if s["message_count"] >= max_messages:
                continue
            s["message_count"] += 1
            s["record_times_s"].append(_ros_time_to_sec(t))
            if topic in info.topics:
                s["types"].add(info.topics[topic].msg_type)
            hs = _header_stamp(msg)
            if hs is not None:
                s["has_header_stamp_count"] += 1
                s["header_times_s"].append(hs)
                s["record_minus_header_s"].append(_ros_time_to_sec(t) - hs)
                stamp = getattr(getattr(msg, "header", None), "stamp", None)
                if stamp is not None and getattr(stamp, "nsecs", None) == 0:
                    s["zero_nsec_count"] += 1

    result["topics"] = []
    for topic, s in sorted(stats.items()):
        result["topics"].append({
            "topic": topic,
            "message_count_sampled": s["message_count"],
            "message_types": sorted(s["types"]),
            "has_header_stamp_count": s["has_header_stamp_count"],
            "header_stamp_coverage": s["has_header_stamp_count"] / max(1, s["message_count"]),
            "zero_nsec_count": s["zero_nsec_count"],
            "record_time_monotonic": monotonic_flags(s["record_times_s"]),
            "header_time_monotonic": monotonic_flags(s["header_times_s"]),
            "record_minus_header_s": describe_numeric(s["record_minus_header_s"]),
        })
    result["summary"].update({
        "topic_count": len(result["topics"]),
        "topics_with_header_stamp": sum(1 for t in result["topics"] if t["has_header_stamp_count"] > 0),
        "total_messages_sampled": sum(t["message_count_sampled"] for t in result["topics"]),
    })
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit ROS 1 bag timing semantics.")
    ap.add_argument("path")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-messages-per-topic", type=int, default=10000)
    args = ap.parse_args()
    write_json(args.output, audit_ros1(args.path, args.dataset, args.max_messages_per_topic))


if __name__ == "__main__":
    main()
