---
description: >-
  Run the same flow in CI. For pipelines we recommend Path B (key via CI secret)
  rather than committing a personalized Compose file.
icon: github
---

# CI/CD Setup (GitHub Actions)

Add secret

* In your repository settings → Secrets → add SPX\_PRODUCT\_KEY

Minimal workflow

{% code title=".github/workflows/ci.yml" %}
```yaml
name: CI

on: [push, pull_request]

jobs:
  tests:
    runs-on: ubuntu-latest
    env:
      SPX_PRODUCT_KEY: ${{ secrets.SPX_PRODUCT_KEY }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Start SPX server
        run: docker compose up -d

      - name: Wait for SPX server
        run: |
          for i in {1..20}; do
            if curl -fsS http://localhost:8000/ >/dev/null; then
              echo "SPX server is up"; exit 0
            fi
            echo "Waiting for SPX server..."
            sleep 3
          done
          echo "SPX server failed to start" >&2
          exit 1

      - name: Run unit tests
        run: |
          python -m unittest discover -s tests -v

      - name: Stop SPX server
        if: always()
        run: docker compose down
```
{% endcode %}
