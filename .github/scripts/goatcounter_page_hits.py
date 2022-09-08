#!/usr/bin/env python3
"""Fetch page view counts from GoatCounter and write data/goatcounter_page_hits.json."""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GOATCOUNTER_API = "https://andreffs18.goatcounter.com/api/v0/stats/hits"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "goatcounter_page_hits.json"


def fetch_hits(token):
    hits = []
    params = {"limit": 200}

    while True:
        url = f"{GOATCOUNTER_API}?{urlencode(params)}"
        req = Request(url, headers={"Authorization": f"Bearer {token}"})
        with urlopen(req) as response:
            data = json.loads(response.read())
        hits.extend(data.get("hits", []))
        if not data.get("more"):
            break
        params["after"] = hits[-1]["path"]

    return {h["path"]: h["count"] for h in hits}


def merge_with_baseline(hits):
    """
    TODO: remove once GoatCounter has accumulated enough real data.
    These are pre-GoatCounter counts (from GA4) used as a floor
    """

    BASELINE_HITS = {
        "/blog/n8n-customizations-for-production/": 51,
        "/blog/setup-n8n-on-kubernetes/": 39,
        "/blog/i-really-like-emojis/": 23,
        "/blog/observability-on-n8n/": 5,
        "/blog/just-keep-on-save-for-later/": 3,
        "/blog/debug-in-hugo/": 1
    }

    all_paths = set(hits) | set(BASELINE_HITS)
    merged = {}
    for path in all_paths:
        before = hits.get(path, 0)
        after = max(before, BASELINE_HITS.get(path, 0))
        merged[path] = (before, after)
    return merged


def main():
    token = os.environ.get("GOATCOUNTER_TOKEN")
    if not token:
        print("Error: GOATCOUNTER_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    hits = fetch_hits(token)
    merged = merge_with_baseline(hits)

    # Sort so that it looks better when printing
    sorted_hits = dict(sorted(merged.items(), key=lambda x: x[1][1], reverse=True))

    print(f"{'Path':<55} {'Before':>7}  {'After':>7}")
    print("-" * 73)
    for path, (before, after) in sorted_hits.items():
        print(f"  {path:<53} {before:>7}  {after:>7}")

    output = {path: after for path, (_, after) in sorted_hits.items()}
    OUTPUT_FILE.write_text(json.dumps(output, indent=4) + "\n")
    print(f"\nWritten {len(output)} entries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
