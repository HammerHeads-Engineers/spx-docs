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

## Definitions

- Pack: an industry bundle of models and services (broad scope).
- Profile: a concrete preset used for a specific scenario, demo, or CI run.

## Pack overview

| Pack ID | Focus | Protocols/Services | Profiles |
| --- | --- | --- | --- |
| `smart_building_pack` | BMS/BAS demo stack | Protocols: mqtt, lwm2m/coap, http, modbus, opcua, knx, matter, bacnet<br>Services: mqtt_broker, lwm2m_server, modbus_tcp_gateway, http_gateway, opcua_server, knx_gateway, bacnet_gateway, homeassistant_bridge, matter_server | [`bms_quickstart`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/smart_building_pack/bms_quickstart.yaml) |
| `energy_pack` | e-mobility and DER | Protocols: http, mqtt, modbus, ocpp<br>Services: mqtt_broker, modbus_tcp_gateway, http_gateway, ocpp_central_system | [`ev_csms_demo`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/energy_pack/ev_csms_demo.yaml) |
| `embedded_lab_pack` | BLE and lab instruments | Protocols: ble, mqtt, lwm2m/coap, scpi, modbus<br>Services: btvirt_adapter, mqtt_broker, lwm2m_server, scpi_tcp_stack, modbus_tcp_gateway | [`mhealth_ci`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/embedded_lab_pack/mhealth_ci.yaml), [`scpi_lab`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/embedded_lab_pack/scpi_lab.yaml) |
| `industrial_iiot_pack` | industrial monitoring | Protocols: modbus, mqtt, http, scpi, opcua<br>Services: modbus_tcp_gateway, mqtt_broker, http_gateway, scpi_tcp_stack, opcua_server | [`process_cell_quickstart`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/industrial_iiot_pack/process_cell_quickstart.yaml), [`iiot_monitoring`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/profiles/industrial_iiot_pack/iiot_monitoring.yaml) |

For pack-specific details, see:

- `library/industries/<pack>/README.md`
- `profiles/<pack>/*.yaml`

## How packs and profiles map to the installer

For maintainers and developers, the installer builds its selection from:

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

## How to verify (by role)

- Integrator:
  - Pick a pack and profile, generate a bundle, then run `spx-start`.
  - Verify `curl -fsS http://localhost:8000/health` and connect a client to one selected protocol.
- QA/CI:
  - `python -m installer generate --packages <pack> --output build/ci/<pack> --no-start`
  - `build/ci/<pack>/spx-start.sh`
  - `poetry run pytest -q tests/packs/<pack>`
- Developer:
  - Update `library/catalog/*.yaml` and `profiles/<pack>/*.yaml`, then regenerate with
    `python -m installer generate --packages <pack> --output build/spx-generated`.

## Extending a pack (for contributors)

To extend or create a pack in spx-examples:

1. Add or update the model entry in `library/catalog/models.yaml` with `packages` and `profiles`.
2. Update `profiles/<pack>/<profile>.yaml` to include the model and services.
3. Update `library/catalog/industries.yaml` with default and start instances (if needed).
4. Document the changes in `library/industries/<pack>/README.md`.
