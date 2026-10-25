---
icon: react
---

# Actions Library

Actions run within a model's cycle. The first key selects the registered action
and its target; sibling fields configure it. Use the complete
[model reference](../simulation-and-modeling/model-definition-reference.md)
for expression and action semantics. These fragments assume the named
attributes already exist.

## Ramp example

```yaml
actions:
  - ramp: $in(voltage_v)
    start_value: 0.0
    stop_value: 230.0
    duration: 5.0
    type: linear
```

Time-aware actions require a model timer. A manual test must advance that timer
or run with an explicit time step; a loop that repeatedly reads a value does not
advance a deterministic simulation.

## PID example

```yaml
actions:
  - pid: $in(heater_power_w)
    setpoint: $in(k__temperature_c)
    input: $in(temperature_c)
    kp: 2.0
    ki: 0.5
    kd: 0.1
```

The input field is `input`, not `feedback`. Tune gains for the model and units.

## Noise injection

```yaml
actions:
  - noise: $out(temperature_c)
    std: 0.01
    mode: proportional
```

Internal values represent simulation state; external values can represent a
noisy measurement exposed to protocols.

## Overrides and suspend

```yaml
actions:
  - overrides:
      $in(k__fan_speed_rpm): 1000.0
  - suspend:
      paths: [actions.ramp]
```

Overrides are a mapping of path → value. Suspend uses `paths` (or its supported
aliases) for component targets. They capture state on preparation and restore
it on stop. Use a scenario's `duration` to limit an effect; do not invent
per-action duration fields for these lifecycle operations. `set` and `function`
write materialized values which remain after a scenario stops.

## Best practices

Keep actions deterministic where tests require it. Set stable action names when
other components refer to their paths, parameterize communication separately,
and validate complete models against the released runtime. A registered custom
action requires implementation in the relevant runtime/extension, not only a
new YAML name.
