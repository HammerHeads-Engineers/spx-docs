---
description: >-
  Understand the SPX Setup Wizard (spx-examples installer): packs/profiles,
  protocol-only installs, generated bundles, and automation options.
icon: package
---

# Installer Wizard & Packs (spx-examples)

The **SPX Setup Wizard** (launched via `spx-setup.*`) is the recommended way to
assemble a ready-to-run SPX environment: SPX Server, optional UI, selected
protocol gateways, and (optionally) example models/instances.

If you want the step-by-step install flow (download -> run -> verify), start
here: [Installation Guide](installation-guide.md).

## What the wizard does (high level)

1. Prompts you in the terminal to select **packs** or a **protocol-only** setup.
2. Generates a self-contained bundle (default: `build/spx-generated/`).
3. Offers to start the stack immediately.
4. If you enabled examples, bootstraps selected models/instances into the server.

## Wizard concepts (packs, profiles, protocols)

### Packs (industry bundles)

An **industry pack** groups models + supporting services for a domain (Smart
Building, Energy, Industrial, etc.). Selecting a pack typically gives you a
turnkey demo environment (models, instances, and the protocol services it needs).

For an overview of available packs/profiles, see:
[Industry Packs and Profiles](../usage-scenarios-and-examples/industry-packs.md).

### Profiles (quickstarts)

A **profile** is a curated pack-specific quickstart that adds extra services and
defaults (for example: a BMS quickstart profile inside Smart Building Pack).

### Protocol-only installs

If you choose **by protocols** (instead of selecting packs), the wizard can
generate a stack focused on protocol gateways (for example: Modbus + SCPI/ASCII)
without installing any pack models/instances.

This is useful when you want to bring up the UI + API quickly and then register
your own models later.

## What pressing ENTER does (the "basic install" behavior)

The wizard is designed so pressing **ENTER** keeps you on safe defaults. In
practice:

- On the first prompt, **ENTER** selects a **protocol-only** default (when
  available).
- **SPX UI** is enabled by default.
- The wizard will still ask for your **SPX product key** (copy/paste from
  Product & Keys).
- When asked to start the stack, **ENTER** chooses "Yes".

If you want a pack demo (models/instances preloaded), select a pack instead of
using the protocol-only default.

## What gets generated (bundle output)

By default, the wizard generates artifacts under:

- `build/spx-generated/`

Typical contents:

- `docker-compose.generated.yml` - Compose file containing only the selected services.
- `.env` - contains `SPX_PRODUCT_KEY=...` used by the stack.
- `bundle.json` - selection + model paths + default instances; used by the bootstrap runner.
- `bootstrap_runner.py` - registers models, creates instances, and optionally starts them.
- `spx-start.sh` / `spx-stop.sh` - start/stop helpers for Bash/zsh.
- `spx-start.ps1` / `spx-stop.ps1` - start/stop helpers for PowerShell.
- `spx-start.command` / `spx-stop.command` and `spx-start.bat` / `spx-stop.bat` - double-click launchers.
- `assets/` - copied service configs/assets referenced by selected services.
- `extensions/` - copied Python extensions (mounted into the SPX Server container).
- `library/` - selected model YAMLs copied into the bundle (for self-contained sharing).

### Security note (important)

The bundle contains your **product key** in:

- `build/spx-generated/.env`
- `build/spx-generated/bundle.json`

Before sharing the bundle with teammates, replace the key with `REPLACE_ME` (or
remove those files) and have each person inject their own key.

## Starting and stopping the stack (after generation)

From inside `build/spx-generated/`:

- Start:
  - macOS/Linux: `./spx-start.sh`
  - Windows: `pwsh ./spx-start.ps1`
- Stop:
  - macOS/Linux: `./spx-stop.sh`
  - Windows: `pwsh ./spx-stop.ps1`

The start scripts:

- verify `docker` and Python are available,
- install missing Python modules (`requests`, `spx-python`, `pyyaml`) via pip,
- if BLE services are selected, install/run the BLE adapter via npm,
- run `docker compose down --remove-orphans`, then `docker compose up -d`,
- run the bootstrap runner (only when examples/models were selected).

## Running the wizard (package vs repo)

### From the downloaded package (recommended)

Run the platform launcher from the extracted folder:

- macOS: `./spx-setup.command`
- Linux desktop: `./spx-setup.desktop`
- Windows: `spx-setup.bat`
- macOS/Linux shells: `./spx-setup.sh`

### From a cloned repo (advanced / contributor workflow)

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
./spx-setup.sh
```

On Windows:

```powershell
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
spx-setup.bat
```

### Run the installer engine directly (advanced)

If you need to bypass the launchers:

- Bash: `./spx-install.sh`
- PowerShell: `pwsh ./spx-install.ps1`

Both commands ultimately run `python -m installer generate ...`.

## Non-interactive generation (automation / CI)

Use selectors to build bundles without prompts. Example:

macOS/Linux:

```bash
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui \
  --output build/spx-generated \
  --start
```

Windows (PowerShell):

```powershell
$env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
python -m installer generate `
  --packages smart_building_pack `
  --profile-ids bms_quickstart `
  --with-ui `
  --output build\spx-generated `
  --start
```

Notes:

- In non-interactive mode, UI is **off by default** unless you pass `--with-ui`.
- Without `--start`, the command generates artifacts and exits (no prompt).

## Troubleshooting

If setup fails, see:

- [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)
