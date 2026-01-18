# Redfish adapters

SPX Server ships two Redfish components:

- `redfish` — Redfish client (HTTP / loopback transport)
- `redfish_server` — in-memory loopback server used for tests and tooling

## `redfish` (client)

**YAML key:** `redfish`

Minimal example (HTTP transport):

```yaml
attributes:
  power_state: "Off"

communication:
  - redfish:
      transport: http
      base_url: "https://example-redfish.local"
      verify_tls: true
      auth:
        username: admin
        password: changeme
      poll_interval: 5.0
      bindings:
        - name: system_state
          direction: inbound
          method: GET
          resource: /redfish/v1/Systems/1
          pointer: /PowerState
          attribute: "#attr(power_state)"
```

## `redfish_server` (loopback server)

**YAML key:** `redfish_server`

```yaml
attributes:
  boot_target: "Hdd"

communication:
  - redfish_server:
      transport: loopback
      bindings:
        - name: boot_override
          direction: inbound
          method: PATCH
          resource: /redfish/v1/Systems/1
          pointer: /Boot/BootSourceOverrideTarget
          attribute: "#attr(boot_target)"
```

## Notes

- The loopback server is in-memory and is primarily used by the loopback transport in tests.
- Pointer syntax is JSON Pointer-like.
