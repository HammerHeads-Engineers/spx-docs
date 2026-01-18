---
description: >-
  Run the same flow in CI. For pipelines we recommend Path B (key via CI secret)
  rather than committing a personalized Compose file.
icon: github
---

# CI/CD Setup (GitHub Actions)

This guide shows how to run your SPX server in CI and execute your unit tests against it using **GitHub Actions**. The workflow below is intentionally minimal, production‑safe, and based on a CI secret for the license key ("Path B").

## Prerequisites
- A repository with your SPX project and a working `docker compose` setup that exposes the API on `http://localhost:8000`.
- A valid **SPX_PRODUCT_KEY** for the runner to use.

## Setup on GitHub
1) Go to **Settings → Secrets and variables → Actions → New repository secret** and create `SPX_PRODUCT_KEY` with your license value.
2) Create the workflow file at **`.github/workflows/ci.yml`** (see example below).
3) Commit and push. The workflow will run on each push and pull request.

---

### Minimal workflow

{% tabs %}
{% tab title=".github/workflows/ci.yml" %}
```yaml
name: CI

on: [push, pull_request]

jobs:
  tests:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    env:
      SPX_PRODUCT_KEY: ${{ secrets.SPX_PRODUCT_KEY }}
      SPX_BASE_URL: http://localhost:8000

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Start SPX server
        run: docker compose up -d

      - name: Wait for SPX server
        run: |
          for i in {1..20}; do
            if curl -fsS http://localhost:8000/health >/dev/null; then
              echo 'SPX server is up'; exit 0
            fi
            echo 'Waiting for SPX server...'
            sleep 3
          done
          echo 'SPX server failed to start' >&2
          exit 1

      - name: Run unit tests
        run: |
          python -m unittest discover -s tests -v

      - name: Stop SPX server
        if: always()
        run: docker compose down
```
{% endtab %}

{% tab title="JSON (reference only)" %}
GitHub Actions workflows must be YAML (`.yml`/`.yaml`). This JSON is a reference format for tooling/templates; do not commit it as a workflow file.

```json
{
  "name": "CI",
  "on": [
    "push",
    "pull_request"
  ],
  "jobs": {
    "tests": {
        "runs-on": "ubuntu-latest",
      "strategy": {
        "fail-fast": false,
        "matrix": {
          "python-version": [
            "3.9",
            "3.10",
            "3.11",
            "3.12"
          ]
        }
      },
      "env": {
        "SPX_PRODUCT_KEY": "${{ secrets.SPX_PRODUCT_KEY }}",
        "SPX_BASE_URL": "http://localhost:8000"
      },
      "steps": [
        {
          "uses": "actions/checkout@v4"
        },
        {
          "name": "Set up Python",
          "uses": "actions/setup-python@v5",
          "with": {
            "python-version": "${{ matrix.python-version }}"
          }
        },
        {
          "name": "Install dependencies",
          "run": "python -m pip install --upgrade pip\\npip install -r requirements.txt"
        },
        {
          "name": "Start SPX server",
          "run": "docker compose up -d"
        },
        {
          "name": "Wait for SPX server",
          "run": "for i in {1..20}; do\\n  if curl -fsS http://localhost:8000/health >/dev/null; then\\n    echo 'SPX server is up'; exit 0\\n  fi\\n  echo 'Waiting for SPX server...'\\n  sleep 3\\ndone\\necho 'SPX server failed to start' >&2\\nexit 1"
        },
        {
          "name": "Run unit tests",
          "run": "python -m unittest discover -s tests -v"
        },
        {
          "name": "Stop SPX server",
          "if": "always()",
          "run": "docker compose down"
        }
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}

- The JSON form escapes multi-line shell steps with `\n` so the example stays self-contained.

## What this workflow does
1. **Checks out** your repository (`actions/checkout`).
2. **Sets up Python** using a matrix (3.9–3.12).
3. **Installs dependencies** from `requirements.txt`.
4. **Starts the SPX server** via `docker compose up -d` (it uses the compose file in your repo).
5. **Waits for readiness** by polling `http://localhost:8000/health`.
6. **Runs unit tests** with `unittest` (replace with `pytest` if you prefer).
7. **Tears down** containers with `docker compose down` even on failure.

## Customization tips
- **Python version / test matrix**: test multiple versions by changing `setup-python` or using matrix strategy.
- **Pytest**: swap the test step for `pytest -q` if your project uses pytest.
- **Compose filename**: if your file is `compose.yml` or lives in a subfolder, add `working-directory:` to steps or pass `-f` to `docker compose`.
- **Port / health URL**: update `http://localhost:8000/health` if your API runs on a different port or path.
- **Caching pip**: add `actions/cache` keyed by `requirements.txt` for faster runs.
- **Build vs. pull**: if images aren’t prebuilt, make sure your compose config includes build context, or add a step `docker compose build`.
- **Artifacts**: you can upload logs or junit XML via `actions/upload-artifact`.

## Troubleshooting
- **Server never becomes ready**: print logs to diagnose:
  ```bash
  docker compose ps
  docker compose logs --no-color --tail=200
  ```
  Verify your compose exposes port `8000` (or update the curl URL).

- **`fatal: could not read Username for 'https://github.com'` during checkout**: ensure you use `actions/checkout@v4` (it injects `GITHUB_TOKEN`). Do not override fetch URLs or credentials. If your repo needs additional private submodules, configure `submodules: true` and proper tokens.

- **License key problems**: confirm `SPX_PRODUCT_KEY` is set under **Settings → Secrets and variables → Actions** and is referenced in the job’s `env:`. Secrets are masked in logs; use short readiness timeouts until the server reports the version and license state.

## Security notes
- Keep secrets in **Actions secrets**; never commit them.
- Restrict who can trigger workflows on forks if your project runs untrusted code.
- Use environment‑scoped secrets for staging/production if needed.

## Next steps
- Add a test matrix (OS / Python) to widen coverage.
- Add integration tests that call your API endpoints.
- Wire this CI to **branch protection rules** so PRs must pass before merge.
