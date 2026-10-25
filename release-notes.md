# Release Notes

SPX ships as multiple versioned artifacts (server image, client libraries, model/examples repo). Treat releases and tags in the upstream repos as the source of truth and **pin versions in CI**.

## Source of truth

- SPX Server releases: https://github.com/HammerHeads-Engineers/spx-server/releases
- spx-python releases: https://github.com/HammerHeads-Engineers/spx-python/releases
- SPX SDK releases: https://github.com/HammerHeads-Engineers/spx-sdk/releases
- spx-examples tags (models + tests baseline): https://github.com/HammerHeads-Engineers/spx-examples/tags

## Versioning (what to expect)

The public repos use SemVer-style tags such as `v0.3.0-alpha.N` / `v0.3.0-rc.N` / `vX.Y.Z`. Pre-releases may change behavior; treat them as “moving fast” and always pin exact versions.

## Compatibility strategy

- **Keep versions aligned**: upgrade SPX Server + clients together and re-run your full MiL suite.
- **Use `spx-examples` as a known-good baseline** when you need a reference set of models/tests that match a specific stack version.
- **Pin everything in CI** (image tags + Python dependencies) so failures are actionable.

## Practical upgrade checklist

- Pin `simplephysx/spx-server:<tag>` in `docker-compose.yml`.
- Pin `spx-python`/`spx-sdk` versions in your Python environment.
- When upgrading:
  - `docker compose pull && docker compose up -d`
  - run your full MiL test suite (`pytest`)
  - refresh Snapshots only if your tests intentionally depend on them ([Snapshots — Getting Started](getting-started/snapshots-guide.md))
