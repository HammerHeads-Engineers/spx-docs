---
description: >-
  Use the spx-examples installer to assemble a ready-to-run bundle of models,
  services, packs, default instances, and optional UI.
icon: package
---

# Installer and packs (spx-examples)

This is an advanced reference for users who need to customize generated
bundles, profiles, supporting services, or automation flows. For a first local
installation, start with the [Installation Guide](installation-guide.md) and run
the native `SPX Setup` wizard.

Use the `spx-examples` installer when you want a complete, ready-to-run bundle:
selected models, supporting services (MQTT, BACnet, KNX, OPC UA, Modbus, SCPI,
Home Assistant, etc.), and optional SPX UI.

Source of truth:
https://github.com/HammerHeads-Engineers/spx-examples

This page is aligned with `spx-examples` `origin/develop` at
`518d631ed9649810445ac9f0c5474ecd22880167` (`1.1.0-rc.48`). At that snapshot,
generated bundles use `simplephysx/spx-server:v1.0.0-rc.64` and
`simplephysx/spx-ui:v1.0.0-rc.68`.

## Golden path (Smart Building Pack)

Prerequisites:

- macOS, Linux, or Windows (PowerShell or `pwsh`)
- Docker and Docker Compose v2 (`docker compose`)
- Python 3.9+
- A valid `SPX_PRODUCT_KEY`

1. Clone `spx-examples`:

   ```bash
   git clone https://github.com/HammerHeads-Engineers/spx-examples.git
   cd spx-examples
   ```

2. Set `SPX_PRODUCT_KEY`:

   macOS/Linux:

   ```bash
   export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
   ```

   Windows PowerShell:

   ```powershell
   $env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
   ```

3. Generate the Smart Building quickstart bundle:

   ```bash
   python -m installer generate \
     --packages smart_building_pack \
     --profile-ids bms_quickstart \
     --with-ui \
     --output build/spx-generated
   ```

4. Enter the generated folder:

   ```bash
   cd build/spx-generated
   ```

5. Start the stack:

   macOS/Linux:

   ```bash
   ./spx-start.sh
   ```

   Windows PowerShell:

   ```powershell
   pwsh ./spx-start.ps1
   ```

6. Verify:

   ```bash
   docker compose -f docker-compose.generated.yml --env-file .env ps
   curl -fsS http://localhost:8000/health
   ```

   Success criteria:

   - `curl` returns JSON with `"status":"ok"`.
   - `docker compose ps` shows the selected services running.
   - If `--with-ui` was used, SPX UI opens at `http://localhost:3000`.

After installing Smart Building Pack, see
[Smart Building Pack: First Run Walkthrough](first-run-smart-building-pack.md).

## Prerequisites

- Docker and Docker Compose v2 (`docker compose`)
- Python 3.9+ with pip (installer requirement in `spx-examples` `pyproject.toml`)
- Tests and local tooling in `spx-examples` are exercised on Python 3.9-3.12 in CI
- A valid SPX product key (`SPX_PRODUCT_KEY`)

Optional:

- Node.js + npm if you include BLE models. The Bash start script can install or
  update `@simplephysx/spx-ble-adapter` when BLE services are selected.

Common environment variables:

| Variable | Purpose | Example |
| --- | --- | --- |
| `SPX_PRODUCT_KEY` | Auth key for SPX API and installer/bootstrap. | `SPX_PRODUCT_KEY=your-product-key` |
| `SPX_BASE_URL` | Override SPX API base URL for client scripts and tests. | `SPX_BASE_URL=http://localhost:8000` |

## Run the interactive wizard from the repo

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
```

Start the wizard:

- macOS/Linux: `./spx-install.sh`
- Windows PowerShell: `pwsh ./spx-install.ps1`

By default, artifacts are generated under `build/spx-generated/`.

Current wizard flow:

- `Enter package numbers (comma-separated, ENTER for default protocols, 0 for protocols, q to quit):`
- `Add models from selected packages? [Y/n]:` (shown only when packages are selected)
- `Add default instances? [y/N]:` (shown only when models are enabled)
- `Include SPX UI frontend container? [Y/n]:`
- `Start the stack immediately after generation? [Y/n]:`
- Product key prompt

If you press `ENTER` at the package selection prompt, the wizard chooses the
default protocol set (`Modbus + SCPI/ASCII` when available), skips model and
instance prompts, keeps SPX UI enabled, and starts the stack by default.

If you select `smart_building_pack`, `industrial_iiot_pack`, or
`embedded_lab_pack` and opt into default instances, the installer narrows the
generated instances to the pack's starter set. This keeps first-run stacks small
enough for the default licensing path.

## Non-interactive generation

Use pack and profile selectors to build bundles without prompts.

Smart Building with UI:

```bash
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui \
  --output build/spx-generated
```

Embedded Lab SCPI bundle without UI:

```bash
python -m installer generate \
  --packages embedded_lab_pack \
  --profile-ids scpi_lab \
  --no-ui \
  --output build/spx-generated
```

Other useful flags:

- `--protocols mqtt,modbus,http` filters by protocol.
- `--with-examples` enables bootstrap runner in generated start scripts (default
  in non-interactive mode).
- `--no-examples` skips model and instance bootstrap in start scripts.
- `--no-ui` or `--with-ui` controls the SPX UI container.
- `--allow-missing-product-key` writes `SPX_PRODUCT_KEY=REPLACE_ME` into `.env`.
- `--start` starts the generated stack immediately.
- `--no-start` generates artifacts without prompting to start.
- `--print-selection json` prints resolved packages, models, services, and
  starter instances for CI/debugging.

## What gets generated

Inside the output folder, for example `build/spx-generated/`:

- `docker-compose.generated.yml`: compose file with only the selected services
- `.env`: product key value or `SPX_PRODUCT_KEY=REPLACE_ME`
- `bundle.json`: selected packages, models, services, and instances consumed by bootstrap
- `bootstrap_runner.py` and `runtime_bootstrap.py`
- `spx-start.sh` / `spx-stop.sh`: start/stop helpers for Bash or zsh
- `spx-start.ps1` / `spx-stop.ps1`: start/stop helpers for PowerShell
- `spx-start.command`, `spx-stop.command`, `spx-start.bat`, `spx-stop.bat`: convenience launchers
- `assets/`: copied service configs, including MQTT, KNX, Home Assistant, Matter
- `extensions/`: copied custom Python extensions
- `library/`: selected model YAMLs copied into the bundle for self-contained sharing

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
- prepare a local runtime Python environment,
- install missing runtime modules such as `requests` and `spx-python`,
- optionally prepare the BLE adapter if BLE services are selected,
- run `docker compose down --remove-orphans` and then `docker compose up -d`,
- bootstrap models and instances from `bundle.json` when examples are enabled.

## Current packs and profiles

| Pack ID | Focus | Profiles |
| --- | --- | --- |
| `smart_building_pack` | BMS/BAS demo stack across MQTT, LwM2M/CoAP, HTTP, Modbus, OPC UA, KNX, Matter, BACnet, Home Assistant | `bms_quickstart` |
| `energy_pack` | e-mobility, OCPP, DER, and energy telemetry | `ev_csms_demo` |
| `embedded_lab_pack` | BLE, MQTT/LwM2M, SCPI, Modbus, and lab instruments | `mhealth_ci`, `scpi_lab` |
| `industrial_iiot_pack` | process, motion, IO, MQTT, Modbus, SCPI, HTTP, OPC UA | `process_cell_quickstart`, `iiot_monitoring`, `modbus_master_plc_demo` |

For deeper pack/model counts, see
[Industry packs and profiles](../usage-scenarios-and-examples/industry-packs.md).

## Security and CI notes

- Do not commit `.env` files containing `SPX_PRODUCT_KEY`.
- Use CI secrets to inject `SPX_PRODUCT_KEY` and `SPX_BASE_URL`.
- Share bundles with `SPX_PRODUCT_KEY=REPLACE_ME` or remove `.env` before sharing.
- Avoid putting keys into command history; prefer environment variables.

## How to verify

Integrator:

- `curl -fsS http://localhost:8000/health`
- `docker compose -f docker-compose.generated.yml --env-file .env ps`
- Confirm your selected protocol ports are exposed.

QA/CI:

- `python -m installer generate --packages <pack> --output build/ci/<pack> --allow-missing-product-key --no-start`
- `build/ci/<pack>/spx-start.sh`
- `curl -fsS http://localhost:8000/health`

Developer:

- Update `library/catalog/*.yaml` and `profiles/<pack>/*.yaml`.
- Regenerate with `python -m installer generate --packages <pack> --output build/spx-generated`.

## Cleanup and uninstall

- Stop containers: `./spx-stop.sh` or `pwsh ./spx-stop.ps1`
- Remove containers and volumes:

  ```bash
  docker compose -f docker-compose.generated.yml --env-file .env down -v
  ```

- Remove generated files: delete the generated folder, for example `build/spx-generated`
- Remove BLE adapter if installed globally: `npm uninstall -g @simplephysx/spx-ble-adapter`
