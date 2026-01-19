---
description: Review UI-level settings and server connectivity information.
---

# Settings

## Purpose

The Settings view is where you confirm UI-level configuration and server connectivity details. Use it to verify the UI is pointing at the correct SPX Server before you troubleshoot behavior elsewhere.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Settings**.

- [Screenshot: Settings main view]

## What you can do here

- Review server base URL or connection status if the UI shows it.
- Check any environment or build information that is displayed.
- Adjust UI settings if the UI exposes them.

- [Screenshot: Server connection section]
- [Screenshot: About or build info section]

## Typical workflow

1. Open **Settings**.
2. Confirm the server base URL matches the running stack.
3. Update settings if needed and refresh the UI.
4. Return to **Instances** and confirm data loads correctly.

## What to verify

- Integrator: the UI is connected to the intended SPX Server.
- QA: environment settings align with the test environment.
- Developer: local UI points to the local or target container.

## Common issues

- UI shows no data: verify the server base URL and connectivity.
- Settings changes do not apply: refresh the UI and recheck.
- Data mismatch between UI and tests: confirm both use the same server.
- Settings section missing: check your UI build or permissions.
