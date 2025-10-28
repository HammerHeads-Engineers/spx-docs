# Instances Container

The `Instances` container (`spx_core/system/instances.py`) creates and manages nested components inside your model. Use it to wire multiple devices together or to reuse the same blueprint several times.

## YAML structure

```yaml
instances:
  - sensor:
      type: library/temperature_sensor
      parameters:
        attributes.temperature.default: 25.0
  - controller:
      type: library/pid_controller
      parameters:
        parameters.setpoint: 80.0
  - fleet:
      type: library/device_cluster
      instances:
        - node:
            type: library/edge_node
```

### Configuration options

| Field | Description |
|-------|-------------|
| `type` | Required class or template name registered in the core. |
| `parameters` | Mapping applied after instantiation. Keys can reference nested attributes (see examples). |
| `instances` | Embedded list that creates grandchildren under this instance. |
| (no `type`) | If an entry omits `type`, the container treats it as an update to an existing child. |

### Behavior details

- **List or dict**: You can provide a list of single-key dicts (recommended) or a plain mapping; the container normalizes the format internally.
- **Limit enforcement**: You can set `instance_limit` when creating the container programmatically to prevent runaway instantiations.
- **Updates**: Supplying an entry without `type` (only parameters) updates an existing child instead of creating a new one. This is useful for hot reconfiguration via API.
- **Nested sections**: Additional keys in the same mapping (after the first) are treated as sub-containers to attach under the new instance.

### Example: updating an instance at runtime

```yaml
instances:
  - sensor:
      type: library/temperature_sensor
  - sensor:
      calibration:
        offset: 0.5
```

The second entry finds the existing `sensor` child and applies the `calibration` block without recreating the object.

### Tips for junior engineers / QA

- Start with one instance at a time; confirm it loads before adding nested devices.
- When something fails to load, check server logs—the container will raise a descriptive error if the class name is missing from the registry.
- Use meaningful names; they appear in diagnostics paths (`models.plant.instances.sensor`).
- Pair instances with `connections` to route signals between them.
