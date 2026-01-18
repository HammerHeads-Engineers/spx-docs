# Hardware Bridges & Backends

Sometimes your simulation needs to talk to the outside world:

- a lab instrument on USB/Ethernet,
- a PLC on a fieldbus,
- a custom protocol stack,
- a HIL rig or data acquisition device.

This page documents patterns that keep SPX models **deterministic** while still integrating with real systems.

## Choose the integration boundary

**Option A: external backend process (recommended)**

- Run a separate service (HTTP/TCP/etc.) next to SPX.
- Keep SPX deterministic: the model pushes/pulls data at explicit step boundaries.
- Example pattern: the BLE integration uses a companion `spx-ble-adapter` process ([BLE Adapter](../../spx-core/communications/ble.md)).

**Option B: code running inside the SPX Server container**

- Works when you can package dependencies and the backend calls are predictable.
- Avoid blocking I/O in tight `run()` loops; prefer buffered reads/writes and timeouts.

## Docker networking checklist

- If the backend runs on the **host** and SPX runs in Docker, use `host.docker.internal` as the host address (where supported).
- If the backend runs in the **same compose project**, refer to it by compose service name and keep ports internal where possible.
- Expose only the ports you need on the host. Keep protocol ports (Modbus, SCPI, etc.) aligned with the models you load.

## Determinism constraints (non-negotiable for tests)

- Do not use wall-clock sleeps for simulation behavior. Drive simulated time from the client (MiL tests).
- Treat external data as inputs sampled at step boundaries; record it if you need repeatable regression tests.
- Keep failure modes explicit: timeouts, retries, and “no data” behavior should be modeled (and tested).
