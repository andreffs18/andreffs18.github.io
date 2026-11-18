#!/usr/bin/env bash
# Download the Feedly OPML export (needs FEEDLY_TOKEN) to the file given as $1.
set -euo pipefail

: "${FEEDLY_TOKEN:?FEEDLY_TOKEN is not set}"
out="${1:?usage: feedly_opml.sh <output file>}"

# --retry only covers transient failures (timeouts, 429, 5xx); a 401 (expired token) fails straight away.
# With --fail-with-body the error response lands in the -o file, so print it on failure.
if ! curl -sS --fail-with-body --retry 3 --max-time 30 \
  -H "Authorization: Bearer $FEEDLY_TOKEN" \
  -o "$out" \
  https://cloud.feedly.com/v3/opml; then
  echo "::error::Feedly request failed. Response:" >&2
  cat "$out" >&2
  echo >&2
  exit 1
fi
