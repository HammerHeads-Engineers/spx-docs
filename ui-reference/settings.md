---
description: Review UI-level settings and server connectivity information.
icon: gear
---

# Settings

## Purpose

The Settings view is where you confirm UI-level configuration and server connectivity details. Use it to connect to the right SPX Server, adjust number formatting, and confirm subscription information.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Settings**.

## What you can do here

* Connect or disconnect from a server using Host and Port, and check the status chip.
* Validate connection inputs before request (Port must be integer in range `1..65535`).
* Get more explicit connection errors (`401` invalid key, `403` denied, network/CORS hints).
* Adjust number formatting (max decimals) and see scientific-notation thresholds.
* Review subscription plan and validity information.
* Note the SPX UI version for support and troubleshooting.

<figure><img src="../.gitbook/assets/image (26).png" alt=""><figcaption><p>Settings view</p></figcaption></figure>

> Image placeholder: Settings connection error chip showing HTTP/CORS diagnostic message.

## Typical workflow

1. Open **Settings**.
2. Connect to the server using Host/Port or confirm the current connection.
   - If the connection fails, read the detailed message and fix host/port, key, or CORS policy.
3. Adjust number formatting if you need fewer or more decimals.
4. Confirm subscription and UI version, then return to **Instances**.

## What to verify

* Integrator: the UI is connected to the intended SPX Server.
* QA: subscription info is visible and matches the test environment.
* Developer: Host/Port matches the target container or remote server.

## Common issues

* Connect is disabled or fails: confirm `SPX_PRODUCT_KEY` is available, host/port are valid, and port is in `1..65535`.
* `401` on connect: product/license key in UI does not match server key validation.
* Browser network/CORS error: verify SPX Server CORS env (`SPX_CORS_ALLOW_ORIGINS`, optional regex) and protocol (`http` vs `https`).
* UI shows no data: verify the server connection status and refresh.
* Subscription shows "Not available": confirm the server exposes license info.
* Settings section missing: check your UI build or permissions.
