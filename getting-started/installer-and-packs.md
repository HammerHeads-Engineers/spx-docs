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

## Golden path (6 steps)

Prerequisites:

- macOS, Linux, or Windows (PowerShell or pwsh)
- Docker and Docker Compose v2 (`docker compose`)
- Python 3.9+

1. Clone spx-examples:

   ```bash
   git clone https://github.com/HammerHeads-Engineers/spx-examples.git
   cd spx-examples
   ```

2. Set `SPX_PRODUCT_KEY` (treat it as a secret; use env/CI secrets and never commit it):

   ```bash
   export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
   ```

   ```powershell
   $env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
   ```

3. Generate a bundle (canonical command):

   ```bash
   python -m installer generate \
     --packages smart_building_pack \
     --profile-ids bms_quickstart \
     --with-ui \
     --output build/spx-generated
   ```

4. Enter the output folder:

   ```bash
   cd build/spx-generated
   ```

5. Start the stack (script or docker compose):

   - macOS/Linux: `./spx-start.sh`
   - Windows: `pwsh ./spx-start.ps1`
   - Or: `docker compose -f docker-compose.generated.yml --env-file .env up -d`

6. Verify it is healthy:

   ```bash
   docker compose -f docker-compose.generated.yml --env-file .env ps
   curl -fsS http://localhost:8000/health
   ```

   Success criteria:
   - `curl` returns JSON with `"status":"ok"`.
   - `docker compose ps` shows `spx-server` as `Up` (healthy).

## Prerequisites

- Docker and Docker Compose v2 (`docker compose`)
- Python 3.9+ with pip (installer requirement in spx-examples `pyproject.toml`)
- Tests and local tooling in spx-examples are exercised on Python 3.9-3.12 in CI
  (pack tests run on Python 3.10.14)
- A valid SPX product key (`SPX_PRODUCT_KEY`)

Optional:

- Node.js + npm if you include BLE models (the start script installs `@simplephysx/spx-ble-adapter`).

## Run the installer from the repo (interactive wizard)

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
```

Start the wizard:

- macOS/Linux: `./spx-install.sh`
- Windows (PowerShell): `pwsh ./spx-install.ps1`

By default, artifacts are generated under `build/spx-generated/`.

## Non-interactive generation

Use pack and profile selectors to build bundles without prompts. Example:

```bash
python -m installer generate \
  --packages embedded_lab_pack \
  --profile-ids scpi_lab \
  --no-ui \
  --start \
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

- `docker-compose.generated.yml`: compose file with only the selected services.
- `.env`: product key placeholder (`SPX_PRODUCT_KEY=REPLACE_ME`) for this bundle.
- `bundle.json`: selected packages, models, services, and instances; consumed by the
  bootstrap runner to register models and create instances.
- `bootstrap_runner.py`: lightweight bootstrap script invoked by `spx-start`.
- `spx-start.sh` / `spx-stop.sh`: start/stop helpers for Bash or zsh.
- `spx-start.ps1` / `spx-stop.ps1`: start/stop helpers for PowerShell.
- `assets/`: copied service configs (MQTT, KNX, Home Assistant, Matter).
- `extensions/`: copied custom Python extensions.
- `library/`: selected model YAMLs copied into the bundle for self-contained sharing.

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

## Security and CI notes

- Do not commit `.env` files containing `SPX_PRODUCT_KEY`.
- Use CI secrets to inject `SPX_PRODUCT_KEY` and `SPX_BASE_URL`.
- Share bundles with `SPX_PRODUCT_KEY=REPLACE_ME` (or remove `.env` before sharing).
- Avoid putting keys into command history; prefer environment variables.

## How to verify (Integrator / QA / Developer)

Integrator:

- `curl -fsS http://localhost:8000/health`
- `docker compose -f docker-compose.generated.yml --env-file .env ps`
- Confirm your target protocol port is listening (for example Modbus on `5020-5120`).

QA/CI:

- `python -m installer generate --packages <pack> --output build/ci/<pack> --no-start`
- `build/ci/<pack>/spx-start.sh`
- `curl -fsS http://localhost:8000/health`

Developer:

- Update `library/catalog/*.yaml` and `profiles/<pack>/*.yaml`, then regenerate:
  `python -m installer generate --packages <pack> --output build/spx-generated`

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
