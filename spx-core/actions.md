# Actions Library

The server core bundles a set of action classes under `spx_core/actions`. They run inside the simulation loop to evolve attribute values over time. Each action inherits from the same base you use in the SDK, but the server version is optimized and instrumented for production logging.

## How actions are structured

- `ramps.py`: ramp, step, and integrator functions for smooth transitions.
- `saws.py`: sawtooth generators, useful for repetitive test signals.
- `interpolate.py`: linear/multi-point interpolation between samples.
- `noises.py`: additive and multiplicative noise injection.
- `pid.py`: PID controller implementation that reads error attributes and writes control outputs.
- `overrides.py`: temporary overrides (`force`, `restore`).
- `suspend.py`: pause/resume other actions.
- `call.py`: call arbitrary registered functions with resolved parameters.

Each action consumes a YAML block in the `actions:` list. Parameters are evaluated just like in the SDK (`#attr`, `#external`, expressions).

### Ramp example

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - ramp:
      output: "#attr(voltage)"
      start_value: 0.0
      stop_value: 230.0
      duration: 5.0
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "ramp": {
        "output": "#attr(voltage)",
        "start_value": 0.0,
        "stop_value": 230.0,
        "duration": 5.0
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

### PID example

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - pid:
      output: "#attr(heater_power)"
      setpoint: "#attr(target_temperature)"
      feedback: "#attr(current_temperature)"
      kp: 2.0
      ki: 0.5
      kd: 0.1
      sample_time: 0.1
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "pid": {
        "output": "#attr(heater_power)",
        "setpoint": "#attr(target_temperature)",
        "feedback": "#attr(current_temperature)",
        "kp": 2.0,
        "ki": 0.5,
        "kd": 0.1,
        "sample_time": 0.1
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

### Noise injection

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - noise:
      output: "#attr(sensor.reading)"
      std: 0.01
      mode: proportional
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "noise": {
        "output": "#attr(sensor.reading)",
        "std": 0.01,
        "mode": "proportional"
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

### Overrides and suspend

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - override:
      target: "#attr(fan_speed)"
      value: 1000
      duration: 2.0
  - suspend:
      target_actions: ["ramp", "pid"]
      duration: 1.0
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "override": {
        "target": "#attr(fan_speed)",
        "value": 1000,
        "duration": 2.0
      }
    },
    {
      "suspend": {
        "target_actions": ["ramp", "pid"],
        "duration": 1.0
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

## Best practices

- Place critical control loops (PID, overrides) at the top of the list so they execute first.
- Use `suspend` to temporarily disable other actions during fault injection.
- Combine ramps with noise to emulate realistic sensor behavior.
- Keep durations explicit; otherwise actions may run indefinitely.
