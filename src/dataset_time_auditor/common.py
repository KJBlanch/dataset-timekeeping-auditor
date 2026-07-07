from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def ns_to_s(value: Optional[int | float]) -> Optional[float]:
    if value is None:
        return None
    return float(value) / 1e9


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        x = float(value)
        if np.isnan(x) or np.isinf(x):
            return None
        return x
    except Exception:
        return None


def describe_numeric(values: Iterable[float]) -> Dict[str, Any]:
    arr = np.array([v for v in values if v is not None and np.isfinite(v)], dtype=float)
    if arr.size == 0:
        return {"count": 0}
    return {
        "count": int(arr.size),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "median": float(np.median(arr)),
        "p95": float(np.percentile(arr, 95)),
        "p99": float(np.percentile(arr, 99)),
    }


def monotonic_flags(values: List[float]) -> Dict[str, Any]:
    clean = [v for v in values if v is not None and np.isfinite(v)]
    if len(clean) < 2:
        return {"checked": False, "monotonic_non_decreasing": None, "negative_steps": 0, "duplicate_steps": 0}
    diffs = np.diff(np.array(clean, dtype=float))
    return {
        "checked": True,
        "monotonic_non_decreasing": bool(np.all(diffs >= 0)),
        "negative_steps": int(np.sum(diffs < 0)),
        "duplicate_steps": int(np.sum(diffs == 0)),
        "min_step_s": float(np.min(diffs)),
        "median_step_s": float(np.median(diffs)),
        "max_step_s": float(np.max(diffs)),
    }


def write_json(path: str | Path, data: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def base_result(dataset_id: str, audit_type: str, audit_level: str, source: str) -> Dict[str, Any]:
    return {
        "dataset_id": dataset_id,
        "audit_type": audit_type,
        "audit_level": audit_level,
        "generated_at_utc": now_utc(),
        "source": source,
        "summary": {},
        "topics": [],
        "documentation": {},
        "warnings": [],
        "errors": [],
    }


def get_nested(obj: Any, path: List[str]) -> Any:
    cur = obj
    for key in path:
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            cur = getattr(cur, key, None)
        if cur is None:
            return None
    return cur


def stamp_to_sec(stamp: Any) -> Optional[float]:
    """Best-effort extraction of ROS-like time stamps from objects/dicts.

    Supports dicts with sec/nsec, secs/nsecs, stamp.sec/stamp.nanosec and common
    Python ROS message object attributes.
    """
    if stamp is None:
        return None
    if isinstance(stamp, (int, float)):
        return safe_float(stamp)

    sec = None
    nsec = None
    for s_key, ns_key in [("sec", "nanosec"), ("sec", "nsec"), ("secs", "nsecs")]:
        if isinstance(stamp, dict):
            sec = stamp.get(s_key)
            nsec = stamp.get(ns_key)
        else:
            sec = getattr(stamp, s_key, None)
            nsec = getattr(stamp, ns_key, None)
        if sec is not None:
            break
    if sec is None:
        return None
    return float(sec) + float(nsec or 0) * 1e-9


def find_header_stamp(msg: Any) -> Optional[float]:
    header = None
    if isinstance(msg, dict):
        header = msg.get("header")
    else:
        header = getattr(msg, "header", None)
    if header is None:
        return None
    stamp = header.get("stamp") if isinstance(header, dict) else getattr(header, "stamp", None)
    return stamp_to_sec(stamp)
