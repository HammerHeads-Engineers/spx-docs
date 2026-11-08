---
description: Install SPX for Windows, macOS or Linux and verify the browser UI and API.
---

# Install SPX

**Result:** the browser UI opens and API health reports `status: ok`.
Choose the ordinary setup wizard or install through a conversation with your
own local AI agent. Browser use does not require an AI client.
This guide targets the [SPX 1.1.0 stable bundle](../release-notes.md):
installer **1.1.0**, Server **1.0.0** and UI **1.1.0**.

## Choose your operating system

[Windows](#windows) · [macOS](#macos) · [Linux/Unix](#linux-unix).
First download the package below, then follow the instructions for your OS.

## Before you start

- Docker is installed and running (Docker Desktop on Windows/macOS; Engine and Compose v2 on Linux).
- You have a product key and free local ports 3000 (UI) and 8000 (API).
- Native macOS/Windows packages provide Python 3.12. Portable setup requires a
  host interpreter; use the [requirements matrix](../overview/system-requirements-and-capability.md).

Do not share product keys or personalized generated configuration.

## Download the installer {#id-1-download-the-installer}

1. Sign in to the [SPX portal](https://www.simplephysx.com/sign-in) and select
   the workspace with an active entitlement. Community supports five instances
   for non-commercial evaluation; see the [licensing guide](../appendices/licensing-information.md).
2. Open [Product Keys](https://www.simplephysx.com/account/product-keys).
   A workspace owner or admin can reveal/copy the key for the intended license slot.
3. Open [Downloads](https://www.simplephysx.com/downloads), keep **Stable** selected,
   and choose installer **1.1.0** for your operating system.

> **Website migration:** until the new portal is available on `www.simplephysx.com`,
> use [staging Downloads](https://staging.simplephysx.com/downloads) and
> [staging Product Keys](https://staging.simplephysx.com/account/product-keys).
> Select **Stable** there as well. A staging website can distribute the stable
> product; choosing **Development** is only for explicitly requested pre-release testing.

Use the offered Windows `.exe`, macOS `.pkg`, or Linux/Unix portable `.tgz`.
Check the version and SHA-256 shown on Downloads. `downloads.simplephysx.com`
is the file-delivery host, not the sign-in or download-selection UI. Direct
file links are authorized and temporary; use the portal for a fresh link.

## Install for your operating system {#id-2-run-the-native-installer}

### Windows

Extract the Windows archive if needed, then run
`spx-installer-<version>.exe`.

- Installs SPX Tools under the per-user SPX location.
- Adds SPX Tools entries to Windows Apps / Start Menu.
- If Python is missing, the installer can install the official Python 3.12
  offline prerequisite.

### macOS

Open `spx-installer-macos-<version>.pkg`.

- Installs SPX Tools into `/Applications/SPX Tools/`.
- Uses the native macOS Installer experience, including the license step.
- Installs the official universal Python 3.12 runtime and opens Setup
  automatically after installation for the signed-in user.
- Installs launcher apps such as `SPX Setup.app`, `SPX Start.app`,
  `SPX MCP Setup.app`, `SPX Stop.app`, `SPX Cleanup.app`, and
  `SPX Uninstall.app`.

### Linux {#linux-unix}

Extract the portable archive and run its setup launcher:

```bash
tar -xzf spx-installer-<version>.tgz
cd spx-installer
./spx-install.sh
```

Use the actual extracted directory name. Generated `spx-start.sh` and
`spx-stop.sh` helpers manage the environment after setup.

## Run SPX Setup {#id-3-run-spx-setup}

Use the automatically opened Setup on macOS. If it is absent, launch
`SPX Setup` once from the location below.

Where to find it:

- Windows: Start Menu / Windows Apps under `SPX Tools`.
- macOS: `/Applications/SPX Tools/SPX Setup.app`.
- Linux/Unix: the extracted portable package provides the setup flow; generated scripts are
  used after setup.

`SPX Setup` is the main environment wizard. It:

- asks which packages or protocols you want,
- asks for your SPX product key,
- generates the local Docker Compose bundle,
- writes helper scripts,
- can start the stack immediately.

Keep **Interactive (default)** selected for the ordinary wizard. For conversational
installation, select **Configure with your own AI Agent** and follow the
[four-step Agent Setup flow](connect-llm-with-spx-mcp.md#install-with-an-ai-agent-in-four-steps).
Setup collects the key locally and prepares the agent workspace; the agent
proposes a plan and waits for your approval. Keep product keys out of chat.

Keep SPX UI enabled and LAN exposure disabled for the local first run.
The first UI exercise provides its own small model, so it does not require a
pack, starter instances or a protocol client. If you choose a pack instead,
explicitly decide whether Setup should install models and starter instances.

## Verify the local stack {#id-4-verify-the-local-stack}

After `SPX Setup` starts the stack, or after running `SPX Start`, verify:

1. Open the UI at `http://localhost:3000`.
2. Check API health.

   macOS/Linux:

   ```bash
   curl -fsS http://localhost:8000/health
   ```

   Windows PowerShell:

   ```powershell
   (Invoke-WebRequest http://localhost:8000/health).Content
   ```

3. Open API docs at `http://localhost:8000/docs`.

The expected health response includes `"status":"ok"`.

Record the installer version and the SPX Server/UI image tags from the generated
`docker-compose.generated.yml`. They have separate version series. Use the supported pair recorded in [Release Notes](../release-notes.md);
do not substitute independently newer image tags.

In **Settings**, confirm **Ready**, the intended managed upstream target and
**Authorization: Accepted by SPX server**. Rerun SPX Setup to correct the key or
upstream configuration, start the updated environment, then select **Retry**.

If Docker is unavailable, Setup explains whether the CLI, Engine or Compose is
missing. Start or unpause Docker Desktop, wait for Engine to be running, and
press Enter to retry. On macOS the tools search Docker Desktop's bundled CLI
and the per-user Docker bin directory, so a manual PATH edit is not required.


## Installation complete

When the UI opens and `/health` reports `status: ok`, the basic installation is
complete. You do not need MCP for browser use.

**Continue with [First device in the UI](README.md).**
That exercise creates one sensor, reaches **RUNNING**, and verifies that setting
`k__temperature_c` to **31.25** produces `temperature_c = 31.25°C`.
For agent access, choose [Connect your MCP client](connect-llm-with-spx-mcp.md).
Current native Setup already prepares the shared installation/runtime workspace.
Continue in that folder; a second MCP Setup is only for repair or older installs.
For code, choose [First Python program](../simulation-and-modeling/using-spx-python.md).

## Need a different setup?

[SPX Tools and generated files](../operations-and-support/spx-tools.md) covers
routine startup, shutdown, cleanup and removal.
[Manual Compose](manual-docker-compose.md) is for a project-owned server deployment.
[Common issues](../troubleshooting-and-support/common-issues-and-solutions.md)
helps identify the right environment before changing configuration.
