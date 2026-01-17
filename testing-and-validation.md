# Testing and Validation

Testing is the quality gate for SPX models. Treat your model library like code: every change should be validated by a deterministic suite.

## Recommended layers

1. **MiL tests (pytest)**: drive SPX deterministically from Python and assert behavior end-to-end.
2. **Scenario checks**: cover multi-step sequences and fault transitions via Scenarios.
3. **Snapshot fixtures**: restore known-good starting states for stable regressions.

## Minimal CI-shaped loop

```bash
docker compose up -d
pytest
docker compose down
```

See:

- MiL tests: `getting-started/use-in-unit-tests-mil.md`
- CI: `getting-started/ci-cd-setup-github-actions.md`
- Snapshots: `getting-started/snapshots-guide.md`
