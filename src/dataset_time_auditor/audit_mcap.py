from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Any, Dict, List, Optional

from .common import base_result, describe_numeric, monotonic_flags, ns_to_s, write_json


def _try_decode_ros1(reader, schema, message):
    try:
        from mcap_ros1.decoder import DecoderFactory
        decoder = DecoderFactory().decoder_for(schema)
        return decoder(message.data)
    except Exception:
        return None


def _try_decode_ros2(reader, schema, message):
    try:
        from mcap_ros2.decoder import DecoderFactory
        decoder = DecoderFactory().decoder_for(schema)
        return decoder(message.data)
    except Exception:
        return None


def _stamp_from_ros_msg(obj: Any) -> Optional[float]:
    try:
        header = getattr(obj, "header", None)
        if header is None:
            return None
        stamp = getattr(header, "stamp", None)
        if stamp is None:
            return None
        sec = getattr(stamp, "sec", None)
        nsec = getattr(stamp, "nanosec", None)
        if sec is None:
            sec = getattr(stamp, "secs", None)
            nsec = getattr(stamp, "nsecs", None)
        if sec is None:
            return None
        return float(sec) + float(nsec or 0) * 1e-9
    except Exception:
        return None


def audit_mcap(path: str, dataset: str, max_messages: int) -> Dict[str, Any]:
    from mcap.reader import make_reader

    result = base_result(dataset, "mcap", "L2", path)
    stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "message_count": 0,
        "schema_names": set(),
        "log_times_s": [],
        "publish_times_s": [],
        "header_times_s": [],
        "log_minus_publish_s": [],
        "log_minus_header_s": [],
        "publish_minus_header_s": [],
        "has_header_stamp_count": 0,
        "decode_errors": 0,
    })

    with open(path, "rb") as f:
        reader = make_reader(f)
        for schema, channel, message in reader.iter_messages():
            topic = channel.topic
            s = stats[topic]
            if s["message_count"] >= max_messages:
                continue
            s["message_count"] += 1
            if schema and schema.name:
                s["schema_names"].add(schema.name)
            log_s = ns_to_s(message.log_time)
            pub_s = ns_to_s(message.publish_time)
            s["log_times_s"].append(log_s)
            s["publish_times_s"].append(pub_s)
            if log_s is not None and pub_s is not None:
                s["log_minus_publish_s"].append(log_s - pub_s)

            decoded = None
            if schema and schema.encoding in {"ros1msg", "ros2msg"}:
                decoded = _try_decode_ros1(reader, schema, message) if schema.encoding == "ros1msg" else _try_decode_ros2(reader, schema, message)
            elif channel.message_encoding in {"json", "application/json"}:
                try:
                    decoded = json.loads(message.data.decode("utf-8"))
                except Exception:
                    decoded = None
            header_s = _stamp_from_ros_msg(decoded) if decoded is not None else None
            if header_s is None and decoded is not None:
                # Some decoder outputs are dict-like.
                try:
                    header = decoded.get("header")
                    stamp = header.get("stamp") if header else None
                    if stamp:
                        sec = stamp.get("sec", stamp.get("secs"))
                        nsec = stamp.get("nanosec", stamp.get("nsec", stamp.get("nsecs", 0)))
                        header_s = float(sec) + float(nsec or 0) * 1e-9
                except Exception:
                    pass
            if decoded is None:
                s["decode_errors"] += 1
            if header_s is not None:
                s["has_header_stamp_count"] += 1
                s["header_times_s"].append(header_s)
                if log_s is not None:
                    s["log_minus_header_s"].append(log_s - header_s)
                if pub_s is not None:
                    s["publish_minus_header_s"].append(pub_s - header_s)

    topics = []
    for topic, s in sorted(stats.items()):
        topics.append({
            "topic": topic,
            "message_count_sampled": s["message_count"],
            "schema_names": sorted(s["schema_names"]),
            "has_log_time": len([x for x in s["log_times_s"] if x is not None]) > 0,
            "has_publish_time": len([x for x in s["publish_times_s"] if x is not None]) > 0,
            "has_header_stamp_count": s["has_header_stamp_count"],
            "header_stamp_coverage": s["has_header_stamp_count"] / max(1, s["message_count"]),
            "log_time_monotonic": monotonic_flags(s["log_times_s"]),
            "publish_time_monotonic": monotonic_flags(s["publish_times_s"]),
            "header_time_monotonic": monotonic_flags(s["header_times_s"]),
            "log_minus_publish_s": describe_numeric(s["log_minus_publish_s"]),
            "log_minus_header_s": describe_numeric(s["log_minus_header_s"]),
            "publish_minus_header_s": describe_numeric(s["publish_minus_header_s"]),
            "decode_errors_sampled": s["decode_errors"],
        })
    result["topics"] = topics
    result["summary"] = {
        "topic_count": len(topics),
        "topics_with_header_stamp": sum(1 for t in topics if t["has_header_stamp_count"] > 0),
        "total_messages_sampled": sum(t["message_count_sampled"] for t in topics),
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit MCAP timing semantics.")
    ap.add_argument("path")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--max-messages-per-topic", type=int, default=10000)
    args = ap.parse_args()
    write_json(args.output, audit_mcap(args.path, args.dataset, args.max_messages_per_topic))


if __name__ == "__main__":
    main()
