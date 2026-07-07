from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def flatten_result(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    topics = data.get("topics", []) or []
    doc_score = (data.get("documentation") or {}).get("score", {})

    def count_topics(pred):
        return sum(1 for t in topics if isinstance(t, dict) and pred(t))

    row = {
        "dataset_id": data.get("dataset_id"),
        "audit_type": data.get("audit_type"),
        "audit_level": data.get("audit_level"),
        "source": data.get("source"),
        "topic_count": len(topics),
        "total_messages_sampled": data.get("summary", {}).get("total_messages_sampled"),
        "topics_with_header_stamp": data.get("summary", {}).get("topics_with_header_stamp"),
        "topics_with_sent_time": data.get("summary", {}).get("files_with_sent_time"),
        "topics_with_received_time": data.get("summary", {}).get("files_with_received_time"),
        "topics_with_sample_time_point": data.get("summary", {}).get("files_with_sample_time_point"),
        "docs_score": doc_score.get("total"),
        "docs_score_max": doc_score.get("max_total"),
        "warning_count": len(data.get("warnings", [])),
        "error_count": len(data.get("errors", [])),
        "json_path": str(path),
    }

    # Best-effort aggregate: mean of topic-level timing offsets where present.
    offsets = []
    for t in topics:
        if not isinstance(t, dict):
            continue
        for key in ["record_minus_header_s", "log_minus_header_s", "publish_minus_header_s", "received_minus_sample_s", "received_minus_sent_s"]:
            v = t.get(key)
            if isinstance(v, dict) and v.get("count", 0) > 0 and v.get("mean") is not None:
                offsets.append(float(v["mean"]))
    row["mean_available_offset_s"] = sum(offsets) / len(offsets) if offsets else None
    return row


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarize audit JSON files into paper-friendly tables.")
    ap.add_argument("json_files", nargs="+")
    ap.add_argument("--csv")
    ap.add_argument("--markdown")
    ap.add_argument("--latex")
    args = ap.parse_args()

    rows = []
    for pattern in args.json_files:
        paths = sorted(Path().glob(pattern)) if any(ch in pattern for ch in "*?[") else [Path(pattern)]
        for p in paths:
            if p.exists():
                rows.append(flatten_result(p))
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No audit rows found.")

    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.csv, index=False)
    if args.markdown:
        Path(args.markdown).parent.mkdir(parents=True, exist_ok=True)
        Path(args.markdown).write_text(df.to_markdown(index=False), encoding="utf-8")
    if args.latex:
        Path(args.latex).parent.mkdir(parents=True, exist_ok=True)
        Path(args.latex).write_text(df.to_latex(index=False, escape=True), encoding="utf-8")

    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
