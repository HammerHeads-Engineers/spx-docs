---
description: >-
  Searchable catalog of device models available per installer pack, generated from spx-examples develop.
icon: list
---

# Device Catalog (spx-examples)

This page lists device models available in each installer pack.
Names and file names are aligned 1:1 with `spx-examples` so docs search can find exact device strings quickly.

> Important
> These are reference simulation models from `spx-examples`, not official digital twins certified by device manufacturers.
> They are not officially supported by manufacturers and we do not guarantee a 100% functional match to real hardware behavior.

Source snapshot: `spx-examples` commit `518d631ed9649810445ac9f0c5474ecd22880167` (2026-05-16T22:16:15+02:00)

Generated from: `scripts/generate_device_catalog.py`.

Grouping on this page: **Pack -> Domain -> Device Class -> Vendor**.

Snapshot summary:
- Model entries in `library/catalog/models.yaml`: **97**
- Domains in catalog: `building` (**15**), `energy` (**25**), `environment` (**5**), `industrial` (**22**), `lab` (**30**)
- Protocol tags in catalog: `bacnet` (**3**), `ble` (**2**), `coap` (**1**), `http` (**3**), `knx` (**5**), `lwm2m` (**1**), `matter` (**2**), `modbus` (**40**), `mqtt` (**8**), `ocpp` (**2**), `opcua` (**6**), `scpi` (**21**)

## Conventions

- `Device name`: official `name` from `library/catalog/models.yaml`.
- `Model file`: exact YAML file name used in the library.
- `Device Class`: official `device_class` from `library/catalog/models.yaml`.
- `Vendor`: official `vendor` from `library/catalog/models.yaml`.
- `Profiles`: only profiles that belong to the current pack.

## `smart_building_pack` - Smart-Building Pack (BMS)

Devices in pack: **39**

Pack profiles: `bms_quickstart`

### Domain: `building` - Building Systems

Device count in domain: **15**

#### Device Class: `actuator`

Device count in class: **4**

##### Vendor: `abb`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| ABB JRA/S 4.230.5.1 Cover Actuator (KNX) | [`abb_jra_s4_230_5_1__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/actuator/abb/abb_jra_s4_230_5_1__knx.yaml) | `Building.CoverActuator.AbbJraS4_230_5_1.Knx` | `knx` | `bms_quickstart` |
| ABB SA/S12.16.5.1 Switch Actuator (KNX) | [`abb_sa_s12_16_5_1__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/actuator/abb/abb_sa_s12_16_5_1__knx.yaml) | `Building.SwitchActuator.AbbSaS12_16_5_1.Knx` | `knx` | `bms_quickstart` |

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Generic Robot Vacuum (MQTT) | [`robot_vacuum__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/actuator/generic/robot_vacuum__mqtt.yaml) | `Building.RobotVacuum.Mqtt` | `mqtt` | - |
| Smart Plug / Relay (Matter) | [`smart_plug__matter.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/actuator/generic/smart_plug__matter.yaml) | `Building.SmartPlug.Matter` | `matter` | `bms_quickstart` |

#### Device Class: `controller`

Device count in class: **4**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| BMS Controller (OPC UA) | [`bms_controller__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/controller/generic/bms_controller__opcua.yaml) | `Building.BMSController.OpcUa` | `opcua` | `bms_quickstart` |
| Flexit Nordic HVAC (BACnet) | [`hvac_flexit_nordic__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/controller/generic/hvac_flexit_nordic__bacnet.yaml) | `Building.HvacFlexitNordic.Bacnet` | `bacnet` | `bms_quickstart` |
| Room Controller (KNX) | [`room_controller__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/controller/generic/room_controller__knx.yaml) | `Building.RoomController.Knx` | `knx` | `bms_quickstart` |
| Security Access Controller (BACnet) | [`security_access_controller__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/controller/generic/security_access_controller__bacnet.yaml) | `Building.SecurityAccessController.Bacnet` | `bacnet` | `bms_quickstart` |

#### Device Class: `gateway`

Device count in class: **1**

##### Vendor: `wago`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Utility Gateway (WAGO PFC200 + Water/Gas Pulse, MQTT Discovery) | [`utility_gateway_wago_pfc200__water_gas_pulse__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/gateway/wago/utility_gateway_wago_pfc200__water_gas_pulse__mqtt.yaml) | `Building.UtilityGateway.WagoPfc200.WaterGasPulse.Mqtt` | `mqtt` | `bms_quickstart` |

#### Device Class: `panel`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Fire Alarm Panel (BACnet) | [`fire_alarm_panel__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/panel/generic/fire_alarm_panel__bacnet.yaml) | `Building.FireAlarmPanel.Bacnet` | `bacnet` | `bms_quickstart` |
| Lighting Panel (OPC UA) | [`lighting_panel__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/panel/generic/lighting_panel__opcua.yaml) | `Building.LightingPanel.OpcUa` | `opcua` | `bms_quickstart` |

#### Device Class: `physics`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Building Physics | [`building_physics.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/physics/generic/building_physics.yaml) | `Building.Physics.Generic` | `-` | `bms_quickstart` |

#### Device Class: `sensor`

Device count in class: **1**

##### Vendor: `theben`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Presence Detector (Theben theRonda P360 KNX) | [`theronda_p360__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/sensor/theben/theronda_p360__knx.yaml) | `Building.PresenceDetector.ThebenP360.Knx` | `knx` | `bms_quickstart` |

#### Device Class: `thermostat`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Thermostat (Matter) | [`thermostat__matter.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/thermostat/generic/thermostat__matter.yaml) | `Building.Thermostat.Matter` | `matter` | `bms_quickstart` |

#### Device Class: `zone`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Lighting Zone (KNX) | [`lighting_zone__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/zone/generic/lighting_zone__knx.yaml) | `Building.LightingZone.Knx` | `knx` | `bms_quickstart` |

### Domain: `energy` - Energy & e-Mobility

Device count in domain: **17**

#### Device Class: `controller`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Building Energy Aggregator | [`building_energy_aggregator.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/controller/generic/building_energy_aggregator.yaml) | `Energy.BuildingEnergyAggregator.Generic` | `-` | `bms_quickstart` |

#### Device Class: `ess`

Device count in class: **1**

##### Vendor: `victron`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Victron Cerbo GX ESS (Modbus) | [`cerbo_gx_ess__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/ess/victron/cerbo_gx_ess__modbus.yaml) | `Energy.ESS.VictronCerboGx.Modbus` | `modbus` | `bms_quickstart` |

#### Device Class: `meter`

Device count in class: **11**

##### Vendor: `abb`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| ABB D13 15 Energy Meter (Modbus) | [`abb_d13_15__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/abb/abb_d13_15__modbus.yaml) | `Energy.EnergyMeterAbbD13_15.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `carlo_gavazzi`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Carlo Gavazzi EM24 Energy Meter (Modbus TCP) | [`carlo_gavazzi_em24__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/carlo_gavazzi/carlo_gavazzi_em24__modbus.yaml) | `Energy.EnergyMeterCarloGavazziEm24.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `eastron`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Eastron SDM630 Energy Meter (Modbus) | [`eastron_sdm630__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/eastron/eastron_sdm630__modbus.yaml) | `Energy.EnergyMeterEastronSdm630.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `eaton`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Eaton Power Xpert Meter 2000 (Modbus TCP) | [`eaton_pxm2000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/eaton/eaton_pxm2000__modbus.yaml) | `Energy.EnergyMeterEatonPxm2000.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `schneider`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Schneider Acti9 iEM3000 Energy Meter (Modbus) | [`energy_meter_iem3000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/energy_meter_iem3000__modbus.yaml) | `Energy.EnergyMeterIem3000.Modbus` | `modbus` | `bms_quickstart` |
| Schneider Electric EM4200 Energy Meter (Modbus) | [`schneider_em4200__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/schneider_em4200__modbus.yaml) | `Energy.EnergyMeterEm4200.Modbus` | `modbus` | `bms_quickstart` |
| Schneider Electric PowerLogic PM3200 Energy Meter (Modbus) | [`schneider_pm3200__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/schneider_pm3200__modbus.yaml) | `Energy.EnergyMeterPm3200.Modbus` | `modbus` | `bms_quickstart` |
| Schneider Electric PowerLogic PM5330 (Modbus) | [`schneider_pm5330__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/schneider_pm5330__modbus.yaml) | `Energy.EnergyMeterPm5330.Modbus` | `modbus` | `bms_quickstart` |
| Schneider Electric PowerLogic PM8000 (Modbus) | [`schneider_powerlogic_pm8000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/schneider_powerlogic_pm8000__modbus.yaml) | `Energy.EnergyMeterPm8000.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens SENTRON PAC3200 Energy Meter (Modbus) | [`siemens_pac3200__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/siemens/siemens_pac3200__modbus.yaml) | `Energy.EnergyMeterPac3200.Modbus` | `modbus` | `bms_quickstart` |

##### Vendor: `socomec`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Socomec DIRIS A-40 Energy Meter (Modbus TCP) | [`diris_a40__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/socomec/diris_a40__modbus.yaml) | `Energy.EnergyMeterDirisA40.Modbus` | `modbus` | `bms_quickstart` |

#### Device Class: `power_quality_analyzer`

Device count in class: **1**

##### Vendor: `janitza`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Janitza UMG 604-PRO Power Quality Analyzer (Modbus) | [`janitza_umg604_pro__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/power_quality_analyzer/janitza/janitza_umg604_pro__modbus.yaml) | `Energy.PowerQualityAnalyzerUmg604Pro.Modbus` | `modbus` | `bms_quickstart` |

#### Device Class: `pv`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| PV Physics from Lux | [`pv_physics_lux.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/pv/generic/pv_physics_lux.yaml) | `Energy.PvPhysics.GenericLux` | `-` | `bms_quickstart` |

#### Device Class: `rack_pdu`

Device count in class: **1**

##### Vendor: `apc`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| APC NetShelter Rack PDU RPDU2g (Modbus) | [`rack_pdu_rpdu2g__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/rack_pdu/apc/rack_pdu_rpdu2g__modbus.yaml) | `Energy.RackPdu.ApcNetShelter2g.Modbus` | `modbus` | `bms_quickstart` |

#### Device Class: `ups`

Device count in class: **1**

##### Vendor: `apc`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| APC Easy UPS 3M (Modbus) | [`apc_easy_ups_3m__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/ups/apc/apc_easy_ups_3m__modbus.yaml) | `Energy.UpsEasy3M.Modbus` | `modbus` | `bms_quickstart` |

### Domain: `environment` - Environment & Weather

Device count in domain: **5**

#### Device Class: `feed`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Weather Forecast Feed | [`weather_forecast__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/feed/generic/weather_forecast__http.yaml) | `Weather.WeatherFeed.Http` | `http` | `bms_quickstart` |

#### Device Class: `gateway`

Device count in class: **1**

##### Vendor: `wago_vaisala`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Weather Gateway (WAGO PFC200 + Vaisala WXT530, MQTT Discovery) | [`weather_gateway_wago_pfc200__vaisala_wxt530__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/gateway/wago_vaisala/weather_gateway_wago_pfc200__vaisala_wxt530__mqtt.yaml) | `Weather.WeatherGateway.WagoPfc200.VaisalaWxt530.Mqtt` | `mqtt` | `bms_quickstart` |

#### Device Class: `sensor`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| LwM2M Environment Sensor | [`environment_sensor__lwm2m.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__lwm2m.yaml) | `Env.EnvSensor.Lwm2m` | `lwm2m, coap` | `bms_quickstart` |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | `bms_quickstart` |

#### Device Class: `station`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Air Quality Station (HTTP) | [`air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/station/generic/air_quality_station__http.yaml) | `Env.AirQualityStation.Http` | `http` | `bms_quickstart` |

### Domain: `industrial` - Industrial Systems

Device count in domain: **2**

#### Device Class: `controller`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Thermal Controller (Advanced) | [`thermal_controller_advanced.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/thermal_controller_advanced.yaml) | `Process.ThermalController.Advanced` | `-` | `bms_quickstart` |
| Thermal Controller (Modbus) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/thermal_controller__modbus.yaml) | `Process.ThermalController.Modbus` | `modbus` | `bms_quickstart` |

## `energy_pack` - Energy Pack (e-Mobility & DER)

Devices in pack: **7**

Pack profiles: `ev_csms_demo`

### Domain: `energy` - Energy & e-Mobility

Device count in domain: **7**

#### Device Class: `csms`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| CSMS Control Simulator (OCPP 1.6) | [`csms__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/csms/generic/csms__ocpp.yaml) | `Energy.CSMS.Ocpp` | `ocpp` | `ev_csms_demo` |

#### Device Class: `evse`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| EVSE / Charge Point (OCPP 1.6) | [`evse__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/evse/generic/evse__ocpp.yaml) | `Energy.EVSE.Ocpp` | `ocpp` | `ev_csms_demo` |

##### Vendor: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens VersiCharge AC EVSE (Modbus TCP) | [`siemens_versicharge_ac__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/evse/siemens/siemens_versicharge_ac__modbus.yaml) | `Energy.EVSE.SiemensVersiChargeAc.Modbus` | `modbus` | `ev_csms_demo` |

#### Device Class: `meter`

Device count in class: **4**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| 3-Phase Energy Meter (Modbus) | [`energy_meter_3ph__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/generic/energy_meter_3ph__modbus.yaml) | `Energy.EnergyMeter3Ph.Modbus` | `modbus` | - |
| 3-Phase Energy Meter (MQTT) | [`energy_meter_3ph__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/generic/energy_meter_3ph__mqtt.yaml) | `Energy.EnergyMeter3Ph.Mqtt` | `mqtt` | - |

##### Vendor: `schneider`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Schneider Electric PowerLogic PM5560 (Modbus) | [`schneider_pm5560__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/schneider_pm5560__modbus.yaml) | `Energy.EnergyMeterPm5560.Modbus` | `modbus` | `ev_csms_demo` |

##### Vendor: `socomec`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Socomec DIRIS A-10 Energy Meter (Modbus) | [`diris_a10__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/socomec/diris_a10__modbus.yaml) | `Energy.EnergyMeterDirisA10.Modbus` | `modbus` | - |

## `embedded_lab_pack` - Embedded & Lab Pack

Devices in pack: **32**

Pack profiles: `mhealth_ci`, `scpi_lab`

### Domain: `environment` - Environment & Weather

Device count in domain: **2**

#### Device Class: `sensor`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| LwM2M Environment Sensor | [`environment_sensor__lwm2m.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__lwm2m.yaml) | `Env.EnvSensor.Lwm2m` | `lwm2m, coap` | - |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | - |

### Domain: `industrial` - Industrial Systems

Device count in domain: **1**

#### Device Class: `sensor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Vacuum Gauge (Modbus) | [`vacuum_gauge__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/sensor/generic/vacuum_gauge__modbus.yaml) | `Process.VacuumGauge.Modbus` | `modbus` | `scpi_lab` |

### Domain: `lab` - Lab & Embedded

Device count in domain: **29**

#### Device Class: `controller`

Device count in class: **1**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac BCU14 Bakeout Controller (Modbus) | [`prevac_bcu14__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/controller/prevac/prevac_bcu14__modbus.yaml) | `Process.ThermalController.PrevacBcu14.Modbus` | `modbus` | `scpi_lab` |

#### Device Class: `detector`

Device count in class: **1**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac MCD7 Multichanneltron Detector (Modbus) | [`prevac_mcd7__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/detector/prevac/prevac_mcd7__modbus.yaml) | `Lab.Detector.PrevacMCD7.Modbus` | `modbus` | - |

#### Device Class: `digital_multimeter`

Device count in class: **4**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Digital Multimeter | [`digital_multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/digital_multimeter/generic/digital_multimeter__scpi.yaml) | `Lab.DigitalMultimeter.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `rohde_schwarz`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rohde & Schwarz HMC8012 Digital Multimeter (SCPI) | [`rohde_schwarz_hmc8012__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/digital_multimeter/rohde_schwarz/rohde_schwarz_hmc8012__scpi.yaml) | `Lab.DigitalMultimeter.RohdeSchwarzHmc8012.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SDM3055 Digital Multimeter (SCPI) | [`siglent_sdm3055__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/digital_multimeter/siglent/siglent_sdm3055__scpi.yaml) | `Lab.DigitalMultimeter.SiglentSdm3055.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `tektronix`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Tektronix DMM4050 Digital Multimeter (SCPI) | [`tektronix_dmm4050__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/digital_multimeter/tektronix/tektronix_dmm4050__scpi.yaml) | `Lab.DigitalMultimeter.TektronixDmm4050.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `electronic_load`

Device count in class: **1**

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SDL1000X Programmable DC Electronic Load (SCPI) | [`siglent_sdl1000x__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/electronic_load/siglent/siglent_sdl1000x__scpi.yaml) | `Lab.ElectronicLoad.SiglentSdl1000x.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `function_generator`

Device count in class: **1**

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SDG1032X Function Generator (SCPI) | [`siglent_sdg1032x__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/function_generator/siglent/siglent_sdg1032x__scpi.yaml) | `Lab.FunctionGenerator.SiglentSdg1032X.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `instrument`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Multimeter | [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml) | `Lab.Multimeter.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `magnetron_power_supply`

Device count in class: **2**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac M1600PDC-PS Magnetron Power Supply (Modbus) | [`prevac_m1600pdc_ps__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/magnetron_power_supply/prevac/prevac_m1600pdc_ps__modbus.yaml) | `Lab.MagnetronPowerSupply.PrevacM1600PDCPS.Modbus` | `modbus` | `scpi_lab` |
| Prevac M600DC-PS Magnetron Power Supply (Modbus) | [`prevac_m600dc_ps__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/magnetron_power_supply/prevac/prevac_m600dc_ps__modbus.yaml) | `Lab.MagnetronPowerSupply.PrevacM600DCPS.Modbus` | `modbus` | `scpi_lab` |

#### Device Class: `monitor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| BLE Vital Signs Monitor | [`vital_signs_monitor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/monitor/generic/vital_signs_monitor__ble_gatt.yaml) | `Embedded.HealthMonitor.BleGatt` | `ble` | `mhealth_ci` |

#### Device Class: `oscilloscope`

Device count in class: **7**

##### Vendor: `keysight`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Keysight InfiniiVision 1000X Oscilloscope (SCPI) | [`keysight_infiniivision_1000x__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/keysight/keysight_infiniivision_1000x__scpi.yaml) | `Lab.Oscilloscope.Keysight1000X.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `rigol`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rigol DS1000Z Oscilloscope (SCPI) | [`rigol_ds1000z__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/rigol/rigol_ds1000z__scpi.yaml) | `Lab.Oscilloscope.RigolDs1000z.Scpi` | `scpi` | `scpi_lab` |
| Rigol MSO5000 Oscilloscope (SCPI) | [`rigol_mso5000__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/rigol/rigol_mso5000__scpi.yaml) | `Lab.Oscilloscope.RigolMso5000.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `rohde_schwarz`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rohde & Schwarz HMO1002 Oscilloscope (SCPI) | [`rohde_schwarz_hmo1002__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/rohde_schwarz/rohde_schwarz_hmo1002__scpi.yaml) | `Lab.Oscilloscope.RohdeSchwarzHmo1002.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SDS1000X-E Oscilloscope (SCPI) | [`siglent_sds1000x_e__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/siglent/siglent_sds1000x_e__scpi.yaml) | `Lab.Oscilloscope.SiglentSds1000xE.Scpi` | `scpi` | `scpi_lab` |
| Siglent SDS2000X HD Oscilloscope (SCPI) | [`siglent_sds2000x_hd__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/siglent/siglent_sds2000x_hd__scpi.yaml) | `Lab.Oscilloscope.SiglentSds2000xHd.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `tektronix`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Tektronix MDO3000 Series Oscilloscope (SCPI) | [`tektronix_mdo3000__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/oscilloscope/tektronix/tektronix_mdo3000__scpi.yaml) | `Lab.Oscilloscope.TektronixMdo3000.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `power_analyzer`

Device count in class: **1**

##### Vendor: `rohde_schwarz`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rohde & Schwarz HMC8015 Power Analyzer (SCPI) | [`rohde_schwarz_hmc8015__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_analyzer/rohde_schwarz/rohde_schwarz_hmc8015__scpi.yaml) | `Lab.PowerAnalyzer.RohdeSchwarzHmc8015.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `power_supply`

Device count in class: **5**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Bench Power Supply | [`bench_power_supply__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_supply/generic/bench_power_supply__scpi.yaml) | `Lab.BenchPowerSupply.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `keysight`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Keysight E36312A Triple Output Power Supply (SCPI) | [`keysight_e36312a__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_supply/keysight/keysight_e36312a__scpi.yaml) | `Lab.PowerSupply.KeysightE36312A.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `rigol`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rigol DP800 Power Supply (SCPI) | [`rigol_dp800__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_supply/rigol/rigol_dp800__scpi.yaml) | `Lab.PowerSupply.RigolDp800.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `rohde_schwarz`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Rohde & Schwarz HMP4040 Power Supply (SCPI) | [`rohde_schwarz_hmp4040__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_supply/rohde_schwarz/rohde_schwarz_hmp4040__scpi.yaml) | `Lab.PowerSupply.RohdeSchwarzHmp4040.Scpi` | `scpi` | `scpi_lab` |

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SPD1000X Programmable DC Power Supply (SCPI) | [`siglent_spd1000x__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/power_supply/siglent/siglent_spd1000x__scpi.yaml) | `Lab.PowerSupply.SiglentSpd1000X.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `sensor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| BLE Temperature Sensor | [`temperature_sensor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/sensor/generic/temperature_sensor__ble_gatt.yaml) | `Embedded.TempSensor.BleGatt` | `ble` | `mhealth_ci` |

#### Device Class: `spectrum_analyzer`

Device count in class: **1**

##### Vendor: `siglent`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siglent SSA3000X Spectrum Analyzer (SCPI) | [`siglent_ssa3000x__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/spectrum_analyzer/siglent/siglent_ssa3000x__scpi.yaml) | `Lab.SpectrumAnalyzer.SiglentSsa3000x.Scpi` | `scpi` | `scpi_lab` |

#### Device Class: `sublimation_pump_power_supply`

Device count in class: **1**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac TSP04-PS Sublimation Pump Power Supply (Modbus) | [`prevac_tsp04_ps__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/sublimation_pump_power_supply/prevac/prevac_tsp04_ps__modbus.yaml) | `Lab.SublimationPumpPowerSupply.PrevacTSP04PS.Modbus` | `modbus` | `scpi_lab` |

#### Device Class: `xray_source_emission_controller`

Device count in class: **1**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac XR40B-EC X-Ray Source Emission Controller (Modbus) | [`prevac_xr40b_ec__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/xray_source_emission_controller/prevac/prevac_xr40b_ec__modbus.yaml) | `Lab.XraySourceEmissionController.PrevacXR40BEC.Modbus` | `modbus` | `scpi_lab` |

## `industrial_iiot_pack` - Industrial Pack (Industry 4.0)

Devices in pack: **31**

Pack profiles: `iiot_monitoring`, `modbus_master_plc_demo`, `process_cell_quickstart`

### Domain: `energy` - Energy & e-Mobility

Device count in domain: **5**

#### Device Class: `meter`

Device count in class: **3**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| 3-Phase Energy Meter (Modbus) | [`energy_meter_3ph__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/generic/energy_meter_3ph__modbus.yaml) | `Energy.EnergyMeter3Ph.Modbus` | `modbus` | `iiot_monitoring` |
| 3-Phase Energy Meter (MQTT) | [`energy_meter_3ph__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/generic/energy_meter_3ph__mqtt.yaml) | `Energy.EnergyMeter3Ph.Mqtt` | `mqtt` | `iiot_monitoring` |

##### Vendor: `schneider`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Schneider Acti9 iEM3000 Energy Meter (Modbus) | [`energy_meter_iem3000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/energy_meter_iem3000__modbus.yaml) | `Energy.EnergyMeterIem3000.Modbus` | `modbus` | `modbus_master_plc_demo` |

#### Device Class: `power_meter`

Device count in class: **1**

##### Vendor: `abb`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| ABB M1M Power Meter (Modbus TCP) | [`abb_m1m_power_meter__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/power_meter/abb/abb_m1m_power_meter__modbus.yaml) | `Energy.PowerMeter.AbbM1M.Modbus` | `modbus` | `process_cell_quickstart` |

#### Device Class: `rack_pdu`

Device count in class: **1**

##### Vendor: `apc`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| APC NetShelter Rack PDU RPDU2g (Modbus) | [`rack_pdu_rpdu2g__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/rack_pdu/apc/rack_pdu_rpdu2g__modbus.yaml) | `Energy.RackPdu.ApcNetShelter2g.Modbus` | `modbus` | `iiot_monitoring` |

### Domain: `environment` - Environment & Weather

Device count in domain: **2**

#### Device Class: `sensor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | `iiot_monitoring` |

#### Device Class: `station`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Air Quality Station (HTTP) | [`air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/station/generic/air_quality_station__http.yaml) | `Env.AirQualityStation.Http` | `http` | `iiot_monitoring` |

### Domain: `industrial` - Industrial Systems

Device count in domain: **22**

#### Device Class: `controller`

Device count in class: **7**

##### Vendor: `eurotherm`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Eurotherm 3216 Temperature Controller (Modbus TCP) | [`eurotherm_3216__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/eurotherm/eurotherm_3216__modbus.yaml) | `Process.ThermalController.Eurotherm3216.Modbus` | `modbus` | - |
| Eurotherm 3504 Pressure Controller (Modbus TCP) | [`eurotherm_3504__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/eurotherm/eurotherm_3504__modbus.yaml) | `Process.PressureController.Eurotherm3504.Modbus` | `modbus` | - |

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Generic PLC Controller (Modbus Master) | [`plc_controller__modbus_master.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/plc_controller__modbus_master.yaml) | `Industrial.PlcController.ModbusMaster` | `modbus` | `modbus_master_plc_demo` |
| PID Process Controller (Modbus) | [`pid_process_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/pid_process_controller__modbus.yaml) | `Process.PIDController.Modbus` | `modbus` | `process_cell_quickstart` |
| Stepper Controller (Modbus) | [`stepper_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/stepper_controller__modbus.yaml) | `Motion.StepperController.Modbus` | `modbus` | `process_cell_quickstart` |
| Thermal Controller (Advanced) | [`thermal_controller_advanced.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/thermal_controller_advanced.yaml) | `Process.ThermalController.Advanced` | `-` | `process_cell_quickstart` |
| Thermal Controller (Modbus) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/thermal_controller__modbus.yaml) | `Process.ThermalController.Modbus` | `modbus` | `process_cell_quickstart` |

#### Device Class: `counter`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Line Counter (MQTT) | [`line_counter__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/counter/generic/line_counter__mqtt.yaml) | `IIoT.LineCounter.Mqtt` | `mqtt` | `iiot_monitoring` |

#### Device Class: `drive`

Device count in class: **3**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| VFD Drive (Modbus) | [`vfd_drive__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/drive/generic/vfd_drive__modbus.yaml) | `Motion.VFDrive.Modbus` | `modbus` | `process_cell_quickstart` |

##### Vendor: `schneider`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Schneider Electric Altivar Machine ATV320 VFD (Modbus) | [`schneider_altivar_320__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/drive/schneider/schneider_altivar_320__modbus.yaml) | `Motion.VFDrive.SchneiderAltivar320.Modbus` | `modbus` | `modbus_master_plc_demo` |

##### Vendor: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens SINAMICS G120C VFD (Modbus TCP) | [`g120c__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/drive/siemens/g120c__modbus.yaml) | `Motion.VFDrive.SiemensG120C.Modbus` | `modbus` | - |

#### Device Class: `io_module`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| IO Module (Modbus) | [`io_module__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/io_module/generic/io_module__modbus.yaml) | `IO.IOModule.Modbus` | `modbus` | `iiot_monitoring` |

##### Vendor: `wago`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| WAGO 750-8000 I/O System (Modbus TCP) | [`wago_750_8000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/io_module/wago/wago_750_8000__modbus.yaml) | `IO.IOModule.Wago750_8000.Modbus` | `modbus` | - |

#### Device Class: `line`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Packaging Line (OPC UA) | [`packaging_line__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/line/generic/packaging_line__opcua.yaml) | `Process.PackagingLine.OpcUa` | `opcua` | `process_cell_quickstart` |

#### Device Class: `monitor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Condition Monitor (MQTT) | [`condition_monitor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/monitor/generic/condition_monitor__mqtt.yaml) | `Condition.ConditionMonitor.Mqtt` | `mqtt` | `iiot_monitoring` |

#### Device Class: `pressure_transmitter`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Pressure Transmitter (Modbus) | [`pressure_transmitter__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/pressure_transmitter/generic/pressure_transmitter__modbus.yaml) | `Process.PressureTransmitter.Modbus` | `modbus` | `iiot_monitoring` |

#### Device Class: `process_cell`

Device count in class: **2**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Process Cell (OPC UA) | [`process_cell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/process_cell/generic/process_cell__opcua.yaml) | `Process.ProcessCell.OpcUa` | `opcua` | `process_cell_quickstart` |

##### Vendor: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens SIMATIC S7-1500 Process Cell (OPC UA) | [`s7_1500_process_cell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/process_cell/siemens/s7_1500_process_cell__opcua.yaml) | `Process.ProcessCell.SiemensS7_1500.OpcUa` | `opcua` | - |

#### Device Class: `sensor`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Vacuum Gauge (Modbus) | [`vacuum_gauge__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/sensor/generic/vacuum_gauge__modbus.yaml) | `Process.VacuumGauge.Modbus` | `modbus` | `process_cell_quickstart` |

#### Device Class: `station`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Vision Quality Station (HTTP) | [`vision_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/station/generic/vision_quality_station__http.yaml) | `Quality.VisionStation.Http` | `http` | `iiot_monitoring` |

#### Device Class: `vehicle`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| AGV Vehicle (MQTT) | [`agv_vehicle__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/vehicle/generic/agv_vehicle__mqtt.yaml) | `Logistics.AGVVehicle.Mqtt` | `mqtt` | `iiot_monitoring` |

#### Device Class: `workcell`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Production Workcell (OPC UA) | [`production_workcell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/workcell/generic/production_workcell__opcua.yaml) | `Process.Workcell.OpcUa` | `opcua` | `process_cell_quickstart` |

### Domain: `lab` - Lab & Embedded

Device count in domain: **2**

#### Device Class: `detector`

Device count in class: **1**

##### Vendor: `prevac`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Prevac MCD7 Multichanneltron Detector (Modbus) | [`prevac_mcd7__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/detector/prevac/prevac_mcd7__modbus.yaml) | `Lab.Detector.PrevacMCD7.Modbus` | `modbus` | - |

#### Device Class: `instrument`

Device count in class: **1**

##### Vendor: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Multimeter | [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml) | `Lab.Multimeter.Scpi` | `scpi` | `iiot_monitoring` |
