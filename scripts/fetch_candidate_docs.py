#!/usr/bin/env python3
"""Best-effort lightweight fetch of candidate documentation pages.

This intentionally avoids raw dataset downloads. It fetches candidate URLs as text/HTML,
strips crude HTML markup, and stores the result under candidate_docs/<dataset_id>/.
PDF and binary URLs are not parsed; a URL note is written instead.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

import yaml

TEXT_CT = ("text/", "application/json", "application/yaml", "application/x-yaml", "application/xml")
BINARY_HINTS = (".zip", ".bag", ".mcap", ".pcap", ".tar", ".gz", ".7z", ".rar", ".h5", ".hdf5")


def safe_name(url: str, index: int) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_")
    return f"source_{index:02d}_{s[:80]}.txt"


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?is)<(br|p|div|li|tr|h[1-6])\b[^>]*>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html.unescape(text)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def fetch_url(url: str, timeout: int, max_bytes: int) -> tuple[str | None, str]:
    lower = url.lower()
    if any(h in lower for h in BINARY_HINTS):
        return None, "skipped_binary_url_hint"
    req = Request(url, headers={"User-Agent": "dataset-timekeeping-auditor/0.1 (+docs audit)"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get("content-type", "").lower()
            data = resp.read(max_bytes + 1)
    except (HTTPError, URLError, TimeoutError) as e:
        return None, f"fetch_failed: {e}"

    if len(data) > max_bytes:
        data = data[:max_bytes]
        trunc = "\n\n[TRUNCATED: lightweight documentation fetch byte limit reached]\n"
    else:
        trunc = ""

    if "application/pdf" in ct or lower.endswith(".pdf"):
        return None, "skipped_pdf_no_text_extraction"
    if ct and not any(ct.startswith(prefix) or prefix in ct for prefix in TEXT_CT) and "html" not in ct:
        return None, f"skipped_non_text_content_type: {ct}"

    text = data.decode("utf-8", errors="ignore")
    if "html" in ct or "<html" in text[:500].lower():
        text = strip_html(text)
    return text + trunc, "ok"


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch lightweight source documentation pages for candidate datasets")
    ap.add_argument("--registry", default="candidate_datasets.yaml")
    ap.add_argument("--out-dir", default="candidate_docs")
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--max-bytes", type=int, default=800_000)
    ap.add_argument("--limit", type=int, default=0, help="Optional max number of candidates to fetch; 0 means all")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    registry = yaml.safe_load(Path(args.registry).read_text(encoding="utf-8"))
    candidates = registry.get("candidates", [])
    if args.limit:
        candidates = candidates[: args.limit]

    out_root = Path(args.out_dir)
    ok = failed = skipped = 0
    for cand in candidates:
        dataset_id = cand["id"]
        doc_dir = out_root / dataset_id
        doc_dir.mkdir(parents=True, exist_ok=True)
        log_lines = []
        for i, url in enumerate(cand.get("candidate_urls") or [], start=1):
            out_path = doc_dir / safe_name(url, i)
            if out_path.exists() and not args.overwrite:
                skipped += 1
                log_lines.append(f"{url} -> skipped_existing {out_path.name}")
                continue
            text, status = fetch_url(url, args.timeout, args.max_bytes)
            if text is None:
                failed += 1
                log_lines.append(f"{url} -> {status}")
                continue
            header = (
                f"# Lightweight fetched documentation\n\n"
                f"- Dataset id: `{dataset_id}`\n"
                f"- Dataset name: `{cand.get('name', dataset_id)}`\n"
                f"- Source URL: {url}\n"
                f"- Fetch status: {status}\n\n"
                f"---\n\n"
            )
            out_path.write_text(header + text, encoding="utf-8")
            ok += 1
            log_lines.append(f"{url} -> ok {out_path.name}")
        (doc_dir / "fetch_log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"Lightweight docs fetch complete: ok={ok}, skipped={skipped}, failed_or_unparsed={failed}")
    if failed:
        print("Some URLs failed or were skipped. This is acceptable for PDFs/binary pages; add manual notes as needed.", file=sys.stderr)


if __name__ == "__main__":
    main()
