---
description: >-
  Use the spx-examples installer to assemble a ready-to-run bundle of models,
  services, and optional UI.
icon: package
---

# Installer and packs (spx-examples)

Use the spx-examples installer when you want a complete, ready-to-run bundle:
selected models, supporting services (MQTT, BACnet, KNX, etc.), and optional UI.
The installer generates a self-contained folder you can share with teammates.

The installer lives in the public spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples

## Prerequisites

- Docker and Docker Compose v2 (`docker compose`)
- Python 3.9+ with pip
- A valid SPX product key (`SPX_PRODUCT_KEY`)

Optional:

- Node.js + npm if you include BLE models (the start script installs `@simplephysx/spx-ble-adapter`).

## Run the installer from the repo

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
```

Start the wizard:

- macOS/Linux: `./spx-install.sh`
- Windows (PowerShell): `pwsh ./spx-install.ps1`

By default, artifacts are generated under `build/spx-generated/`.

## Non-interactive generation

Use pack and profile selectors to build bundles without prompts:

```bash
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui \
  --output build/spx-generated
```

Other useful flags:

- `--protocols mqtt,modbus,http` (filter by protocols)
- `--no-examples` (skip model/instance bootstrap in start scripts)
- `--no-ui` or `--with-ui`
- `--allow-missing-product-key` (writes `REPLACE_ME` into `.env`)
- `--start` (launch after generating)

## What gets generated

Inside the output folder (for example `build/spx-generated/`):

- `docker-compose.generated.yml` with only the selected services.
- `.env` with `SPX_PRODUCT_KEY=REPLACE_ME` (edit to a real key).
- `bundle.json` describing selected packages, models, services, and instances.
- `spx-start.sh` / `spx-stop.sh` and `spx-start.ps1` / `spx-stop.ps1`.
- `assets/` and `extensions/` copied from the repo.
- Selected model YAMLs copied into the bundle so it is self-contained.

## Start and stop the stack

From the generated folder:

- Start:
  - macOS/Linux: `./spx-start.sh`
  - Windows: `pwsh ./spx-start.ps1`
- Stop:
  - macOS/Linux: `./spx-stop.sh`
  - Windows: `pwsh ./spx-stop.ps1`

The start scripts:

- verify `docker` and Python,
- install missing Python modules (`requests`, `spx-python`),
- optionally install and run the BLE adapter if BLE services are selected,
- run `docker compose down --remove-orphans` and then `docker compose up -d`,
- bootstrap models and instances from `bundle.json`.

## Cleanup and uninstall

- Stop containers: `./spx-stop.sh` or `pwsh ./spx-stop.ps1`
- Remove containers and volumes: `docker compose -f docker-compose.generated.yml --env-file .env down -v`
- Remove generated files: delete the generated folder (for example `build/spx-generated`)
- Remove BLE adapter (if installed): `npm uninstall -g @simplephysx/spx-ble-adapter`

## Build shareable installer packages (optional)

If you need a redistributable archive (no repo clone):

```bash
scripts/build_installer_package.sh
```

This creates `dist/spx-installer/` and `dist/spx-installer.tgz`.
Recipients extract and run `./spx-install.sh` or `pwsh ./spx-install.ps1`.

For single-file installers:

```bash
scripts/build_self_extractors.sh --version v1.2.3
```

Outputs:

- `dist/spx-installer-v1.2.3.run` (macOS/Linux)
- `dist/spx-installer-v1.2.3.ps1` (Windows)

## Packs and profiles

Packs and profiles define the model and service bundles available to the installer.
See: [Industry packs and profiles](../usage-scenarios-and-examples/industry-packs.md).
