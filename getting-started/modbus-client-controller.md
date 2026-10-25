---
description: Use SPX as an active Modbus TCP client, master, and PLC-style controller.
icon: network-wired
---

# Use SPX as a Modbus Client / PLC Controller

SPX can simulate a Modbus TCP device, but it can also act as an active Modbus
client. Use this flow when you want an SPX model to poll downstream Modbus
devices, write control commands, and validate PLC-style control logic.

The main distinction is:

- `modbus_slave` exposes an SPX model as a Modbus TCP server/device.
- `modbus_master` makes an SPX model act as a Modbus TCP client/controller.

For the device-simulator path, start with
[Add Modbus TCP/IP to Your Simulation](add-communication-protocol.md). For the
controller path, use the Industrial IIoT pack profile described below.

## Example profile

The reference example is `industrial_iiot_pack` with the
`modbus_master_plc_demo` profile from `spx-examples`.

It starts a small closed-loop Modbus setup:

- `Industrial.PlcController.ModbusMaster` acts as the PLC-style controller.
- `Motion.VFDrive.SchneiderAltivar320.Modbus` acts as the downstream VFD.
- `Energy.EnergyMeterIem3000.Modbus` acts as the downstream power meter.

The PLC controller reads feedback from the VFD and power meter, writes run and
speed commands to the VFD, and applies a simple power-limit interlock. When the
measured power exceeds the configured limit, the controller clears the drive run
command.

Source files:

- [`spx-examples`](https://github.com/HammerHeads-Engineers/spx-examples)
- [`profiles/industrial_iiot_pack/modbus_master_plc_demo.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/profiles/industrial_iiot_pack/modbus_master_plc_demo.yaml)
- [`library/domains/industrial/controller/generic/plc_controller__modbus_master.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/industrial/controller/generic/plc_controller__modbus_master.yaml)

## Generate the demo bundle

From `spx-examples`, generate an Industrial IIoT bundle with the Modbus master
profile:

```bash
python -m installer generate \
  --packages industrial_iiot_pack \
  --profile-ids modbus_master_plc_demo \
  --no-ui \
  --output build/spx-generated
```

Then start the generated stack:

```bash
cd build/spx-generated
./spx-start.sh
```

On Windows PowerShell, use `pwsh ./spx-start.ps1` instead.

## How the controller is wired

The controller model uses `communication.modbus_master.bindings`. Each binding
defines a target device, register area, address, codec, direction, and mapped
SPX attribute.

Typical binding roles in the demo:

| Binding role | Direction | Target |
| --- | --- | --- |
| Read VFD status word | inbound | Altivar holding register |
| Read VFD actual speed | inbound | Altivar holding register |
| Write VFD control word | outbound | Altivar holding register |
| Write VFD speed reference | outbound | Altivar holding register |
| Read active power | inbound | iEM3000 input registers |
| Read frequency | inbound | iEM3000 input registers |
| Read imported energy | inbound | iEM3000 holding registers |

This makes the SPX controller behave like a Modbus TCP master while the VFD and
meter models behave like Modbus TCP slave devices.

## Control flow

The PLC controller has command attributes such as:

- `k__drive_run_enable`
- `k__drive_speed_setpoint_hz`
- `k__power_limit_kw`
- `k__power_limit_stop_enable`

It computes internal command registers and writes them through Modbus:

- `_drive_control_word_raw` -> VFD run command
- `_drive_speed_setpoint_raw` -> VFD speed reference

It also reads back downstream state:

- `drive_status_word_raw`
- `drive_speed_actual_raw`
- `drive_speed_actual_hz`
- `meter_active_power_total_kw`
- `meter_frequency_hz`
- `meter_energy_import_total_kwh`

The power-limit interlock is the key controller behavior:

- if `meter_active_power_total_kw <= k__power_limit_kw`, the drive command can
  pass through;
- if `meter_active_power_total_kw > k__power_limit_kw`, the controller blocks
  the drive command and writes stop to the VFD.

## Minimal YAML shape

The core pattern is a `modbus_master` block with inbound and outbound bindings:

```yaml
communication:
  - modbus_master:
      poll_interval: 0.2
      timeout: 1.0
      bindings:
        - name: query_meter_active_power_total
          host: "$param(meter_host)"
          port: "$param(meter_port)"
          slave_id: "$param(meter_unit_id)"
          area: i_r
          address: 3060
          length: 2
          codec: float
          direction: inbound
          attribute: meter_active_power_total_kw

        - name: set_drive_speed_reference
          host: "$param(drive_host)"
          port: "$param(drive_port)"
          slave_id: "$param(drive_unit_id)"
          area: h_r
          address: 12762
          length: 1
          codec: uint_16
          direction: outbound
          attribute: _drive_speed_setpoint_raw
```

Use inbound bindings for telemetry and feedback. Use outbound bindings for
commands written by the controller.

## When to use this pattern

Use `modbus_master` when SPX should represent the automation controller side of
a system:

- PLC-like supervisory logic
- gateway or edge-controller behavior
- closed-loop Modbus control tests
- validation of drive, meter, and IO interactions
- testing interlocks and fallback logic without physical hardware

Use `modbus_slave` instead when your real SUT is the Modbus client and SPX only
needs to expose simulated device registers.

## Validation

The `spx-examples` integration test for this profile checks the important
runtime behavior:

- the PLC reads VFD status and speed feedback;
- the PLC reads meter power and frequency;
- the PLC writes VFD run and speed commands;
- the power-limit interlock clears the VFD run command.

Reference:
[`tests/packs/industrial_iiot_pack/integration/test_modbus_master_plc_demo_smoke.py`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/tests/packs/industrial_iiot_pack/integration/test_modbus_master_plc_demo_smoke.py)

## Next steps

- Adapter reference: [Modbus adapters](../spx-core/communications/modbus.md)
- Pack reference: [Industry packs and profiles](../usage-scenarios-and-examples/industry-packs.md)
- Device-simulator tutorial: [Add Modbus TCP/IP to Your Simulation](add-communication-protocol.md)

## Next steps on simplephysx.com

Explore the Modbus TCP simulator workflow:

- [Modbus TCP Simulator](https://www.simplephysx.com/modbus-simulator)
