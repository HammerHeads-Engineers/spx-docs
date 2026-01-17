# General View

The General view is the fastest way to confirm that your SPX Server is up and that your simulation is doing what you think it is doing.

## Typical workflow

1. **Confirm connectivity**: verify the UI is connected to the correct SPX Server (API base URL and “server is up” state).
2. **Locate the running Instance**: find the Instance you created from your Model.
3. **Inspect live state**:
   - attributes (internal/external values where applicable),
   - timers / simulated time,
   - protocol adapter status (if the model exposes communication endpoints).
4. **Trigger or observe scenarios**: run a Scenario and confirm it changes state as expected.
5. **Debug with logs**: when something looks wrong in the UI, cross-check the server logs and the API endpoints used by your tests.

## What to keep in mind

- The UI is great for interactive debugging, but MiL tests should be the authoritative regression suite.
- When a value “does not change”, first check that simulation time is being advanced deterministically (your client/test is stepping time and calling `run()`).
