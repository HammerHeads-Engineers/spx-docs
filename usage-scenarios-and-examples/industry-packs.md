---
description: >-
  How industry packs and quickstart profiles in spx-examples map to installer
  selections.
icon: boxes-stacked
---

# Industry packs and profiles (spx-examples)

Industry packs are curated bundles of models, services, and quickstart profiles
grouped around a domain: smart buildings, energy, labs, and industrial IIoT.
Packs are defined in `spx-examples` and used by the installer to generate
ready-to-run bundles.

Source of truth:
https://github.com/HammerHeads-Engineers/spx-examples

Current snapshot used for pack/model counts:

- `spx-examples` `origin/develop` @ `518d631ed9649810445ac9f0c5474ecd22880167`
- Commit date: `2026-05-16`
- `spx-examples` version: `1.1.0-rc.48`

## Current catalog summary

Total model entries in `library/catalog/models.yaml`: **97**

### By pack

| Pack ID | Model entries | Default instances | Starter instances |
| --- | ---: | ---: | ---: |
| `smart_building_pack` | 39 | 33 | 5 |
| `energy_pack` | 7 | 5 | 0 |
| `embedded_lab_pack` | 32 | 9 | 5 |
| `industrial_iiot_pack` | 31 | 28 | 6 |

### By domain

| Domain | Model entries |
| --- | ---: |
| `building` | 15 |
| `energy` | 25 |
| `environment` | 5 |
| `industrial` | 22 |
| `lab` | 30 |

### By protocol tag

| Protocol | Model entries |
| --- | ---: |
| `bacnet` | 3 |
| `ble` | 2 |
| `coap` | 1 |
| `http` | 3 |
| `knx` | 5 |
| `lwm2m` | 1 |
| `matter` | 2 |
| `modbus` | 40 |
| `mqtt` | 8 |
| `ocpp` | 2 |
| `opcua` | 6 |
| `scpi` | 21 |

## Definitions

- Pack: an industry bundle of models and services.
- Profile: a concrete preset used for a specific scenario, demo, or CI run.
- Starter instances: the subset of default instances the installer starts when
  default instance generation is enabled for large packs.

## Pack overview

| Pack ID | Focus | Protocols and services | Profiles |
| --- | --- | --- | --- |
| `smart_building_pack` | BMS/BAS demo stack | Protocols: mqtt, lwm2m/coap, http, modbus, opcua, knx, matter, bacnet<br>Services: mqtt_broker, lwm2m_server, modbus_tcp_gateway, http_gateway, knx_gateway, homeassistant_bridge, matter_server, opcua_server, bacnet_gateway | [`bms_quickstart`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/smart_building_pack/bms_quickstart.yaml) |
| `energy_pack` | e-mobility and DER | Protocols: mqtt, modbus, ocpp<br>Services: mqtt_broker, modbus_tcp_gateway, ocpp_central_system | [`ev_csms_demo`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/energy_pack/ev_csms_demo.yaml) |
| `embedded_lab_pack` | BLE and lab instruments | Protocols: ble, mqtt, lwm2m/coap, scpi, modbus<br>Services: btvirt_adapter, mqtt_broker, lwm2m_server, scpi_tcp_stack, modbus_tcp_gateway | [`mhealth_ci`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/embedded_lab_pack/mhealth_ci.yaml), [`scpi_lab`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/embedded_lab_pack/scpi_lab.yaml) |
| `industrial_iiot_pack` | industrial process, motion, IO, monitoring | Protocols: modbus, mqtt, http, scpi, opcua<br>Services: modbus_tcp_gateway, mqtt_broker, http_gateway, scpi_tcp_stack, opcua_server | [`process_cell_quickstart`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/industrial_iiot_pack/process_cell_quickstart.yaml), [`iiot_monitoring`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/industrial_iiot_pack/iiot_monitoring.yaml), [`modbus_master_plc_demo`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/industrial_iiot_pack/modbus_master_plc_demo.yaml) |

## Starter instance sets

Smart Building Pack starts these 5 instances when you opt into default instance
generation:

- `HVAC_Flexit_Nordic_BACnet`
- `Energy_Meter_iEM3000_Modbus`
- `Victron_Cerbo_GX_ESS_Modbus`
- `Weather_Gateway_WAGO_PFC200_Vaisala_WXT530_MQTT`
- `Building_Physics`

Embedded Lab Pack starts:

- `spx_health_monitor_ble`
- `spx_temp_sensor_ble`
- `spx_env_sensor_mqtt`
- `spx_lab_multimeter`
- `spx_vacuum_gauge`

Industrial IIoT Pack starts:

- `spx_eurotherm_3216_temp`
- `spx_eurotherm_3504_pressure`
- `spx_g120c_vfd`
- `spx_altivar_320_vfd`
- `spx_wago_750_8000_io`
- `spx_s7_1500_process_cell`

Energy Pack currently defines default instances but no dedicated
`start_instances` subset.

## Examples

Smart Building quickstart bundle:

```bash
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui \
  --output build/spx-generated
```

Lab-only bundle for SCPI + Modbus:

```bash
python -m installer generate \
  --packages embedded_lab_pack \
  --profile-ids scpi_lab \
  --no-ui \
  --output build/spx-generated
```

Industrial Modbus master PLC demo:

```bash
python -m installer generate \
  --packages industrial_iiot_pack \
  --profile-ids modbus_master_plc_demo \
  --no-ui \
  --output build/spx-generated
```

For pack-specific details, see:

- `library/industries/<pack>/README.md`
- `library/industries/<pack>/MODELS.yaml`
- `profiles/<pack>/*.yaml`

## How packs and profiles map to the installer

For maintainers and developers, the installer builds its selection from:

- `library/catalog/industries.yaml` (pack metadata, default instances, start instances)
- `library/catalog/models.yaml` (model catalog, `packages`, `profiles`, `domain`, `device_class`, `vendor`)
- `library/catalog/services.yaml` (service definitions and port mappings)
- `profiles/<pack>/<profile>.yaml` (model and service list for a quickstart)

Selecting a pack:

- Includes models tagged with that pack in `models.yaml`.
- Adds services declared in the pack entry in `industries.yaml`.
- Can create default instances if you answer `yes` to `Add default instances? [y/N]:`.
- Narrows default instances to starter instances for large packs when starter
  lists are defined.

Selecting a profile:

- Adds models and services listed in the profile YAML.
- Can be combined with a pack selection or used on its own.

## How to verify

Integrator:

- Pick a pack and profile, generate a bundle, then run `spx-start`.
- Verify `curl -fsS http://localhost:8000/health`.
- Connect a client to one selected protocol.

QA/CI:

- `python -m installer generate --packages <pack> --output build/ci/<pack> --allow-missing-product-key --no-start`
- `build/ci/<pack>/spx-start.sh`
- `poetry run pytest -q tests/packs/<pack>`

Developer:

- Update `library/catalog/*.yaml` and `profiles/<pack>/*.yaml`.
- Regenerate with `python -m installer generate --packages <pack> --output build/spx-generated`.
- Update generated pack indexes with `python tools/render_pack_indexes.py`.

## Extending a pack

To extend or create a pack in `spx-examples`:

1. Add or update the model entry in `library/catalog/models.yaml` with `packages`, `profiles`, `domain`, `device_class`, and `vendor`.
2. Update `profiles/<pack>/<profile>.yaml` to include the model and services.
3. Update `library/catalog/industries.yaml` with default and starter instances if needed.
4. Regenerate `library/industries/<pack>/MODELS.yaml`.
5. Document pack-specific behavior in `library/industries/<pack>/README.md`.
