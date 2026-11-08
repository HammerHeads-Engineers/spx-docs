---
description: Install SPX with your own AI agent or open the prepared workspace for runtime work.
icon: brain-circuit
---

# Connect an LLM with SPX MCP

The SPX 1.1.0 native installer prepares a shared workspace for installation and
later runtime work. Use **Configure with your own AI Agent** in SPX Setup to
install through a conversation, or open the prepared workspace after a normal
wizard installation. A separate MCP Setup is not required for a new native install.

## Prerequisites

- Download the [stable native installer](installation-guide.md), currently 1.1.0.
- Have Docker Desktop running and your SPX product key ready.
- Use your own installed local agent with project MCP support. Native setup
  prepares configurations for Codex, Claude Code and OpenCode v2; it does not
  install or sign in to the AI client. Native packages provide Python 3.12.

Setup tools work before the stack is running. Live runtime tools need a
successfully started SPX environment. A web chat alone cannot launch the local
tools; it needs a local execution bridge.

## Quick path

Already installed with the native wizard? Open the shared workspace below in
your local agent and use its SPX runtime tools. If your client does not load the
project configuration initially, reload that configuration once. Continue in
the same workspace and conversation after successful installation; no second
MCP Setup or routine reconnect is needed.

## Install with an AI agent in four steps

1. **Get the installer and key.** Download the Stable package and obtain your
   product key through the [installation guide](installation-guide.md).
2. **Choose Agent Setup.** Run the package, open SPX Setup and select
   **Configure with your own AI Agent**. Enter the key in Setup when asked.
   Setup shows the prepared folder to open; do not paste the key into chat.
3. **Describe your requirements.** Open that folder in your local agent and say
   **“Complete SPX setup and installation.”** Describe your devices/protocols,
   request SPX UI and startup, and review the agent's proposed configuration.
4. **Approve and open SPX.** Approve the concrete plan in the conversation.
   Wait for confirmed installation and startup, then open the reported UI
   address (normally `http://localhost:3000`). Check Settings for **Ready** and
   **Authorization: Accepted by SPX server**.

Installation creates no simulation instances by default. After success, continue
in the same conversation with a separate simulation request, or follow
[First device in the UI](README.md). The Setup terminal monitors progress;
before execution, **R** returns to the ordinary wizard if you prefer it.

## Launch SPX MCP Setup

Use this launcher for repair or an older installation whose workspace was not
prepared. A current native installation already prepares the shared workspace.

- Windows: open `SPX MCP Setup` from Windows Apps / Start Menu.
- macOS: open `/Applications/SPX Tools/SPX MCP Setup.app`.
- Linux/Unix or portable payload: run `spx-mcp-setup.sh` from the installer
  payload.

Default workspace locations:

- macOS: `~/Documents/SPX MCP Workspace`
- Windows: `%LocalAppData%\SPX\workspace`
- Linux/Unix: `~/spx-mcp-workspace`

Older installs may still have a legacy `SPX Codex Workspace`. Treat that as an
old workspace name, not the current default.

Native Setup writes project-local client configuration, shared instructions and
installation/runtime launchers. It registers `spx_setup` for installation and
`spx` for live work. Private key and connection state remain outside the agent
workspace. See the [MCP reference](mcp-reference.md#bootstrap-mcp-client-configs)
for binding, recovery and no-start behavior.

## Choose the work mode

Use `runtime_mcp` for the normal post-install workflow. This creates an
installer-managed workspace for fast MCP-first work against the live local
`spx-server`. Runtime changes are local unless you later decide to port them
into a repository workflow.

Use `repo_dev` only when you need a full Git clone of the public
[spx-examples repository](https://github.com/HammerHeads-Engineers/spx-examples)
for durable changes: models, tests, docs, packs, commits, and PRs. This mode is
for repository work that should survive beyond local runtime experiments.

Packaged MCP workspaces are read/write by default so Codex can register models,
create instances, start/stop instances, update attributes, and manage runtime
scenarios or connections. Use read-only mode only when you want inspection-only
access.

## First use in an MCP client

After successful installation and startup, open the prepared workspace in your
configured client, or continue the existing Agent Setup conversation. Then ask:

```text
Use the SPX MCP tools from this workspace. First list the available SPX MCP
tools, then check local server health, list models and instances, register or
ensure one catalog model instance if needed, start it, then read and update one
safe attribute. Report the model id, instance key, final state, and any relevant
endpoint details.
```

For normal local runtime work, a good result is short and concrete:

- the MCP server is available,
- the local SPX server is healthy,
- models and instances can be inspected,
- one model can be registered or ensured as an instance,
- instance attributes can be read or updated through MCP.

## Client support

The native installer prepares project configuration for Codex, Claude Code and
OpenCode v2. Other MCP-capable local clients can use the same local `stdio`
servers with a project configuration appropriate to that client. Use the actual
command and arguments from the generated workspace; do not replace them with
instructions intended for a standalone repository clone.

## Troubleshooting

- If the client does not initially show the tools, verify that you opened the
  generated folder and reload the project MCP configuration if necessary.
  Successful installation does not require another reload.
- For a damaged or legacy workspace, use SPX MCP Setup to repair it. Native
  Windows/macOS packages provide the Python runtime; portable workflows have
  the separate [host prerequisites](../overview/system-requirements-and-capability.md).
- If runtime tools cannot reach SPX, start the stack with `SPX Start` and verify
  `http://localhost:8000/health`.
- If you only need inspection, rerun the setup in read-only mode.

## Complete runtime reference

For tool groups, work modes, permissions, scenarios and connections, read the
[SPX MCP reference](mcp-reference.md). Public Examples contains a complete
generated offline copy at `docs/MCP.md`; client provisioning remains part of
the private product installer.
