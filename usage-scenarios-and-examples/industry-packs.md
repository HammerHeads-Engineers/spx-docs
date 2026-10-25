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

## Catalog baseline

Model counts and pack membership are generated in the [Device Catalog](device-catalog.md)
from the exact public Examples revision recorded in `sources.json`. Use that
page for current counts instead of duplicating numbers here. The installer
RC115 baseline pins public Examples `be71a161e97eb7a112d0581136a7b702b34cd98a`;
new public models need a later installer context update before appearing in a
new packaged selection.

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

## Using the packs

Use [SPX Setup](../getting-started/installer-and-packs.md) to provision an installed
bundle. Public Examples holds `library/industries/<pack>/{README.md,MODELS.yaml}`
and `profiles/<pack>/*.yaml` for inspection and independent model development.
For the active controller walkthrough, see
[Modbus Client / PLC Controller](../getting-started/modbus-client-controller.md).

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

Model contributors run the public repository validator, relevant pack tests and
`tools/render_pack_indexes.py`. Installer maintainers separately generate and
validate bundles in the private installer repository. Integration tests require
a running stack, product key and the selected protocol services.

## Extending a pack

To extend or create a pack in `spx-examples`:

1. Add or update the model entry in `library/catalog/models.yaml` with `packages`, `profiles`, `domain`, `device_class`, and `vendor`.
2. Update `profiles/<pack>/<profile>.yaml` to include the model and services.
3. Update `library/catalog/industries.yaml` with default and starter instances if needed.
4. Regenerate `library/industries/<pack>/MODELS.yaml`.
5. Document pack-specific behavior in `library/industries/<pack>/README.md`.
