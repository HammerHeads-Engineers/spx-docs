# Snapshots — Getting Started

This guide shows how to **save**, **list**, and **load** system snapshots using SPX. Snapshots capture the **structure** of your system (models, instances, and connections) so you can quickly persist and restore configurations.

> **What a snapshot captures**
>
> - Model templates (their definitions)
> - Instances (which instance uses which template)
> - Connections (wiring between instances)
>
> **What it does _not_ capture (MVP)**
>
> - Runtime state (thread state, attribute runtime values, timers, …)  
>   Snapshots currently rebuild structure; runtime state always starts “fresh”.

---

## Prerequisites

- SPX Server `v0.3.0+` with API v3 enabled.
- Your `System` has the `snapshots` component mounted (this is default in recent builds).
- `spx-python` client connected to your server (examples below).

---

## Quick Start (with `spx-python`)

### 1) Save a snapshot (default, durable)

By default, calling `save()` with no arguments creates an in-memory snapshot **and** persists it to disk (durable mode). You get a unique `id` and a `persisted_path`.

```python
resp = client["snapshots"].save()
print(resp)
```

Example output:

```json
{
  "result": {
    "id": "c2b8dfed-ba63-4d6b-bc08-b29daa142a45",
    "in_memory": true,
    "persisted_path": "/app/snapshots/memory/c2b8dfed-ba63-4d6b-bc08-b29daa142a45.json"
  }
}
```

### 2) List available snapshots

```python
client["snapshots"].list()
```

Example output:

```json
{
  "result": {
    "in_memory": [],
    "files": [
      {
        "path": "/app/snapshots/memory/c2b8dfed-ba63-4d6b-bc08-b29daa142a45.json",
        "id": "c2b8dfed-ba63-4d6b-bc08-b29daa142a45",
        "created_at": "2025-09-10T19:57:53.267730Z",
        "label": null,
        "notes": null
      }
    ]
  }
}
```

### 3) Load a snapshot

You can load by **path** or by **id**.

**By path**:

```python
client["snapshots"].load(path="/app/snapshots/memory/c2b8dfed-ba63-4d6b-bc08-b29daa142a45.json")
```

**By id** (when persisted in durable mode, the manager locates the file under the configured directory):

```python
client["snapshots"].load(id="c2b8dfed-ba63-4d6b-bc08-b29daa142a45")
```

> **Effect of `load()`**
>
> In the standard configuration, `load()` **replaces the active System** in place (runtime replace).  
> This means further API calls operate on the newly loaded system structure.

---

## Saving to a specific file

If you want a deterministic file name and location:

```python
client["snapshots"].save(path="/app/snapshots/runs/run_001/system.json")
```

Or compose from directory + name:

```python
client["snapshots"].save(directory="/app/snapshots/runs/run_002", name="system.json")
```

You can optionally attach metadata:

```python
client["snapshots"].save(
    directory="/app/snapshots/runs/run_003",
    name="system.json",
    label="before-experiment",
    notes="PID tuned to kp=2.5, ki=0.01, kd=0.01"
)
```

---

## Persistence behavior

- **Durable-by-default**: The default `save()` persists to disk (and still returns an `id` for convenience).
- **In-memory only**: If your setup is configured for *non-durable* mode, in-memory saves do not create a file (the response will have `persisted_path: ""`). You can later persist all in-memory snapshots with:
  ```python
  client["snapshots"].persist_all_in_memory()
  ```

> **Tip**
>
> The snapshot file includes minimal metadata (id, timestamp, optional label/notes) and the structure definition.  
> Schema evolution is handled by a simple `schema_version` field inside the file.

---

## Using the generic API v3 endpoints (HTTP)

All operations can be performed via the generic _“call method”_ endpoint on the `snapshots` component:

- **Save**  
  `POST /api/v3/system/snapshots/method/save`  
  Body (optional):
  ```json
  {
    "kwargs": {
      "path": "/app/snapshots/runs/run_001/system.json"
    }
  }
  ```
  Response includes `id` and, in durable mode, `persisted_path`.

- **List**  
  `POST /api/v3/system/snapshots/method/list`  
  Body:
  ```json
  { "kwargs": {} }
  ```

- **Load by id**  
  `POST /api/v3/system/snapshots/method/load`  
  Body:
  ```json
  { "kwargs": { "id": "c2b8dfed-ba63-4d6b-bc08-b29daa142a45" } }
  ```

- **Load by path**  
  ```json
  { "kwargs": { "path": "/app/snapshots/memory/c2b8dfed-ba63-4d6b-bc08-b29daa142a45.json" } }
  ```

---

## Troubleshooting

- **“File not found” on load by id**  
  Ensure the snapshot was saved in durable mode or the manager is configured with the same base directory used when saving.

- **No `models`/`instances` after load**  
  Snapshots capture structure. If you are exploring the live tree immediately after `load()`, confirm your `System` populates children during initialization. You can always inspect the stored definition inside the loaded system (implementation may expose it as `definition` or `definition_snapshot` for debugging).

- **Different IDs between file name and snapshot id**  
  Depending on configuration, file names may be derived from either the snapshot id or another chosen naming scheme. Always rely on `list()` to map ids to file paths.

---

## Minimal end‑to‑end example

```python
# Save (durable by default)
s1 = client["snapshots"].save()
snap_id = s1["result"]["id"]

# Verify it’s on disk
listing = client["snapshots"].list()

# Load by id (replaces active System)
client["snapshots"].load(id=snap_id)

# Continue working on the restored system…
```

That’s it! You now know how to persist and restore system structure using SPX Snapshots.