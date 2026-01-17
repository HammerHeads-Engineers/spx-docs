# Release Notes

SPX ships as multiple versioned artifacts (server image, client libraries, examples). For compatibility, keep the set aligned (use `spx-examples` as a known-good reference).

## Where to look

- SPX Server releases: https://github.com/HammerHeads-Engineers/spx-server/releases
- spx-python releases: https://github.com/HammerHeads-Engineers/spx-python/releases
- SPX SDK releases: https://github.com/HammerHeads-Engineers/spx-sdk/releases
- spx-examples changelog: https://github.com/HammerHeads-Engineers/spx-examples

## Practical guidance

- Pin `simplephysx/spx-server:<tag>` in `docker-compose.yml`.
- Pin `spx-python`/`spx-sdk` versions in your Python environment.
- When upgrading, run the full MiL test suite and refresh snapshots if necessary.
