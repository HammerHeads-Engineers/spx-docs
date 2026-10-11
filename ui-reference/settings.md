---
description: Check the managed server connection, save or load UI layout, and adjust display settings.
icon: gear
---

# Settings

## Purpose

The Settings view shows the managed connection from SPX UI to SPX Server, UI layout sessions, display preferences, and subscription information. These instructions describe UI 1.0.0-rc.75 shipped with SPX 1.1.0-rc.107.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Settings**.

## What you can do here

* Confirm **Ready**, the upstream target, and **Authorization: Accepted by SPX server**. The installed UI uses a managed same-origin proxy; Settings does not contain editable Host, Port, or product-key fields.
* Select **Retry** to repeat the connection check after correcting the installation configuration.
* Read connection diagnostics when the server is unavailable or rejects authorization.
* Use **Save session**, **Load session**, and **Reset session** to manage a copy of the UI layout on the current server.
* Adjust number formatting (max decimals) and see scientific-notation thresholds.
* Adjust the instance status refresh rate.
* Review subscription plan and validity information.
* Note the SPX UI version for support and troubleshooting.

## UI layout sessions

**Save session** copies the current browser layout and display preferences to SPX Server. **Load session** replaces the local layout with that copy and reloads the application after confirmation. **Reset session** replaces the server copy with an empty session after confirmation.

**No server session** is normal before the first save; **Load session** remains disabled until a server session exists. The server copy is held in the current server runtime and can be lost on restart or configuration Restore. Browser-local preferences may remain in the same profile.

A UI session does not preserve simulation measurements or running state. Use [Snapshots](snapshots.md) with **Save to disk** to retain simulation configuration across server restarts. After Restore, start simulations and connections manually.

## Typical workflow

1. Open **Settings**.
2. Confirm **Ready**, the intended upstream target, and accepted authorization. If the check fails, correct the generated installation configuration and select **Retry**.
3. Adjust number formatting and the instance status refresh rate.
4. Select **Save session** if you want to retain a server copy of the current UI layout. To load that copy later, select **Load session** and confirm **Load**.
5. Confirm subscription and UI version, then return to **Instances**.

## What to verify

* Integrator: the managed upstream target is the intended SPX Server and authorization is accepted.
* QA: subscription info is visible and matches the test environment.
* Developer: the server-side runtime configuration points to the intended container or remote server.

## Common issues

* Connection unavailable: confirm SPX Server is running, inspect the upstream target and diagnostics, and select **Retry** after correcting the installation.
* `401` authorization failure: check the product key in the generated installation configuration or rerun SPX Setup with the correct key. Settings does not provide a key-entry field.
* Network/proxy failure: check the managed upstream address, server availability, and deployment networking. For a custom deployment, also verify its proxy and origin configuration.
* **No server session** after restart: save the current browser layout again. Restore simulation configuration from a disk snapshot when needed.
* UI shows no data: verify the server connection status and refresh.
* Subscription shows "Not available": confirm the server exposes license info.
* Settings section missing: check your UI build or permissions.
