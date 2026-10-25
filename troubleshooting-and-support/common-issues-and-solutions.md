# Common Issues and Solutions

First identify the installation shape. Do not install dependencies into a random
host Python or replace a managed connection by guessing which `.env` is active.

| Installation | Working directory / tools | First check |
| --- | --- | --- |
| Managed SPX Tools installation | installed launchers and Setup-selected generated environment | SPX Start/Setup; Docker running; generated stack status |
| Managed MCP workspace | workspace created by SPX MCP Setup, its `.venv` | fresh client session, MCP doctor/configuration and private server binding |
| Public Examples checkout | clone root, Poetry environment | repo instructions, validator and MCP setup scripts |
| Project-owned Compose | directory containing your Compose file | explicit Compose file, env and host mappings |

## Managed stack or MCP is unavailable

1. Open SPX Start for the generated environment you intended to use. If the
   environment is missing, rerun SPX Setup; do not start a second guessed stack.
2. Verify `http://localhost:8000/health` and UI `http://localhost:3000` (if installed).
   A public health response does not prove the product key is accepted.
3. For MCP rerun SPX MCP Setup to bind the workspace to that environment, then
   open a fresh client session. Its private connection binding may override
   fallback environment values; see [MCP reference](../getting-started/mcp-reference.md).
4. Inspect the configured interpreter and paths. A package installed through
   `pip --user` in another interpreter does not repair the workspace `.venv`.

## Inspect a managed Compose deployment

Locate the generated environment selected in Setup. From that directory use the
actual `docker-compose.generated.yml` rather than a different `docker-compose.yml`:

```bash
docker compose -f docker-compose.generated.yml ps
docker compose -f docker-compose.generated.yml logs --tail=200 --no-color spx-server
```

For project-owned Compose use your project's actual file instead. Check whether
keys come from its environment or generated configuration before changing them.
Never attach an unsanitized generated Compose file to a public issue.

## Model rejected or unknown class

Check the model versus system-definition shape, registered class names and
extension import paths. Run repository validation in a public checkout; for live
MCP work validate/register through its tools. A 422 is usually a definition or
request error; preserve its exact diagnostic with secrets removed.

## Clock or values do not match expectations

Use the [verified client loop](../simulation-and-modeling/using-spx-python.md).
Set `real_time=False`, prepare outside the loop, use the timer property setter,
and account for the first cycle after an absolute time write. Runtime paused
single-step remains PAUSED. Snapshot import restores defaults and structure;
reapply runtime fixtures. Internal writes clear external overrides.

## Protocol unavailable

Use the [capability matrix](../spx-core/communications/capabilities.md) before
changing ports or installing packages. Confirm role, transport, backend, host
mappings, identifiers and SUT. Container localhost differs from host localhost.
BLE needs the separate compatible host service/radio; Matter needs its controller.
A protocol block appearing in the tree does not prove external read/write works.

If unresolved, follow [How to Get Support](how-to-get-support.md).
