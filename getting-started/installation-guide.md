---
description: >-
  Install SPX with the ready native installer for your platform, then run SPX
  Setup to generate and start your local environment.
icon: up-to-dotted-line
---

# Installation Guide

The recommended installation path is to use the ready native installer for your
operating system. The installer packages include the setup wizard and the SPX
Tools launchers you need for day-to-day work.

Quick path:

1. Make sure Docker is installed and running.
2. Download the installer for your platform from
   [simplephysx.com/keys](https://simplephysx.com/keys).
3. Run the native installer.
4. Launch `SPX Setup` from the installed SPX Tools.
5. Let `SPX Setup` generate and start your local SPX environment.
6. Verify the UI and API on localhost.
7. Launch `SPX MCP Setup`, open the generated `SPX MCP Workspace` in Codex,
   Claude Code, or another MCP-capable client, and start a fresh session so the
   client loads the local MCP config.

After setup, verify:

- **UI**: `http://localhost:3000`
- **API**: `http://localhost:8000`
- **API docs**: `http://localhost:8000/docs`

## Prerequisites

- Docker must be installed and running before you start SPX.
- Windows and macOS users should use Docker Desktop.
- Linux users need Docker Engine with Docker Compose v2.
- A valid SPX product key is required.
- Python 3.10+ is required for `SPX MCP Setup`.
- Local ports `3000` and `8000` should be available.

> Security: treat your `SPX_PRODUCT_KEY` as a secret. Do not commit it to git
> or share generated bundles that contain a real key.

## 1) Download the installer

Download the current installer from
[simplephysx.com/keys](https://simplephysx.com/keys). This page contains your
available SPX product keys and the download links for the prepared installers.

Use the package for your platform:

- Windows: `spx-installer-<version>.exe`
- macOS: `spx-installer-macos-<version>.pkg`
- Linux/Unix: `spx-installer-<version>.run`

On Windows and Linux, the download page may wrap the installer in a delivery
archive:

- Windows: download the `.zip`, extract it, then run the `.exe`.
- Linux/Unix: download the `.tar`, extract it, then run the `.run`.
- macOS: download and open the `.pkg`.

These are the recommended installer packages. Portable `.tgz` and `.zip`
payloads are fallback artifacts for advanced or internal use.

## 2) Run the native installer

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
- Installs launcher apps such as `SPX Setup.app`, `SPX Start.app`,
  `SPX MCP Setup.app`, `SPX Stop.app`, `SPX Cleanup.app`, and
  `SPX Uninstall.app`.

### Linux/Unix

Extract the Linux archive if needed, make the `.run` executable, and run it:

```bash
tar -xf <downloaded-file>.tar
chmod +x spx-installer-<version>.run
./spx-installer-<version>.run
```

The `.run` package starts the same terminal setup flow used by SPX Setup. After
setup, day-to-day work happens through the generated shell scripts such as
`spx-start.sh` and `spx-stop.sh`.

## 3) Run SPX Setup

After the native installer finishes, launch `SPX Setup`.

Where to find it:

- Windows: Start Menu / Windows Apps under `SPX Tools`.
- macOS: `/Applications/SPX Tools/SPX Setup.app`.
- Linux/Unix: the `.run` package launches the setup flow; generated scripts are
  used after setup.

`SPX Setup` is the main environment wizard. It:

- asks which packages or protocols you want,
- asks for your SPX product key,
- generates the local Docker Compose bundle,
- writes helper scripts,
- can start the stack immediately.

If you accept the default package selection, setup uses the default protocol
set (`Modbus + SCPI/ASCII` when available), keeps SPX UI enabled, and skips
model installation. If you select a pack, decide explicitly whether to add
models and starter instances.

## 4) Verify the local stack

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

## 5) Connect an LLM with SPX MCP

SPX MCP is the recommended next step after the local stack is running. It lets
MCP-capable LLM clients call the local SPX server through the packaged
`spx-mcp` server, inspect models and instances, register catalog models, and
make runtime changes through MCP tools.

Launch `SPX MCP Setup`:

- Windows: Start Menu / Windows Apps under `SPX Tools`.
- macOS: `/Applications/SPX Tools/SPX MCP Setup.app`.
- Linux/Unix or portable payload: run `spx-mcp-setup.sh` from the installer
  payload.

The setup creates an `SPX MCP Workspace` with:

- a local `.venv` for the MCP server,
- `.codex/config.toml` pointing Codex at the local `spx-mcp` server,
- `.mcp.json` pointing Claude Code at the same local `spx-mcp` server,
- `CLAUDE.md` so Claude Code can follow `@AGENTS.md`,
- `.spx/workspace_mode.toml` with the selected work mode,
- `.spx-mcp-workspace.json` with workspace metadata.

Choose `runtime_mcp` for normal post-install work with the local `spx-server`.
Use `repo_dev` only when you want a full `spx-examples` checkout for durable
repository changes, tests, docs, commits, or PRs. Packaged workspaces are
read/write by default; use read-only mode only for inspection-only access.
Existing `.codex/workspace_mode.toml` files are still read as a legacy
fallback.

After setup finishes, open the generated workspace in Codex, Claude Code, or
another MCP-capable client and start a fresh session so the client reloads the
local MCP configuration.

Full walkthrough: [Connect an LLM with SPX MCP](connect-llm-with-spx-mcp.md).

## 6) Use SPX Tools

After setup, use the installed SPX Tools instead of rerunning the installer.

### `SPX Setup`

Generates or refreshes your local SPX environment. Use it when installing for
the first time, changing packages, or regenerating the runtime bundle.

### `SPX Start`

Starts the previously generated SPX stack. Use it for normal day-to-day startup
after setup has already generated the environment.

### `SPX Stop`

Stops the generated SPX stack cleanly.

### `SPX Cleanup`

Removes the generated SPX environment and related Docker resources. It does not
uninstall the native SPX Tools package.

### `SPX MCP Setup`

Creates or refreshes the SPX MCP workspace for local MCP access. Use it after
the SPX stack is generated and reachable on `http://localhost:8000`.

### `SPX Uninstall`

macOS has a dedicated `SPX Uninstall.app` in `/Applications/SPX Tools/`.

On Windows, uninstall SPX Tools through the standard Windows Apps / installed
app management flow.

On Linux/Unix, remove the generated environment and package files according to
the distribution method you used.

## 7) What SPX Setup creates

The generated runtime environment contains:

- `docker-compose.generated.yml`
- `.env`
- `bundle.json`
- start/stop scripts for Bash, zsh, PowerShell, and desktop launchers
- selected assets, extensions, and model library files

Default generated locations:

- Windows: `%LocalAppData%\SPX\generated`
- macOS: `~/Library/Application Support/SPX/generated`
- Linux/Unix: `~/.local/share/spx/generated`

## Advanced fallback

Use portable archives or manual Docker Compose only when you intentionally need
an advanced fallback flow, debugging payload, or server-only setup.

- Portable installer and packs: [Installer and packs](installer-and-packs.md)
- Server-only Compose: [Advanced: Manual Docker Compose](manual-docker-compose.md)
- Troubleshooting: [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)

## Next steps

- Connect an MCP-capable LLM client: [Connect an LLM with SPX MCP](connect-llm-with-spx-mcp.md)
- Smart Building Pack walkthrough: [Smart Building Pack: First Run Walkthrough](first-run-smart-building-pack.md)
- Build your own simulation: [Build Your First Simulation](build-your-first-simulation.md)
- Troubleshooting runbook: [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)
