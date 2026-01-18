---
description: >-
  How industry packs and quickstart profiles in spx-examples map to installer
  selections.
icon: boxes-stacked
---

# Industry packs and profiles (spx-examples)

Industry packs are curated bundles of models, services, and quickstart profiles
grouped around a domain (smart buildings, energy, labs, industrial IIoT). Packs
are defined in spx-examples and used by the installer to generate ready-to-run
bundles.

Source of truth (public repo):
https://github.com/HammerHeads-Engineers/spx-examples

## Pack overview

| Pack ID | Focus | Protocols (high level) | Quickstart profiles |
| --- | --- | --- | --- |
| `smart_building_pack` | BMS/BAS demo stack | mqtt, lwm2m/coap, http, modbus, opcua, knx, matter, bacnet | `bms_quickstart` |
| `energy_pack` | e-mobility and DER | http, mqtt, modbus, ocpp | `ev_csms_demo` |
| `embedded_lab_pack` | BLE and lab instruments | ble, mqtt, lwm2m/coap, scpi, modbus | `mhealth_ci`, `scpi_lab` |
| `industrial_iiot_pack` | industrial monitoring | modbus, mqtt, http, scpi, opcua | `process_cell_quickstart`, `iiot_monitoring` |

For pack-specific details, see:

- `library/industries/<pack>/README.md`
- `profiles/<pack>/*.yaml`

## How packs and profiles map to the installer

The installer builds its selection from:

- `library/catalog/industries.yaml` (pack metadata, default instances, start instances)
- `library/catalog/models.yaml` (model catalog, `packages` and `profiles` tags)
- `library/catalog/services.yaml` (service definitions and port mappings)
- `profiles/<pack>/<profile>.yaml` (model + service list for a quickstart)

Selecting a pack:

- Includes all models tagged with that pack in `models.yaml`.
- Adds services declared in the pack entry in `industries.yaml`.
- Optionally creates and starts default instances listed in `industries.yaml`.

Selecting a profile:

- Adds models and services listed in the profile YAML.
- Can be combined with a pack selection or used on its own.

## Examples

Generate a smart-building quickstart bundle:

```bash
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui
```

Generate a lab-only bundle for SCPI + Modbus:

```bash
python -m installer generate \
  --packages embedded_lab_pack \
  --profile-ids scpi_lab \
  --no-ui
```

## Extending a pack (for contributors)

To extend or create a pack in spx-examples:

1. Add or update the model entry in `library/catalog/models.yaml` with `packages` and `profiles`.
2. Update `profiles/<pack>/<profile>.yaml` to include the model and services.
3. Update `library/catalog/industries.yaml` with default and start instances (if needed).
4. Document the changes in `library/industries/<pack>/README.md`.
