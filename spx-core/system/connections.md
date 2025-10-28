# Connections

Connections (`spx_core/system/connections.py`) copy values between attributes each time the simulation runs. They are handy for routing sensor data into controllers without writing custom actions.

## YAML structure

```yaml
connections:
  - sensor_to_controller:
      from: sensor.attributes.temperature
      to: controller.attributes.input_temperature
  - flow_feedback:
      from: "#attr(pump.flow)"
      to: "#external(tank.inflow)"
```

### How it works

- Each entry becomes a `Connection` component with a `run()` method that reads the source wrapper and writes the destination wrapper.
- Sources and destinations can use plain dotted paths (`sensor.attributes.temperature`) or explicit wrapper syntax (`#attr(...)`, `#external(...)`).
- Connections run as part of the standard model loop, so values stay in sync automatically.

### Validation & logging

- The container accepts lists or dicts; mixed formats are normalized internally.
- If the source or destination cannot be resolved, the connection raises a `ValueError` during load so you catch mistakes early.
- At runtime, errors are logged with the connection name; this helps QA trace broken signal paths.

### Tips

- Use connections for simple mirroring. If you need math (scaling, offsets), combine them with actions (e.g., a `function` action that multiplies before writing to the target).
- Group related connections in the YAML and comment them; you will thank yourself during troubleshooting.
- Remember that connections overwrite the destination every cycle—do not point them at values users need to edit manually unless you intend to clamp those values.
