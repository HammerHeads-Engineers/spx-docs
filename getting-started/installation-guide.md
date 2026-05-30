---
description: >-
  Install SPX with the native installer for your platform, then run SPX Setup to
  generate and start your local environment.
icon: up-to-dotted-line
---

# Installation Guide

Use the native SPX release artifact for your platform, complete the installer,
and then run `SPX Setup` to generate your local SPX environment.

This page is aligned with `spx-examples` `origin/develop` at
`518d631ed9649810445ac9f0c5474ecd22880167` (`spx-examples` `1.1.0-rc.48`).
At that snapshot the generated installer bundles use:

- SPX Server image: `simplephysx/spx-server:v1.0.0-rc.64`
- SPX UI image: `simplephysx/spx-ui:v1.0.0-rc.68`

Installer file names on the download page are versioned. The examples below use
`<version>` intentionally so this page does not go stale on every RC.

Quick path:

1. Download the current installer from `simplephysx.com/keys`.
2. On Windows and Linux, extract the delivery archive first if the download page
   wraps the native installer in `.zip` or `.tar`.
3. Run the native installer for your platform.
4. Run `SPX Setup` after installation completes.
5. Let setup start the stack, or run `SPX Start`.
6. Verify the UI and API on localhost.

After setup, verify:

- **UI**: `http://localhost:3000`
- **API**: `http://localhost:8000`
- **API docs**: `http://localhost:8000/docs`

If you only need the SPX Server with a manual Compose flow, see
[Advanced: Manual Docker Compose (server-only)](manual-docker-compose.md).

## Prerequisites

- Docker must be installed and running.
- Windows and macOS users should use Docker Desktop.
- Linux users need Docker Engine with Docker Compose v2.
- macOS and Linux require access to a local Python installation for the setup flow.
- The Windows installer can install the Python prerequisite automatically.
- A valid SPX product key is required.
- Local ports `3000` and `8000` should be available. Pack selections can expose
  more ports, for example Modbus, MQTT, BACnet, OPC UA, Home Assistant, KNX, and
  Matter ports.

> Security: treat your `SPX_PRODUCT_KEY` as a secret. Do not commit it to git
> or share generated bundles that contain a real key.

## 1) Download the recommended installer for your platform

Download the current installer from
[simplephysx.com/keys](https://simplephysx.com/keys). This subscriber-only page
contains your available SPX product keys and the download links for the current
installers.

Use the native installer artifact that matches your OS:

- Windows: `spx-installer-<version>.exe`
- macOS: `spx-installer-macos-<version>.pkg`
- Linux/Unix: `spx-installer-<version>.run`

On the subscriber download page, the Windows and Linux installers may be
delivered inside archives:

- Windows: download the `.zip`, extract it, then run
  `spx-installer-<version>.exe`
- Linux/Unix: download the `.tar`, extract it, then run
  `spx-installer-<version>.run`
- macOS: download and open `spx-installer-macos-<version>.pkg`

The portable `.tgz` and `.zip` archives mentioned later in this guide are
fallback artifacts only. Do not confuse them with a delivery archive that wraps
the Windows or Linux native installer download.

## 2) Run the native installer

### Windows

Download the Windows archive from [simplephysx.com/keys](https://simplephysx.com/keys),
extract the `.zip` if needed, then run `spx-installer-<version>.exe`.

- The EXE is a Windows-native installer for `SPX Tools`.
- It installs the application payload under `%LocalAppData%\SPX\app`.
- Start Menu and Windows Apps entries are grouped under `SPX Tools`.
- If Python is missing, the installer can install the official Python 3.12
  offline prerequisite for you.

### macOS

Download and open `spx-installer-macos-<version>.pkg`.

- The PKG installs `SPX Tools` into `/Applications/SPX Tools/`.
- The installation flow uses the native macOS `Installer.app` experience,
  including the license step.

### Linux/Unix

Download the Linux archive from [simplephysx.com/keys](https://simplephysx.com/keys),
extract the `.tar` if needed, then make `spx-installer-<version>.run`
executable and run it.

```bash
tar -xf <downloaded-file>.tar
chmod +x spx-installer-<version>.run
./spx-installer-<version>.run
```

- The `.run` file is the recommended release artifact on Linux/Unix.
- It self-extracts to a temporary directory and launches the same terminal-based
  installer engine used by the portable package.

## 3) Run SPX Setup

The native installer/bootstrapper itself is not the environment wizard. After
installation, run `SPX Setup` so SPX can generate the local environment and
install/start the services, packs, models, and UI you choose.

`SPX Setup` does the user-facing setup work:

- It guides you through package or protocol selection.
- It generates the local compose bundle and helper scripts.
- It can start the stack immediately after generation.
- It writes a generated runtime environment that can be managed later with
  `SPX Start`, `SPX Stop`, and `SPX Cleanup`.

Current wizard flow:

- `Enter package numbers (comma-separated, ENTER for default protocols, 0 for protocols, q to quit):`
- `Add models from selected packages? [Y/n]:` (shown only when packages are selected)
- `Add default instances? [y/N]:` (shown only when models are enabled)
- `Include SPX UI frontend container? [Y/n]:`
- `Start the stack immediately after generation? [Y/n]:`
- Product key prompt

If you press `ENTER` at the package selection prompt, the wizard chooses the
default protocol set (`Modbus + SCPI/ASCII` when available), skips model and
instance prompts, keeps the SPX UI enabled, and starts the stack by default.

If you select a pack, decide explicitly whether to add models and default
instances. Default instance creation is opt-in (`[y/N]`). For large packs,
current installer logic narrows default instance generation to the starter
instances selected for startup.

## 4) Platform-specific behavior and install locations

### Windows

- The generated runtime environment lives under `%LocalAppData%\SPX\generated`.
- The installer-managed Codex workspace lives under `%LocalAppData%\SPX\workspace`.
- Windows installs shortcuts for `SPX Setup`, `SPX MCP Setup`, `SPX Start`,
  `SPX Stop`, and `SPX Cleanup`.
- Do not use a separate `SPX Uninstall` launcher on Windows. Uninstall is done
  through the standard Windows Apps / installed app management flow.

### macOS

- Installed apps: `SPX Setup.app`, `SPX MCP Setup.app`, `SPX Start.app`,
  `SPX Stop.app`, `SPX Cleanup.app`, and `SPX Uninstall.app`.
- `SPX Setup.app` contains the full installer payload and launches the
  terminal-based wizard without asking you to trust a loose downloaded
  `.command` file.
- The generated runtime environment lives under
  `~/Library/Application Support/SPX/generated`.
- The installer runtime lives under
  `~/Library/Application Support/SPX/runtime`.
- The installer-managed Codex workspace is created at
  `~/Documents/SPX Codex Workspace`.

### Linux/Unix

- Generated files live under `~/.local/share/spx/generated` when SPX runs from
  an installed or non-writable packaged location.
- Runtime files live under `~/.local/share/spx/runtime`.
- Linux does not install the macOS/Windows-style launcher apps.
- After setup, Linux users primarily work with generated scripts such as
  `spx-start.sh` and `spx-stop.sh`.

## 5) What each installed launcher does

### `SPX Setup`

Use this right after the native installer finishes.

- It is the main post-install entrypoint.
- It generates or refreshes the local SPX environment.
- It writes the generated compose bundle and helper scripts.
- It can start the stack immediately.

### `SPX Start`

- It starts the previously generated SPX stack.
- It is the normal day-to-day entrypoint when you want to bring the local
  environment back up without rerunning setup.

### `SPX Stop`

- It stops the generated SPX stack.
- Use it to shut down the local environment cleanly.

### `SPX Cleanup`

- It removes the generated SPX environment and related Docker resources.
- It does not uninstall the native app or package itself.
- Use it when you want to reset the generated environment and regenerate it
  later with `SPX Setup`.

### `SPX Uninstall`

- This is a dedicated macOS app only.
- It stops the local stack, removes generated SPX files, deletes the installed
  SPX apps, forgets the macOS package receipt, and can optionally remove the
  installer-managed workspace.
- On Windows, use standard Windows app management instead of a dedicated
  launcher.

### `SPX MCP Setup`

- It creates or refreshes the installer-managed Codex MCP workspace.
- It prepares a local Python environment for that workspace.
- It writes `.codex/config.toml` and points Codex at the local SPX MCP server.
- During setup you choose a work mode: `runtime_mcp` for an installer-managed
  MCP workspace copy, or `repo_dev` for a full Git clone of `spx-examples` on
  `develop`.
- For packaged setup, pressing `ENTER` should suggest or select `runtime_mcp`
  by default.
- The generated MCP workspace is write-enabled by default unless you explicitly
  choose read-only mode.

## 6) What the setup wizard generates

The generated environment is created in the platform-specific locations listed
above. In practical terms, `SPX Setup` writes:

- `docker-compose.generated.yml` with only the selected services
- `.env` containing `SPX_PRODUCT_KEY=REPLACE_ME` until you insert a real key
- `bundle.json` for bootstrap
- `bootstrap_runner.py` and `runtime_bootstrap.py`
- `spx-start.sh`, `spx-stop.sh`, `spx-start.ps1`, `spx-stop.ps1`, plus desktop
  convenience launchers such as `.command` and `.bat`
- `assets/`, `extensions/`, and selected `library/` files needed by the bundle

## 7) Verify the installation

After `SPX Setup` finishes, either let it start the stack immediately or use
`SPX Start` to bring the environment up before verifying it.

1. Open the UI at `http://localhost:3000`.
2. Check API health.

   macOS/Linux:

   ```bash
   curl -fsS http://localhost:8000/health
   ```

   Windows (PowerShell):

   ```powershell
   (Invoke-WebRequest http://localhost:8000/health).Content
   ```

3. Open API docs at `http://localhost:8000/docs`.

The expected health response includes `"status":"ok"`.

## 8) Portable fallback

Portable `.tgz` and `.zip` archives are fallback artifacts for internal
sharing, debugging, or manual payload handoff. They are not the recommended
main installation path.

If you are intentionally using a portable archive, the fallback entrypoints are:

- `spx-setup.command`
- `spx-setup.desktop`
- `spx-setup.sh`
- `spx-setup.bat`
- Direct `spx-install.sh` or `spx-install.ps1` usage as an advanced manual
  fallback

If you run into problems during setup or startup, see
[Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md).

## Next steps

- Smart Building Pack walkthrough: [Smart Building Pack: First Run Walkthrough](first-run-smart-building-pack.md)
- Build your own simulation: [Build Your First Simulation](build-your-first-simulation.md)
- Troubleshooting runbook: [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)
