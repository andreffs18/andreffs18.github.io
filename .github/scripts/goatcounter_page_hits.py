#!/usr/bin/env python3
"""Fetch page view counts from GoatCounter and write data/goatcounter_page_hits.json."""

import json
import os
import random
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GOATCOUNTER_API = "https://andreffs18.goatcounter.com/api/v0/stats/hits"
OUTPUT_FILE = Path(__file__).parent.parent.parent / "data" / "goatcounter_page_hits.json"

# The API only returns a recent window unless `start` is given; this predates the site, so counts are all-time.
START = "2020-01-01T00:00:00Z"

TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 4
RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_BACKOFF_SECONDS = 30


class ApiError(Exception):
    """A GoatCounter request failed for good (not retried, or retries exhausted)."""


def request_json(url, token, sleep=time.sleep):
    """GET `url` and return the decoded JSON, retrying only transient failures.

    Retries 429, 5xx and network errors with exponential backoff and jitter,
    honoring Retry-After. Any other 4xx (including 404) fails immediately.
    The token is never included in error messages.
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        req = Request(url, headers={"Authorization": f"Bearer {token}"})
        retry_after = None
        try:
            with urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                return json.loads(response.read())
        except HTTPError as e:
            reason = f"HTTP {e.code} {e.reason}"
            body = e.read().decode("utf-8", errors="replace")[:500]
            if e.code not in RETRY_STATUSES or attempt == MAX_ATTEMPTS:
                raise ApiError(f"{reason} for {url}\n{body}") from e
            header = e.headers.get("Retry-After", "")
            retry_after = int(header) if header.isdigit() else None
        except (URLError, TimeoutError) as e:
            reason = f"network error: {e}"
            if attempt == MAX_ATTEMPTS:
                raise ApiError(f"{reason} for {url}") from e

        delay = retry_after
        if delay is None:
            delay = min(2**attempt, MAX_BACKOFF_SECONDS) + random.random()
        print(f"{reason} for {url} (attempt {attempt}/{MAX_ATTEMPTS}), retrying in {delay:.1f}s", file=sys.stderr)
        sleep(delay)


def fetch_hits(token, sleep=time.sleep):
    """Return {path: total hits since START}. Pages by excluding already-seen path IDs (the API has no cursor)."""
    hits = []
    seen_ids = []

    while True:
        params = {"limit": 200, "start": START}
        if seen_ids:
            params["exclude_paths"] = ",".join(str(i) for i in seen_ids)
        data = request_json(f"{GOATCOUNTER_API}?{urlencode(params)}", token, sleep)

        page = data.get("hits", [])
        hits.extend(page)
        seen_ids.extend(h["path_id"] for h in page)
        if not data.get("more") or not page:
            break

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

    # Fetch fully before touching OUTPUT_FILE, so a failed run never overwrites good data.
    try:
        hits = fetch_hits(token)
    except ApiError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
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
