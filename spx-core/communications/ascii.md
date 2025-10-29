# ASCII / SCPI Adapter

The ASCII adapter serves simple text protocols such as SCPI. It listens on TCP, parses newline-terminated commands, and maps them to attributes or custom handlers.

## YAML structure

```yaml
communication:
  ascii:
    port: 5025
    terminator: "\n"
    response_delay: 0.01
    response_jitter: 0.0
    mappings:
      "MEAS:VOLT?": "#out(voltage)"
      "CONF:MODE {mode}":
        "#attr(measurement_mode)": "mode"
        response: "ACK"
```

### JSON structure

```json
{
  "communication": {
    "ascii": {
      "port": 5025,
      "terminator": "\n",
      "response_delay": 0.01,
      "response_jitter": 0.0,
      "mappings": {
        "MEAS:VOLT?": "#out(voltage)",
        "CONF:MODE {mode}": {
          "#attr(measurement_mode)": "mode",
          "response": "ACK"
        }
      }
    }
  }
}
```

### Key fields

- `port`: TCP port, default 5025.
- `terminator`: command delimiter (`\n`, `\r\n`, etc.).
- `response_delay`: base delay inserted before responding (seconds).
- `response_jitter`: random delta added to delay (seconds).
- `mappings`: command dictionary. Each key is a command pattern.
  - A string value returns the referenced attribute.
  - A mapping updates attributes or invokes handlers; optional `response` overrides the reply.

### Placeholders

Commands may include placeholders (`{mode}`) that the adapter passes into the mapping as variables. You can write them back to attributes or use them in responses.

```yaml
"CONF:VOLT {value}":
  "#attr(voltage_setpoint)": "value"
  response: "VOLT {value}"
```

```json
{
  "CONF:VOLT {value}": {
    "#attr(voltage_setpoint)": "value",
    "response": "VOLT {value}"
  }
}
```

### Scenarios

Use scenarios to simulate link issues:

```yaml
scenarios:
  ascii_disconnect:
    duration: 2.0
    call:
      path: communication.ascii.detach
      stop_path: communication.ascii.attach
  ascii_delay_spike:
    duration: 5.0
    overrides:
      communication.ascii.response_delay: 10.0
```

```json
{
  "scenarios": {
    "ascii_disconnect": {
      "duration": 2.0,
      "call": {
        "path": "communication.ascii.detach",
        "stop_path": "communication.ascii.attach"
      }
    },
    "ascii_delay_spike": {
      "duration": 5.0,
      "overrides": {
        "communication.ascii.response_delay": 10.0
      }
    }
  }
}
```

### Tips

- Normalize commands to uppercase to avoid case mismatches.
- Use `response_delay` and `response_jitter` to emulate slow hardware.
- Validate mappings with unit tests using the SDK (`scpi_multimeter.yaml` is a good starting point).
