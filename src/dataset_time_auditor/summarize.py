from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd


def flatten_result(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    topics = data.get("topics", []) or []
    doc_score = (data.get("documentation") or {}).get("score", {})

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

    offsets = []
    for t in topics:
        if not isinstance(t, dict):
            continue
        for key in [
            "record_minus_header_s",
            "log_minus_header_s",
            "publish_minus_header_s",
            "received_minus_sample_s",
            "received_minus_sent_s",
        ]:
            v = t.get(key)
            if isinstance(v, dict) and v.get("count", 0) > 0 and v.get("mean") is not None:
                offsets.append(float(v["mean"]))
    row["mean_available_offset_s"] = sum(offsets) / len(offsets) if offsets else None
    return row


def _cell(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value)


def _markdown_escape(value: Any) -> str:
    return _cell(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def dataframe_to_markdown_no_optional_deps(df: pd.DataFrame) -> str:
    """Render a GitHub-flavored Markdown table without pandas' tabulate dependency."""
    columns = [str(c) for c in df.columns]
    lines = []
    lines.append("| " + " | ".join(_markdown_escape(c) for c in columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(_markdown_escape(row[c]) for c in df.columns) + " |")
    return "\n".join(lines) + "\n"


_LATEX_REPL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _latex_escape(value: Any) -> str:
    text = _cell(value).replace("\n", " ")
    return "".join(_LATEX_REPL.get(ch, ch) for ch in text)


def dataframe_to_latex_no_optional_deps(df: pd.DataFrame) -> str:
    """Render a simple tabular without pandas' jinja2 dependency."""
    columns = list(df.columns)
    alignment = "l" * len(columns)
    lines = [rf"\begin{{tabular}}{{{alignment}}}", r"\toprule"]
    lines.append(" & ".join(_latex_escape(c) for c in columns) + r" \\")
    lines.append(r"\midrule")
    for _, row in df.iterrows():
        lines.append(" & ".join(_latex_escape(row[c]) for c in columns) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Summarize audit JSON files into paper-friendly tables.")
    ap.add_argument("json_files", nargs="+")
    ap.add_argument("--csv")
    ap.add_argument("--markdown")
    ap.add_argument("--latex")
    args = ap.parse_args()

    rows: List[Dict[str, Any]] = []
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
        Path(args.markdown).write_text(dataframe_to_markdown_no_optional_deps(df), encoding="utf-8")
    if args.latex:
        Path(args.latex).parent.mkdir(parents=True, exist_ok=True)
        Path(args.latex).write_text(dataframe_to_latex_no_optional_deps(df), encoding="utf-8")

    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
