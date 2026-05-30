---
description: Connect Codex to your local SPX runtime with the packaged SPX MCP server.
icon: cable
---

# Connect an LLM with SPX MCP

SPX MCP is the recommended path after `SPX Setup` has generated and started
your local SPX stack. It gives Codex a local MCP server that understands the
SPX catalog, profiles, packs, model validation rules, runtime logs,
communication trees, protocol bindings, and the running `spx-server`.

The installer flow is Codex-first: `SPX MCP Setup` writes a ready
`.codex/config.toml` for the generated workspace. The same `spx-mcp` server is a
local MCP `stdio` server, so Claude Code or another MCP-compatible client can
use it too after you configure that client manually.

## Prerequisites

- SPX is installed with the native installer.
- `SPX Setup` has generated the local environment.
- The SPX stack is running and `http://localhost:8000/health` returns
  `"status":"ok"`.
- Python 3.10+ is available for the MCP runtime.
- Codex is installed if you want the automatic workspace flow.

## Quick path

1. Start SPX with `SPX Setup` or `SPX Start`.
2. Verify the API at `http://localhost:8000/health`.
3. Launch `SPX MCP Setup`.
4. Choose `runtime_mcp` unless you intentionally need full repository work.
5. Keep the default read/write MCP access for normal local runtime work.
6. Open the generated workspace in Codex.
7. Start a fresh Codex thread so the host app reloads `.codex/config.toml`.

## Launch SPX MCP Setup

Use the launcher for your platform:

- Windows: open `SPX MCP Setup` from Windows Apps / Start Menu.
- macOS: open `/Applications/SPX Tools/SPX MCP Setup.app`.
- Linux/Unix or portable payload: run `spx-mcp-setup.sh` from the installer
  payload.

Default workspace locations:

- macOS: `~/Documents/SPX Codex Workspace`
- Windows: `%LocalAppData%\SPX\workspace`
- Linux/Unix: `~/spx-codex-workspace`

The setup creates:

- a local `.venv` prepared for `spx-mcp`,
- `.codex/config.toml` pointing Codex at the local MCP server,
- `.codex/workspace_mode.toml` with the selected work mode,
- `.spx-mcp-workspace.json` with workspace metadata,
- an `.env` seeded from the generated SPX environment when available.

## Choose the work mode

Use `runtime_mcp` for the normal post-install workflow. This creates an
installer-managed workspace for fast MCP-first work against the live local
`spx-server`. Runtime changes are local unless you later decide to port them
into a repository workflow.

Use `repo_dev` only when you need a full Git clone of `spx-examples` for
durable changes: models, tests, docs, packs, commits, and PRs.

Packaged MCP workspaces are read/write by default so Codex can register models,
create instances, start/stop instances, update attributes, and manage runtime
scenarios or connections. Use read-only mode only when you want inspection-only
access.

## First use in Codex

Open the generated workspace in Codex and start a new thread. Then ask Codex:

```text
Use the SPX MCP tools from this workspace. First list the available SPX MCP
tools, then check local server health, list models and instances, register or
ensure one catalog model instance if needed, start it, then read and update one
safe attribute. Report the model id, instance key, final state, and any relevant
endpoint details.
```

For normal local runtime work, a good Codex result is short and concrete:

- the MCP server is available,
- the local SPX server is healthy,
- models and instances can be inspected,
- one model can be registered or ensured as an instance,
- instance attributes can be read or updated through MCP.

## Other MCP clients

Codex is the only client auto-configured by the installer today. Other
MCP-compatible clients can use the same local `stdio` server, but you must add
the MCP server entry to that client's configuration yourself.

The command shape is the same one written into the generated Codex config: run
Python from the workspace `.venv`, execute `-m spx_mcp stdio`, and include
`--allow-write` when you want runtime write tools.

## Troubleshooting

- If Codex does not show the SPX MCP tools, open the generated workspace and
  start a fresh thread so `.codex/config.toml` is reloaded.
- If setup cannot find Python, install Python 3.10+ and rerun `SPX MCP Setup`.
- If runtime tools cannot reach SPX, start the stack with `SPX Start` and verify
  `http://localhost:8000/health`.
- If you only need inspection, rerun the setup in read-only mode.
