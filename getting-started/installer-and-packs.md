---
description: Install the released SPX bundle, select packs, and use public models independently.
icon: package
---

# Installer and packs

Start with the [Installation Guide](installation-guide.md). Download the released
Windows EXE, macOS PKG or portable TGZ through [staging Downloads](https://staging.simplephysx.com/downloads),
then run **SPX Setup**. Select the pack or protocols, whether to include models
and starter instances, UI, and whether to start the environment immediately.

## Who owns what

| Repository | Responsibility | Access |
| --- | --- | --- |
| `spx-installer` | Product/MCP installation, Python preparation, client configuration, service assets, packaging, signing, release publication | Private |
| [spx-examples](https://github.com/HammerHeads-Engineers/spx-examples) | Models, catalogs, profiles, examples, runtime MCP modules and agent instructions | Public |
| [spx-docs](https://github.com/HammerHeads-Engineers/spx-docs) | Canonical product documentation and generated public catalog | Public |

The installer pins a committed public Examples context in `examples-source.json`.
Packaging stages that content before building the installers. A public checkout
can move independently; updating it does not update an installed bundle or its
server/UI images. See [Release Notes](../release-notes.md) for the coherent RC baseline.

## Select a pack

| Pack | Typical profile | Focus |
| --- | --- | --- |
| `smart_building_pack` | `bms_quickstart` | Building control, weather and energy |
| `energy_pack` | `ev_csms_demo` | EV charging and energy |
| `embedded_lab_pack` | `scpi_lab`, `mhealth_ci` | Instruments and embedded devices |
| `industrial_iiot_pack` | `process_cell_quickstart`, `iiot_monitoring`, `modbus_master_plc_demo` | Process and industrial control |

Available models are listed in the [public device catalog](../usage-scenarios-and-examples/device-catalog.md).
The installed selection depends on its pinned snapshot, chosen profile and license.
Protocol-only setup does not automatically create model instances. Selecting a
large pack can use a smaller starter instance set; enabling every catalog model
is a separate choice.

## Work with the installed environment

Use **SPX Start** and **SPX Stop**, or the generated start/stop helpers in the
installation's environment directory. Run Compose diagnostics from that directory:

```bash
docker compose -f docker-compose.generated.yml --env-file .env ps
curl -fsS http://localhost:8000/health
```

Default local endpoints are UI `http://localhost:3000`, API
`http://localhost:8000`, and API documentation `http://localhost:8000/docs`.
Keep the product key private. Use SPX Setup to change the installed configuration.
Use **SPX MCP Setup** for client provisioning and repairs; see
[Connect an LLM](connect-llm-with-spx-mcp.md).

## Work with public examples independently

Clone `spx-examples`, install its Poetry dependencies and follow `AGENTS.md`.
Point its MCP runtime or scripts at an already running SPX Server. It contains
no product installer CLI, native packages or product Compose bundle.
For a server-only container, follow [Manual Docker Compose](manual-docker-compose.md).

## Maintainer and CI use

The private installer contains `python -m installer generate` and service assets.
Those commands require an authorized private checkout; they cannot be run from
the public Examples repository. Public model changes follow the Examples
catalog/pack validation workflow. A maintainer then updates the installer's
public context pin, validates the selected pack and publishes a new installer.
Never expose private repository tokens to public documentation or Examples CI.

## Removal

Stop the installed environment first, then use its cleanup/uninstall launcher.
Removing Compose volumes deletes persisted state; export needed snapshots first.
