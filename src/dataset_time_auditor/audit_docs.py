from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

from .common import base_result, write_json

KEYWORDS = {
    "clock_source": ["gnss time", "gps time", "utc", "ptp", "pps", "ntp", "chrony", "grandmaster", "hardware clock", "host clock", "system clock", "sim time", "simulation time"],
    "sync_method": ["synchroni", "sync", "hardware trigger", "trigger", "genlock", "ptp", "pps", "ntp", "software sync", "post-hoc", "post hoc", "aligned", "calibrated"],
    "timestamp_fields": ["timestamp", "time stamp", "header.stamp", "stamp", "bag time", "record time", "publish time", "log_time", "publish_time", "sample time", "received", "sent"],
    "latency_jitter": ["latency", "delay", "offset", "jitter", "drift", "skew", "time offset"],
    "camera_timing": ["exposure", "rolling shutter", "global shutter", "frame start", "frame end", "mid-exposure", "mid exposure"],
    "middleware": ["rosbag", "ros bag", "ros 1", "ros2", "ros 2", "mcap", "lcm", "cyberrt", "apollo", "opendlv", "libcluon", ".rec", "dds"],
    "replay": ["replay", "playback", "rosbag play", "/clock", "use_sim_time", "simulated clock"],
}

SCORING_HINTS = {
    "clock_source_documented": ("clock_source", 2),
    "synchronization_documented": ("sync_method", 2),
    "timestamp_semantics_documented": ("timestamp_fields", 2),
    "latency_or_offset_documented": ("latency_jitter", 2),
    "middleware_semantics_documented": ("middleware", 2),
    "replay_semantics_documented": ("replay", 2),
}


def snippets(text: str, needle: str, radius: int = 120, limit: int = 5) -> List[str]:
    out = []
    lower = text.lower()
    for m in re.finditer(re.escape(needle.lower()), lower):
        start = max(0, m.start() - radius)
        end = min(len(text), m.end() + radius)
        out.append(" ".join(text[start:end].split()))
        if len(out) >= limit:
            break
    return out


def audit_text(text: str) -> Dict:
    lower = text.lower()
    categories = {}
    for category, words in KEYWORDS.items():
        hits = []
        hit_snippets = []
        for w in words:
            if w in lower:
                hits.append(w)
                hit_snippets.extend(snippets(text, w, limit=2))
        categories[category] = {
            "hit_count": len(hits),
            "hits": sorted(set(hits)),
            "snippets": hit_snippets[:8],
        }

    score = {}
    total = 0
    max_total = 0
    for name, (category, max_score) in SCORING_HINTS.items():
        max_total += max_score
        hit_count = categories[category]["hit_count"]
        value = 0 if hit_count == 0 else (1 if hit_count < 3 else 2)
        score[name] = value
        total += value
    score["total"] = total
    score["max_total"] = max_total
    return {"categories": categories, "score": score}


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit dataset documentation for timekeeping-relevant terms.")
    ap.add_argument("path", help="Text/Markdown file, or a directory containing text-like docs.")
    ap.add_argument("--dataset", required=True, help="Dataset identifier.")
    ap.add_argument("--output", required=True, help="Output JSON path.")
    args = ap.parse_args()

    p = Path(args.path)
    files = []
    if p.is_dir():
        for ext in ("*.md", "*.txt", "*.rst", "*.yaml", "*.yml"):
            files.extend(p.rglob(ext))
    else:
        files = [p]

    text_parts = []
    warnings = []
    for f in files:
        try:
            text_parts.append(f"\n\n--- FILE: {f} ---\n" + f.read_text(encoding="utf-8", errors="ignore"))
        except Exception as e:
            warnings.append(f"Could not read {f}: {e}")

    result = base_result(args.dataset, "docs", "L0", str(p))
    result["documentation"] = audit_text("\n".join(text_parts))
    result["summary"] = result["documentation"].get("score", {})
    result["warnings"].extend(warnings)
    write_json(args.output, result)


if __name__ == "__main__":
    main()
