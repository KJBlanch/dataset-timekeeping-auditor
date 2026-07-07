from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .common import base_result, describe_numeric, monotonic_flags, safe_float, write_json

TIME_COL_PATTERNS = {
    "sent": ["sent", "sent.seconds", "sent.microseconds", "senttime", "sent_time", "sent timestamp"],
    "received": ["received", "received.seconds", "received.microseconds", "recv", "received_time", "received timestamp"],
    "sample": ["sample", "sampletime", "sample_time", "sample time point", "sampletimepoint", "sample timestamp"],
}


def norm_col(c: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", c.strip().lower())


def candidate_cols(cols: List[str], key: str) -> List[str]:
    pats = [norm_col(x) for x in TIME_COL_PATTERNS[key]]
    out = []
    for c in cols:
        nc = norm_col(c)
        if any(p in nc for p in pats):
            out.append(c)
    return out


def combine_seconds_microseconds(df: pd.DataFrame, cols: List[str], prefix: str) -> Optional[pd.Series]:
    # Handles common cluon-rec2fuse-style splits, e.g. sent.seconds + sent.microseconds.
    lower = {norm_col(c): c for c in cols}
    sec_col = None
    usec_col = None
    for c in cols:
        n = norm_col(c)
        if prefix in n and "second" in n and "micro" not in n and "nano" not in n:
            sec_col = c
        if prefix in n and "micro" in n:
            usec_col = c
    if sec_col is not None:
        sec = pd.to_numeric(df[sec_col], errors="coerce")
        frac = 0
        if usec_col is not None:
            frac = pd.to_numeric(df[usec_col], errors="coerce") * 1e-6
        return sec + frac
    return None


def best_time_series(df: pd.DataFrame, kind: str) -> Optional[pd.Series]:
    cols = list(df.columns)
    combined = combine_seconds_microseconds(df, cols, kind)
    if combined is not None:
        return combined
    cands = candidate_cols(cols, kind)
    for c in cands:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() > 0:
            # Heuristic: if values look like micro/nanoseconds, convert to seconds.
            med = s.dropna().abs().median()
            if med > 1e15:
                return s / 1e9
            if med > 1e12:
                return s / 1e6
            return s
    return None


def audit_csv(path: Path) -> Dict[str, Any]:
    try:
        df = pd.read_csv(path, nrows=50000)
    except Exception as e:
        return {"file": str(path), "error": str(e)}

    sent = best_time_series(df, "sent")
    received = best_time_series(df, "received")
    sample = best_time_series(df, "sample")

    out: Dict[str, Any] = {
        "file": str(path),
        "rows_sampled": int(len(df)),
        "columns": list(df.columns),
        "has_sent_time": sent is not None,
        "has_received_time": received is not None,
        "has_sample_time_point": sample is not None,
    }

    if sent is not None:
        out["sent_time_monotonic"] = monotonic_flags(sent.dropna().astype(float).tolist())
    if received is not None:
        out["received_time_monotonic"] = monotonic_flags(received.dropna().astype(float).tolist())
    if sample is not None:
        out["sample_time_monotonic"] = monotonic_flags(sample.dropna().astype(float).tolist())
    if sent is not None and received is not None:
        out["received_minus_sent_s"] = describe_numeric((received - sent).dropna().astype(float).tolist())
    if sample is not None and received is not None:
        out["received_minus_sample_s"] = describe_numeric((received - sample).dropna().astype(float).tolist())
    if sample is not None and sent is not None:
        out["sent_minus_sample_s"] = describe_numeric((sent - sample).dropna().astype(float).tolist())
    return out


def audit_export(path: str, dataset: str) -> Dict[str, Any]:
    root = Path(path)
    result = base_result(dataset, "opendlv_rec_export", "L1", str(root))
    csvs = sorted(root.rglob("*.csv")) if root.is_dir() else [root]
    if not csvs:
        result["errors"].append("No CSV files found. Export or mount the .rec with cluon-rec2fuse first, then point this auditor to the mounted/exported directory.")
        return result

    topics = []
    for csv in csvs:
        topics.append(audit_csv(csv))
    result["topics"] = topics
    result["summary"] = {
        "csv_file_count": len(csvs),
        "files_with_sent_time": sum(1 for t in topics if t.get("has_sent_time")),
        "files_with_received_time": sum(1 for t in topics if t.get("has_received_time")),
        "files_with_sample_time_point": sum(1 for t in topics if t.get("has_sample_time_point")),
        "note": "OpenDLV .rec binary decoding is delegated to cluon-rec2fuse or equivalent tooling. This audit inspects the exported CSV structure.",
    }
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit cluon-rec2fuse CSV exports from OpenDLV/libcluon .rec recordings.")
    ap.add_argument("path", help="Directory of CSV files exported/mounted from .rec, or a single CSV file.")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    write_json(args.output, audit_export(args.path, args.dataset))


if __name__ == "__main__":
    main()
