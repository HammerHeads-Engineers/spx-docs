---
icon: satellite-dish
---

# Communication Adapters

SPX Server implements protocol adapters in its server runtime.

**Source of truth (in priority order):**

1) Implementation: SPX Server runtime
   - The YAML key is the `@register_class(name="...")` value.
2) Runnable examples: `spx-examples/library/domains/**`

## Shared concepts

- **Model YAML shape**: `communication` can be a mapping or a list (list form also supports multiple adapters of the same kind).
  - Prefer the list form when you need more than one adapter and when you want unknown adapter keys to fail fast.
- **Lifecycle**: adapters typically implement `prepare` → `start` → `stop` → `release` (some also support `attach` / `detach`).
- **Bindings**: most adapters map protocol I/O onto attributes using binding entries (`direction`, `attributes` / `read_attribute` / `write_attribute`).
- **Scenarios**: scenarios can override adapter properties at runtime (latency, disconnects, blackholes) to test client behavior.

## Adapter index

**Common**

- [ASCII / SCPI (`ascii`)](ascii.md) — TCP text protocols (SCPI-style).
- [HTTP endpoint (`http_endpoint`)](http.md) — REST-style endpoints backed by attributes.
- [MQTT (`mqtt`, `mqtt-ha`)](mqtt.md) — publish/subscribe bindings + Home Assistant discovery variant.
- [Modbus (`modbus_slave`, `modbus_tcp`, `modbus_master`)](modbus.md) — Modbus TCP server(s) + Modbus client.
- [BLE (`ble`)](ble.md) — bridges to the standalone `spx-ble-adapter`.

**Automation / industrial**

- [BACnet (`bacnet`)](https://docs.simplephysx.com/spx-development-guide/spx-core/system/templates/communications/bacnet) — BACnet/IP objects, schedules, alarms.
- [KNX IP (`knx_ip`, `knx_ip_simulator`)](knx.md) — KNXnet/IP routing + local simulator.
- [OPC UA server (`opcua_server`)](opcua.md) — exposes nodes via `opc.tcp://...`.
- [PROFINET (`profinet_server`, `profinet_snap7_adapter`)](profinet.md) — PROFINET server and Snap7-based adapter.
- [DALI (`dali`)](dali.md) — DALI client bindings.
- [M-Bus (`mbus`, `mbus_server`)](mbus.md) — M-Bus client + server.

**IoT / device clouds**

- [CoAP server (`coap_server`)](coap.md) — CoAP endpoints with bindings.
- [LwM2M client (`lwm2m`)](lwm2m.md) — LwM2M client registrations + resources.
- [Matter (`matter`)](matter.md) — Matter controller integration over WebSocket.
- [OCPP (`ocpp`)](ocpp.md) — OCPP 1.6J client/server roles.

**Management**

- [SNMP (`snmp`, `snmp_server`)](snmp.md) — SNMP client + agent.
- [Redfish (`redfish`, `redfish_server`)](redfish.md) — Redfish client + server.

Tips:

* Keep instance-specific protocol ports/config in `meta_parameters` and bind with `$param(...)` so deployments can override them per environment.
* Prefer spx-examples models as runnable references for adapter behavior.
* Use scenarios for chaos testing (`detach`, delay spikes, message drops) and validate via MiL tests.

## Scope of support and verification

Adapter implementation does not imply that every physical bus or vendor device
has been hardware-qualified. The reference models are simulations, not certified
manufacturer twins. Read each adapter page for roles, transport limitations and
optional external bridges. In particular, a Snap7 bridge is not proof of a full
PROFINET IO device stack, Matter requires a controller service, and BLE requires
the separately installed host adapter and suitable host Bluetooth support.

Bind configurable hostnames, ports, device identifiers and topics using
`meta_parameters`; keep these independent from model behavior attributes.
The documentation audit records source review separately from protocol and
hardware execution evidence.

Before selecting an adapter, check [roles, backends and verification limits](capabilities.md).
