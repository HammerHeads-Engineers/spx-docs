# Parameters

SPX distinguishes deployment inputs from initial model state.

## Communication and provisioning parameters

Declare `meta_parameters` in a reusable model and bind values with `$param(...)`.
Provide the instance's concrete `meta_parameters` at creation. Use this for
hostnames, ports, unit IDs, topics and other instance-specific transport wiring.
Keep ordinary simulation tuning in model attributes.

```yaml
meta_parameters:
  ascii_port: {type: int, default: 0}
communication:
  - ascii:
      port: $param(ascii_port)
      bindings: []
```

Port zero permits runtime assignment for multi-instance ASCII devices.

## Initial attribute values

`init_parameters` is the registered initialization container in the RC76 runtime
(`spx_core/system/init_parameters.py`). It assigns existing attribute wrappers
when the definition is populated; it is not a generic `parameters` container.

```yaml
attributes:
  k__setpoint_c: {type: float, default: 20.0, unit: degC}
init_parameters:
  $in(k__setpoint_c): 25.0
```

The mapping must refer to attributes that already exist. An unknown name is an
error. `$in` selects the internal value; `$ext` selects the external value.
For API/client construction examples, use the
[model reference](../../simulation-and-modeling/model-definition-reference.md)
and the matching Python client helper documentation.
