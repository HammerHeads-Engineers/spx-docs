---
description: >-
  Searchable catalog of device models available per installer pack, generated from spx-examples main.
icon: list
---

# Device Catalog (spx-examples)

This page lists device models available in each installer pack.
Names and file names are aligned 1:1 with `spx-examples` so docs search can find exact device strings quickly.

> Important
> These are reference simulation models from `spx-examples`, not official digital twins certified by device manufacturers.
> They are not officially supported by manufacturers and we do not guarantee a 100% functional match to real hardware behavior.

Source snapshot: `spx-examples` `origin/main` at commit `8d03be0fed44188672fc8eb1f3a598fc3d797be7` (checked 2026-02-08 14:57 UTC).

Grouping on this page: **Pack -> Domain -> Vendor/Family**.

## Conventions

- `Device name`: official `name` from `library/catalog/models.yaml`.
- `Model file`: exact YAML file name used in the library.
- `Vendor/Family`: folder under `library/domains/<domain>/...` (for example `abb`, `siemens`, `generic`).
- `Profiles`: only profiles that belong to the current pack.

## `smart_building_pack` - Smart-Building Pack (BMS)

Devices in pack: **20**

Pack profiles: `bms_quickstart`

### Domain: `iot` - IoT & Edge Telemetry

Device count in domain: **16**

#### Vendor/Family: `abb`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| ABB JRA/S 4.230.5.1 Cover Actuator (KNX) | [`abb_jra_s4_230_5_1__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/abb/abb_jra_s4_230_5_1__knx.yaml) | `Building.CoverActuator.AbbJraS4_230_5_1.Knx` | `knx` | `bms_quickstart` |
| ABB SA/S12.16.5.1 Switch Actuator (KNX) | [`abb_sa_s12_16_5_1__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/abb/abb_sa_s12_16_5_1__knx.yaml) | `Building.SwitchActuator.AbbSaS12_16_5_1.Knx` | `knx` | `bms_quickstart` |

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Air Quality Station (HTTP) | [`air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/air_quality_station__http.yaml) | `Env.AirQualityStation.Http` | `http` | `bms_quickstart` |
| BMS Controller (OPC UA) | [`bms_controller__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/bms_controller__opcua.yaml) | `Building.BMSController.OpcUa` | `opcua` | `bms_quickstart` |
| Fire Alarm Panel (BACnet) | [`fire_alarm_panel__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/fire_alarm_panel__bacnet.yaml) | `Building.FireAlarmPanel.Bacnet` | `bacnet` | `bms_quickstart` |
| Flexit Nordic HVAC (BACnet) | [`hvac_flexit_nordic__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/hvac_flexit_nordic__bacnet.yaml) | `Building.HvacFlexitNordic.Bacnet` | `bacnet` | `bms_quickstart` |
| Lighting Panel (OPC UA) | [`lighting_panel__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/lighting_panel__opcua.yaml) | `Building.LightingPanel.OpcUa` | `opcua` | `bms_quickstart` |
| Lighting Zone (KNX) | [`lighting_zone__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/lighting_zone__knx.yaml) | `Building.LightingZone.Knx` | `knx` | `bms_quickstart` |
| LwM2M Environment Sensor | [`environment_sensor__lwm2m.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__lwm2m.yaml) | `Env.EnvSensor.Lwm2m` | `lwm2m, coap` | `bms_quickstart` |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | `bms_quickstart` |
| Room Controller (KNX) | [`room_controller__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/room_controller__knx.yaml) | `Building.RoomController.Knx` | `knx` | `bms_quickstart` |
| Schneider Acti9 iEM3000 Energy Meter (Modbus) | [`energy_meter_iem3000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_iem3000__modbus.yaml) | `Energy.EnergyMeterIem3000.Modbus` | `modbus` | `bms_quickstart` |
| Security Access Controller (BACnet) | [`security_access_controller__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/security_access_controller__bacnet.yaml) | `Building.SecurityAccessController.Bacnet` | `bacnet` | `bms_quickstart` |
| Smart Plug / Relay (Matter) | [`smart_plug__matter.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/smart_plug__matter.yaml) | `Building.SmartPlug.Matter` | `matter` | `bms_quickstart` |
| Thermostat (Matter) | [`thermostat__matter.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/thermostat__matter.yaml) | `Building.Thermostat.Matter` | `matter` | `bms_quickstart` |

#### Vendor/Family: `theben`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Presence Detector (Theben theRonda P360 KNX) | [`theronda_p360__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/theben/theronda_p360__knx.yaml) | `Building.PresenceDetector.ThebenP360.Knx` | `knx` | `bms_quickstart` |

### Domain: `thermal_controllers` - Thermal Controllers

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Thermal Controller (Advanced) | [`thermal_controller_advanced.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller_advanced.yaml) | `Process.ThermalController.Advanced` | `-` | `bms_quickstart` |
| Thermal Controller (Modbus) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml) | `Process.ThermalController.Modbus` | `modbus` | `bms_quickstart` |

### Domain: `weather` - Weather & Forecasting

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Weather Forecast Feed | [`weather_forecast__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/weather/weather_forecast__http.yaml) | `Weather.WeatherFeed.Http` | `http` | `bms_quickstart` |
| Weather Gateway (WAGO PFC200 + Vaisala WXT530, MQTT Discovery) | [`weather_gateway_wago_pfc200__vaisala_wxt530__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/weather/weather_gateway_wago_pfc200__vaisala_wxt530__mqtt.yaml) | `Weather.WeatherGateway.WagoPfc200.VaisalaWxt530.Mqtt` | `mqtt` | `bms_quickstart` |

## `energy_pack` - Energy Pack (e-Mobility & DER)

Devices in pack: **8**

Pack profiles: `ev_csms_demo`

### Domain: `energy` - Energy & e-Mobility

Device count in domain: **2**

#### Vendor/Family: `emobility`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| CSMS Control Simulator (OCPP 1.6) | [`csms__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/energy/emobility/csms__ocpp.yaml) | `Energy.CSMS.Ocpp` | `ocpp` | `ev_csms_demo` |
| EVSE / Charge Point (OCPP 1.6) | [`evse__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/energy/emobility/evse__ocpp.yaml) | `Energy.EVSE.Ocpp` | `ocpp` | `ev_csms_demo` |

### Domain: `iot` - IoT & Edge Telemetry

Device count in domain: **3**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| 3-Phase Energy Meter (Modbus) | [`energy_meter_3ph__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_3ph__modbus.yaml) | `Energy.EnergyMeter3Ph.Modbus` | `modbus` | - |
| 3-Phase Energy Meter (MQTT) | [`energy_meter_3ph__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_3ph__mqtt.yaml) | `Energy.EnergyMeter3Ph.Mqtt` | `mqtt` | - |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | `ev_csms_demo` |

### Domain: `thermal_controllers` - Thermal Controllers

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Thermal Controller (Advanced) | [`thermal_controller_advanced.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller_advanced.yaml) | `Process.ThermalController.Advanced` | `-` | `ev_csms_demo` |
| Thermal Controller (Modbus) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml) | `Process.ThermalController.Modbus` | `modbus` | `ev_csms_demo` |

### Domain: `weather` - Weather & Forecasting

Device count in domain: **1**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Weather Forecast Feed | [`weather_forecast__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/weather/weather_forecast__http.yaml) | `Weather.WeatherFeed.Http` | `http` | `ev_csms_demo` |

## `embedded_lab_pack` - Embedded & Lab Pack

Devices in pack: **7**

Pack profiles: `mhealth_ci`, `scpi_lab`

### Domain: `ble` - BLE Devices

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| BLE Temperature Sensor | [`temperature_sensor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/ble/generic/temperature_sensor__ble_gatt.yaml) | `Embedded.TempSensor.BleGatt` | `ble` | `mhealth_ci` |
| BLE Vital Signs Monitor | [`vital_signs_monitor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/ble/generic/vital_signs_monitor__ble_gatt.yaml) | `Embedded.HealthMonitor.BleGatt` | `ble` | `mhealth_ci` |

### Domain: `iot` - IoT & Edge Telemetry

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| LwM2M Environment Sensor | [`environment_sensor__lwm2m.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__lwm2m.yaml) | `Env.EnvSensor.Lwm2m` | `lwm2m, coap` | - |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | - |

### Domain: `measurement_instruments` - Measurement Instruments

Device count in domain: **1**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Multimeter | [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml) | `Lab.Multimeter.Scpi` | `scpi` | `scpi_lab` |

### Domain: `vacuum_systems` - Vacuum Systems

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Vacuum Gauge (Modbus) | [`vacuum_gauge__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/vacuum_systems/generic/vacuum_gauge__modbus.yaml) | `Process.VacuumGauge.Modbus` | `modbus` | `scpi_lab` |
| Vacuum Gauge Multichannel (Modbus) | [`vacuum_gauge_multichannel__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/vacuum_systems/generic/vacuum_gauge_multichannel__modbus.yaml) | `Process.VacuumGaugeMultichannel.Modbus` | `modbus` | - |

## `industrial_iiot_pack` - Industrial Pack (Industry 4.0)

Devices in pack: **26**

Pack profiles: `iiot_monitoring`, `process_cell_quickstart`

### Domain: `iot` - IoT & Edge Telemetry

Device count in domain: **15**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| 3-Phase Energy Meter (Modbus) | [`energy_meter_3ph__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_3ph__modbus.yaml) | `Energy.EnergyMeter3Ph.Modbus` | `modbus` | `iiot_monitoring` |
| 3-Phase Energy Meter (MQTT) | [`energy_meter_3ph__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_3ph__mqtt.yaml) | `Energy.EnergyMeter3Ph.Mqtt` | `mqtt` | `iiot_monitoring` |
| AGV Vehicle (MQTT) | [`agv_vehicle__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/agv_vehicle__mqtt.yaml) | `Logistics.AGVVehicle.Mqtt` | `mqtt` | `iiot_monitoring` |
| Air Quality Station (HTTP) | [`air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/air_quality_station__http.yaml) | `Env.AirQualityStation.Http` | `http` | `iiot_monitoring` |
| Condition Monitor (MQTT) | [`condition_monitor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/condition_monitor__mqtt.yaml) | `Condition.ConditionMonitor.Mqtt` | `mqtt` | `iiot_monitoring` |
| IO Module (Modbus) | [`io_module__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/io_module__modbus.yaml) | `IO.IOModule.Modbus` | `modbus` | `iiot_monitoring` |
| Line Counter (MQTT) | [`line_counter__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/line_counter__mqtt.yaml) | `IIoT.LineCounter.Mqtt` | `mqtt` | `iiot_monitoring` |
| MQTT Environment Sensor | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml) | `Env.EnvSensor.Mqtt` | `mqtt` | `iiot_monitoring` |
| Packaging Line (OPC UA) | [`packaging_line__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/packaging_line__opcua.yaml) | `Process.PackagingLine.OpcUa` | `opcua` | `process_cell_quickstart` |
| Pressure Transmitter (Modbus) | [`pressure_transmitter__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/pressure_transmitter__modbus.yaml) | `Process.PressureTransmitter.Modbus` | `modbus` | `iiot_monitoring` |
| Process Cell (OPC UA) | [`process_cell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/process_cell__opcua.yaml) | `Process.ProcessCell.OpcUa` | `opcua` | `process_cell_quickstart` |
| Production Workcell (OPC UA) | [`production_workcell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/production_workcell__opcua.yaml) | `Process.Workcell.OpcUa` | `opcua` | `process_cell_quickstart` |
| Vision Quality Station (HTTP) | [`vision_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/vision_quality_station__http.yaml) | `Quality.VisionStation.Http` | `http` | `iiot_monitoring` |

#### Vendor/Family: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens SIMATIC S7-1500 Process Cell (OPC UA) | [`s7_1500_process_cell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/siemens/s7_1500_process_cell__opcua.yaml) | `Process.ProcessCell.SiemensS7_1500.OpcUa` | `opcua` | - |

#### Vendor/Family: `wago`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| WAGO 750-8000 I/O System (Modbus TCP) | [`wago_750_8000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/wago/wago_750_8000__modbus.yaml) | `IO.IOModule.Wago750_8000.Modbus` | `modbus` | - |

### Domain: `measurement_instruments` - Measurement Instruments

Device count in domain: **1**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| SCPI Multimeter | [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml) | `Lab.Multimeter.Scpi` | `scpi` | `iiot_monitoring` |

### Domain: `motion_controllers` - Motion Controllers

Device count in domain: **3**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Stepper Controller (Modbus) | [`stepper_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/motion_controllers/generic/stepper_controller__modbus.yaml) | `Motion.StepperController.Modbus` | `modbus` | `process_cell_quickstart` |
| VFD Drive (Modbus) | [`vfd_drive__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/motion_controllers/generic/vfd_drive__modbus.yaml) | `Motion.VFDrive.Modbus` | `modbus` | `process_cell_quickstart` |

#### Vendor/Family: `siemens`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Siemens SINAMICS G120C VFD (Modbus TCP) | [`g120c__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/motion_controllers/siemens/g120c__modbus.yaml) | `Motion.VFDrive.SiemensG120C.Modbus` | `modbus` | - |

### Domain: `thermal_controllers` - Thermal Controllers

Device count in domain: **5**

#### Vendor/Family: `eurotherm`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Eurotherm 3216 Temperature Controller (Modbus TCP) | [`eurotherm_3216__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/eurotherm/eurotherm_3216__modbus.yaml) | `Process.ThermalController.Eurotherm3216.Modbus` | `modbus` | - |
| Eurotherm 3504 Pressure Controller (Modbus TCP) | [`eurotherm_3504__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/eurotherm/eurotherm_3504__modbus.yaml) | `Process.PressureController.Eurotherm3504.Modbus` | `modbus` | - |

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| PID Process Controller (Modbus) | [`pid_process_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/pid_process_controller__modbus.yaml) | `Process.PIDController.Modbus` | `modbus` | `process_cell_quickstart` |
| Thermal Controller (Advanced) | [`thermal_controller_advanced.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller_advanced.yaml) | `Process.ThermalController.Advanced` | `-` | `process_cell_quickstart` |
| Thermal Controller (Modbus) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml) | `Process.ThermalController.Modbus` | `modbus` | `process_cell_quickstart` |

### Domain: `vacuum_systems` - Vacuum Systems

Device count in domain: **2**

#### Vendor/Family: `generic`

| Device name | Model file | Model ID | Protocols | Profiles |
| --- | --- | --- | --- | --- |
| Vacuum Gauge (Modbus) | [`vacuum_gauge__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/vacuum_systems/generic/vacuum_gauge__modbus.yaml) | `Process.VacuumGauge.Modbus` | `modbus` | `process_cell_quickstart` |
| Vacuum Gauge Multichannel (Modbus) | [`vacuum_gauge_multichannel__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/vacuum_systems/generic/vacuum_gauge_multichannel__modbus.yaml) | `Process.VacuumGaugeMultichannel.Modbus` | `modbus` | - |
