---
description: Runtime snapshot fields and restore behavior; no live-value checkpoint.
icon: floppy-disks
---

# Snapshot runtime reference

Snapshots save model definitions, instance/template relationships and connections.
They restore configuration and structure, not live attribute values, elapsed
time, scenario progress, threads or network sessions. Reapply runtime inputs,
seeds and warmup after import. A default of 20°C saved while the runtime reads
42°C restores 20°C, not 42°C.

## YAML and API integration

The registered `snapshots` component uses these configuration fields:

```yaml
snapshots:
  base_dir: ./snapshots
  persist_memory_to_disk: false
  memory_subdir: memory
```

`base_dir` must be writable by the server. `persist_memory_to_disk` optionally
persists in-memory snapshots under `memory_subdir`. The runtime does not expose
`directory`, `auto_on_shutdown` or `retention` as the documented configuration
contract; manage retention explicitly in your operational process.

Use the UI or Python client. API v3 invokes snapshot component methods under
`/api/v3/system/snapshots/method/<method>`, for example `save`, `list` and `load`.
See [Snapshots — Getting Started](../getting-started/snapshots-guide.md) for
request bodies and client examples. There is no product `spx snapshots create`
CLI documented for this release.

## Import behavior

Runtime replacement stops and tears down existing children before rebuilding
the tree. Active license/configuration limits remain enforced. Import can load
structure without automatically starting all instances; verify and start the
required instances and connections after restoration. Keep the exported model
and runtime versions with your snapshot.

Snapshots and exported configuration can contain instance metadata or values
that are sensitive. Inspect and sanitize them before sharing. Do not assume
that placing a key in a model parameter removes it from an export.
