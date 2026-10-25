---
description: Start, stop, configure, clean up or uninstall a managed SPX environment.
---

# SPX Tools and generated files

After setup, use the installed SPX Tools instead of rerunning the installer.

### `SPX Setup`

Generates or refreshes your local SPX environment. Use it when installing for
the first time, changing packages, or regenerating the runtime bundle.

### `SPX Start`

Starts the previously generated SPX stack. Use it for normal day-to-day startup
after setup has already generated the environment.

### `SPX Stop`

Stops the services carrying this installation's ownership ID, including KNX
and other selected auxiliary services. Rollback snapshots and unrelated
containers are excluded. Verify the selected services are stopped before
starting again.

### `SPX Cleanup`

On macOS, stops the managed stack and removes the generated/runtime directories.
This deletes local configuration and disk snapshots in those directories.
It does not uninstall SPX Tools or remove Docker images, volumes or unrelated
containers. Export snapshots you want to keep before using Cleanup.

### `SPX MCP Setup`

Creates or refreshes the SPX MCP workspace for local MCP access. Use it after
the SPX stack is generated and reachable on `http://localhost:8000`.

### `SPX Uninstall`

macOS has a dedicated `SPX Uninstall.app` in `/Applications/SPX Tools/`.
It stops the local stack, removes SPX support files and launcher apps, and
forgets the SPX package receipt. The dialog lets you choose whether to remove
the managed MCP workspace. Back up snapshots first. Docker Desktop and the
shared Python framework are not removed by this SPX operation.

On Windows, uninstall SPX Tools through the standard Windows Apps / installed
app management flow.

On Linux/Unix, remove the generated environment and package files according to
the distribution method you used.

## Generated files and locations

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


## Continue with…

[Common issues](../troubleshooting-and-support/common-issues-and-solutions.md) for
installation-specific diagnostics, or [configuration snapshots](../getting-started/snapshots-guide.md)
before replacing an environment.
