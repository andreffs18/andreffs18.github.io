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

## `feedly_opml.yml`

Runs weekly (Monday 06:30 UTC, or on demand with `workflow_dispatch`). It runs `.github/scripts/feedly_opml.sh`, which downloads your subscriptions from Feedly (`GET https://cloud.feedly.com/v3/opml`), and compares them with `assets/feedly.opml`, the source for the "Resources I follow" page. Only if they differ does it replace the file, commit and push; otherwise it logs "OPML unchanged" and makes no commit.

It needs a `FEEDLY_TOKEN` repository secret: a Feedly access token.

### How it behaves

- **Retries:** curl retries transient failures (timeouts, 429, 5xx) three times. Anything else fails the job.
- **Expired token:** a 401 fails the run and prints Feedly's response (`token expired: …`), so GitHub's failure email is the reminder to refresh the secret. Feedly developer tokens are reported to last about 30 days (third-party sources, not confirmed by Feedly's docs), so expect to renew it periodically.
- **No noise commits:** the comparison is byte-for-byte against the committed file, so an unchanged subscription list produces no commit. If Feedly ever reorders the export without any real change, you'd get a commit; the log prints the start of the diff so you can tell.
- **The diff is the only gate:** the response isn't otherwise validated. An error status fails the job before anything is written, which covers the realistic failures.

### Running it locally

```sh
FEEDLY_TOKEN=... .github/scripts/feedly_opml.sh assets/feedly.opml
```

## `goatcounter_page_hits.yml`

Runs weekly (Monday 06:00 UTC, or on demand with `workflow_dispatch`). It runs `.github/scripts/goatcounter_page_hits.py`, which fetches page view counts from the GoatCounter API and writes `data/goatcounter_page_hits.json` (the "Blogpost view stats"). If the file changed, the workflow commits and pushes it.

It needs a `GOATCOUNTER_TOKEN` repository secret: a GoatCounter API token with read access to statistics.

### How the script behaves

- **All-time totals:** every request sends `start=2020-01-01T00:00:00Z`. Without `start` the API only returns a recent window (in a check on 2026-11-06: 103 views over 29 paths, versus 308 over 49 with it).
- **Pagination:** `GET /api/v0/stats/hits` has no cursor. The script pages by passing the path IDs it has already seen in `exclude_paths`. (`after` is not a GoatCounter parameter and returns a 400.)
- **Retries:** 429, 5xx and network errors are retried (4 attempts, exponential backoff with jitter, `Retry-After` honored). The first request also retries a 404, after 15s, 30s and 60s (see Known issues). Any other 4xx, including a 404 on a later page, fails immediately.
- **Failures are readable:** the run prints the HTTP status, the URL and the `<title>` of an HTML error page (or the start of the body), never the token.
- **No bad writes:** the data file is only written after every page has been fetched, so a failed run leaves the previous data untouched.
- **Baseline floor:** `merge_with_baseline` keeps the pre-GoatCounter (GA4) counts as a minimum for a few posts, until GoatCounter has enough real data.

### Running it locally

```sh
GOATCOUNTER_TOKEN=... python3 .github/scripts/goatcounter_page_hits.py
```

### Known issues

- **The first request after a long idle period can return a transient 404.** GoatCounter answers with its HTML error page (`GoatCounter – Error!`) and the same request works about a minute later. This made the scheduled runs fail on 2026-10-12 to 2026-11-02 and 2026-11-16, while a manual re-run right after passed. The cause on GoatCounter's side is unconfirmed, so the script retries a 404 on the first request only. If a scheduled run still fails with a 404, check whether all retries were used (the log shows `attempt n/4`). See `TASKS/COMPLETED/005-fix-goatcounter-workflow-404.md`.
