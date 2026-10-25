# Connections

Connections propagate a source attribute value into a target input. They are
runtime components under the System `connections` container.

```yaml
connections:
  weather_to_building:
    from: $out(weather.outdoor_temperature_c)
    to: $in(building.k__outdoor_temperature_c)
```

Equivalent JSON:

```json
{
  "connections": {
    "weather_to_building": {
      "from": "$out(weather.outdoor_temperature_c)",
      "to": "$in(building.k__outdoor_temperature_c)"
    }
  }
}
```

The referenced instances must already exist. `from` is read, and `to` is
written. `$out` selects external telemetry; `$in` selects internal control
state. Prefer persistent inputs, commonly `k__*`, as targets. `cmd__*` is for
explicit one-shot command flows rather than continuous propagation.

## Lifecycle and propagation

Start both the global connections container and the individual connection.
A loaded/imported connection can still be `INITIALIZED`; existence alone does
not prove it is active. Running connections subscribe to source changes and
also support an explicit `run()` for immediate propagation. Stop/disable detaches
the source hook. Unresolved endpoints are reported during load or diagnostics;
recreated instances require the connection to resolve its live endpoints again.

For MCP work, prefer structured endpoint arguments on `server_upsert_connection`,
then check state and propagation as described in the
[MCP reference](../../getting-started/mcp-reference.md#runtime-connection-workflow).
Use a calculated source action if scaling or arithmetic is needed. Continuous
propagation can overwrite a target user's manual input, so choose the target
according to the requested control relationship.
