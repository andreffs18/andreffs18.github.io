# Workflows

## `deploy.yml`

Builds the Hugo site and publishes it to GitHub Pages on every push to `master`.

### Why there is a "Setup Dart Sass" step

`layouts/partials/head.html` compiles `assets/css/main.scss` with Dart Sass (`transpiler: dartsass`). The older libsass transpiler is deprecated in Hugo and will be removed in a future release.

Hugo does not bundle Dart Sass. It runs a `sass` executable found on the `PATH` and talks to it over the embedded protocol, so the workflow installs it before the build:

```yaml
- name: Setup Dart Sass
  run: npm install -g sass-embedded@1.107.1
```

## `goatcounter_page_hits.yml`

Runs weekly (Monday 06:00 UTC, or on demand with `workflow_dispatch`). It runs `.github/scripts/goatcounter_page_hits.py`, which fetches page view counts from the GoatCounter API and writes `data/goatcounter_page_hits.json` (the "Blogpost view stats"). If the file changed, the workflow commits and pushes it.

It needs a `GOATCOUNTER_TOKEN` repository secret: a GoatCounter API token with read access to statistics.

### How the script behaves

- **All-time totals:** every request sends `start=2020-01-01T00:00:00Z`. Without `start` the API only returns a recent window (in a check on 2026-11-06: 103 views over 29 paths, versus 308 over 49 with it).
- **Pagination:** `GET /api/v0/stats/hits` has no cursor. The script pages by passing the path IDs it has already seen in `exclude_paths`. (`after` is not a GoatCounter parameter and returns a 400.)
- **Retries:** 429, 5xx and network errors are retried (4 attempts, exponential backoff with jitter, `Retry-After` honored). Any other 4xx, including 404, fails immediately.
- **Failures are readable:** the run prints the HTTP status, the URL and the start of the response body, never the token.
- **No bad writes:** the data file is only written after every page has been fetched, so a failed run leaves the previous data untouched.
- **Baseline floor:** `merge_with_baseline` keeps the pre-GoatCounter (GA4) counts as a minimum for a few posts, until GoatCounter has enough real data.

### Running it locally

```sh
GOATCOUNTER_TOKEN=... python3 .github/scripts/goatcounter_page_hits.py
cd .github/scripts && python3 -m unittest test_goatcounter_page_hits
```

### Known issues

- **Scheduled runs failed with `HTTP Error 404` from 2026-10-12 to 2026-11-02.** The failing URL was never logged, and a 404 could not be reproduced locally with a personal token (bad or missing tokens return 401). Check the next run's log, which now names the URL, and compare the repo secret with a token that works locally. See `TASKS/005-fix-goatcounter-workflow-404.md`.
