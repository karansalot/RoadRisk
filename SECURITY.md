# Security

## Scope

This is a portfolio case study, not a deployed service — there's no server, no user data, and no credentials anywhere in this repo. All scripts read static files already checked into the repo and write local output; nothing makes a network call or handles secrets. See the "Engineering notes" section of the [README](README.md#engineering-notes) for the full picture.

## Reporting a vulnerability

If you find something anyway — a dependency with a known CVE, a CI workflow misconfiguration, anything that shouldn't be possible given the scope above — please open an issue using the bug report template, or reach out to the maintainer directly rather than filing a public issue if it's sensitive.

## What's already in place

- **No secrets in the repo or its history.** Verified across every commit, not just the current tree.
- **Dependencies pinned to exact versions** in `requirements.txt`, with [Dependabot](.github/dependabot.yml) opening weekly PRs for updates to both the Python dependencies and the GitHub Actions used in CI.
- **CI runs with least-privilege permissions** (`contents: read` only) and uses the `pull_request` trigger, not `pull_request_target` — a fork's pull request can't access repo secrets or write anything.
- **GitHub's automatic secret scanning** is on by default for this public repo as a backstop.
