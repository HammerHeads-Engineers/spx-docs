# Communication protocols: SPX Server inventory vs spx-docs coverage

This note inventories protocol components implemented in SPX Server and the current documentation coverage in spx-docs.

## Implemented protocol components (YAML keys)

SPX Server registers protocol components via `@register_class(name="...")`.

| YAML key (`register_class`) | spx-docs coverage | Notes |
|---|---|---|
| `ascii` | `spx-core/communications/ascii.md` | Docs aligned with current adapter behavior (terminator, mappings, delay/jitter). |
| `http_endpoint` | `spx-core/communications/http.md` | Docs aligned with `http_endpoint` + `endpoints` (examples + schema notes). |
| `mqtt` | `spx-core/communications/mqtt.md` | Docs aligned with bindings-based MQTT config (`broker`, `bindings`, QoS/retain, payload codecs). |
| `mqtt-ha` | `spx-core/communications/mqtt.md` | Included as a dedicated section (`brokers`, availability, discovery). |
| `ble` | `spx-core/communications/ble.md` | Docs appear to match current config shape (`adapter.baseUrl`, polling, codecs/bindings). |
| `modbus_tcp` | `spx-core/communications/modbus.md` | Documented as a legacy/compat adapter (avoid for new models; prefer `modbus_slave`). |
| `modbus_slave` | `spx-core/communications/modbus.md` | Documented (auto-port behaviour, mapping vs bindings, blackhole `detach/attach`). |
| `modbus_master` | `spx-core/communications/modbus.md` | Documented (binding-based poller/client, inbound/outbound). |
| `bacnet` | `spx-core/communications/bacnet.md` | Minimal config + links to spx-examples models. |
| `coap_server` | `spx-core/communications/coap.md` | Minimal config example included. |
| `dali` | `spx-core/communications/dali.md` | Minimal config example included. |
| `knx_ip` | `spx-core/communications/knx.md` | Documented with a real spx-examples model. |
| `knx_ip_simulator` | `spx-core/communications/knx.md` | Documented alongside `knx_ip`. |
| `lwm2m` | `spx-core/communications/lwm2m.md` | Docs note that the spx-examples LwM2M model uses an older schema. |
| `matter` | `spx-core/communications/matter.md` | Minimal config + link to spx-examples model. |
| `mbus` | `spx-core/communications/mbus.md` | Documented alongside `mbus_server`. |
| `mbus_server` | `spx-core/communications/mbus.md` | Documented alongside `mbus`. |
| `ocpp` | `spx-core/communications/ocpp.md` | Minimal config + link to spx-examples models (EVSE + CSMS). |
| `opcua_server` | `spx-core/communications/opcua.md` | Minimal config + link to example model. |
| `profinet_server` | `spx-core/communications/profinet.md` | Documented (bindings + legacy mapping conversion + transport selection). |
| `profinet_snap7_adapter` | `spx-core/communications/profinet.md` | Documented as a `profinet_server.transport` option (requires `python-snap7`). |
| `redfish` | `spx-core/communications/redfish.md` | Documented alongside `redfish_server`. |
| `redfish_server` | `spx-core/communications/redfish.md` | Documented alongside `redfish`. |
| `snmp` | `spx-core/communications/snmp.md` | Documented alongside `snmp_server`. |
| `snmp_server` | `spx-core/communications/snmp.md` | Documented alongside `snmp`. |

## Documentation status (spx-docs today)

Current adapter pages in `spx-docs/spx-core/communications/`:

- ✅ `README.md` (routing hub listing all implemented keys)
- ✅ `ascii.md`
- ✅ `http.md`
- ✅ `mqtt.md` (includes `mqtt-ha`)
- ✅ `modbus.md` (covers `modbus_slave`, `modbus_tcp`, `modbus_master`)
- ✅ `ble.md`
- ✅ `bacnet.md`
- ✅ `coap.md`
- ✅ `dali.md`
- ✅ `knx.md`
- ✅ `lwm2m.md`
- ✅ `matter.md`
- ✅ `mbus.md`
- ✅ `ocpp.md`
- ✅ `opcua.md`
- ✅ `profinet.md`
- ✅ `redfish.md`
- ✅ `snmp.md`

No occurrences of the "advanced" protocol names (BACnet / CoAP / DALI / KNX / LwM2M / Matter / M-Bus / OCPP / OPC UA / PROFINET / Redfish / SNMP) were found in `spx-docs` outside excluded sections.

## Remaining gaps / follow-ups

- Align the spx-examples LwM2M model schema with the current bindings-based schema.
- Keep cross-doc pages consistent: `spx-development-guide/spx-sdk/communication.md` must not document fictional built-in adapters (`http_api`, `SimpleHttp`, etc.). Prefer linking to `spx-core/communications/**` and grounding examples in spx-examples.
