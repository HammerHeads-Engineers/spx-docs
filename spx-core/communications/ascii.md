# ASCII / SCPI Adapter

**YAML key:** `ascii`

The ASCII adapter serves simple text protocols such as SCPI. It listens on TCP (or UDP), parses newline-terminated commands, and maps them to attributes or custom handlers.

## Configuration Example

{% tabs %}
{% tab title="YAML" %}
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
{% endtab %}

{% tab title="JSON" %}
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
{% endtab %}
{% endtabs %}

### Key fields

- `host` (default: `0.0.0.0`) — bind address
- `port`: TCP port. If omitted, SPX auto-assigns a free port starting at `5025` and writes the effective value into the instance at `communication.ascii.port`.
- `transport` (default: `tcp`) — `tcp|udp`
- `terminator`: command delimiter (`\n`, `\r\n`, etc.).
- `response_delay`: base delay inserted before responding (seconds).
- `response_jitter`: random delta added to delay (seconds).
- `mappings`: legacy command dictionary (still supported; converted internally to `bindings`). Each key is a command pattern.
  - A string value returns the referenced attribute.
  - A mapping updates attributes or invokes handlers; optional `response` overrides the reply.
- `bindings`: explicit binding definitions (see the spx-examples SCPI multimeter model for a concrete pattern).

> Tip: In `spx-examples`, the SCPI multimeter model omits `port` so it can run multiple instances without collisions. See [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml).

### Placeholders

Commands may include placeholders (`{mode}`) that the adapter passes into the mapping as variables. You can write them back to attributes or use them in responses.

{% tabs %}
{% tab title="YAML" %}
```yaml
"CONF:VOLT {value}":
  "#attr(voltage_setpoint)": "value"
  response: "VOLT {value}"

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "CONF:VOLT {value}": {
    "#attr(voltage_setpoint)": "value",
    "response": "VOLT {value}"
  }
}

```
{% endtab %}
{% endtabs %}

### Scenarios

Use scenarios to simulate link issues:

{% tabs %}
{% tab title="YAML" %}
```yaml
scenarios:
  ascii_disconnect:
    duration: 2.0
    call:
      path: communication.ascii.detach
      stop_path: communication.ascii.attach
  ascii_response_delay_spike:
    duration: 5.0
    overrides:
      communication.ascii.response_delay: 10.0

```
{% endtab %}

{% tab title="JSON" %}
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
    "ascii_response_delay_spike": {
      "duration": 5.0,
      "overrides": {
        "communication.ascii.response_delay": 10.0
      }
    }
  }
}

```
{% endtab %}
{% endtabs %}

### Tips

- Normalize commands to uppercase to avoid case mismatches.
- Use `response_delay` and `response_jitter` to emulate slow hardware.
- Validate mappings with MiL tests against SPX Server (see `spx-examples` [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml) and [`scpi_multimeter_sut_example.py`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/tests/shared/integration/scpi_multimeter_sut_example.py)).
