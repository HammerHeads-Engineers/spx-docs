# Snapshots

Snapshots capture the entire state of a running simulation (attributes, timers, scenarios, and protocol settings) so you can restore it later or move it between environments.

The core implements snapshots in `spx_core/snapshots/snapshot_manager.py` and `snapshots.py`.

## When to use snapshots

- **Regression testing**: freeze a known-good state before running destructive tests and restore afterward.
- **Support diagnostics**: capture a user's environment to reproduce issues.
- **Warm starts**: preload complex rigs with initialized state (e.g., machine is mid-cycle).

## YAML & API integration

Snapshots are usually triggered via API (`POST /snapshots`). YAML controls defaults:

```yaml
snapshots:
  directory: /var/spx/snapshots
  auto_on_shutdown: true
  retention: 5
```

```json
{
  "snapshots": {
    "directory": "/var/spx/snapshots",
    "auto_on_shutdown": true,
    "retention": 5
  }
}
```

Fields:

- `directory`: where to store files (server must have write access).
- `auto_on_shutdown`: automatically save on orderly shutdown.
- `retention`: number of snapshots to keep (older files are deleted).

## CLI usage

```bash
spx snapshots create --name baseline
spx snapshots list
spx snapshots restore --name baseline
```

The CLI proxies API calls; ensure the server is running and credentials are configured.

## What gets stored?

- Attribute values (internal & external).
- Active scenarios and their progress.
- Timer state (current time, step mode).
- Communication adapter overrides.
- Parameter overrides.

Sensitive data (credentials, secrets) should be kept out of snapshots; store them in parameters or vault-backed configs.

## Best practices

- Keep snapshot directories on fast storage; large models can produce sizeable files.
- Version snapshots alongside model definitions so they match schema changes.
- Use `retention` to avoid filling disks.
- Document which tests rely on specific snapshots and refresh them regularly.
