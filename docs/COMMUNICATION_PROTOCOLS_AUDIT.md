# Communication protocols: spx-server inventory vs spx-docs coverage

This note inventories protocol components implemented in `spx-server/spx_core/communications`, their test coverage in `spx-server/tests/test_spx_core/test_communications`, and the current documentation coverage in `spx-docs`.

Audit inputs (local workspace):

- `spx-server` @ `62a0350`
- `spx-docs` @ `981529e`

## Implemented protocol components (YAML keys)

SPX Server registers protocol components via `@register_class(name="...")` under `spx-server/spx_core/communications`.

| YAML key (`register_class`) | Implementation (spx-server) | Tests (spx-server) | spx-docs coverage | Notes |
|---|---|---|---|---|
| `ascii` | `spx_core/communications/ascii/ascii.py` | `tests/test_spx_core/test_communications/test_ascii/*` | `spx-core/communications/ascii.md` | Docs seem aligned with current code (terminator, mappings, delay/jitter). |
| `http_endpoint` | `spx_core/communications/http/http_endpoint.py` | `tests/test_spx_core/test_communications/test_http/*` | `spx-core/communications/http.md` | Docs aligned with `http_endpoint` + `endpoints` (examples + schema notes). |
| `mqtt` | `spx_core/communications/mqtt/server.py` | `tests/test_spx_core/test_communications/test_mqtt/*` | `spx-core/communications/mqtt.md` | Docs aligned with bindings-based MQTT config (`broker`, `bindings`, QoS/retain, payload codecs). |
| `mqtt-ha` | `spx_core/communications/mqtt/ha_server.py` | `tests/test_spx_core/test_communications/test_mqtt/*` | `spx-core/communications/mqtt.md` | Included as a dedicated section (`brokers`, availability, discovery). |
| `ble` | `spx_core/communications/ble/ble_protocol.py` | `tests/test_spx_core/test_communications/test_ble/*` | `spx-core/communications/ble.md` | Docs appear to match current config shape (`adapter.baseUrl`, polling, codecs/bindings). |
| `modbus_tcp` | `spx_core/communications/modbus/modbus_tcp.py` | `tests/test_spx_core/test_communications/test_modbus_tcp/*` + API v3: `tests/test_spx_server/test_api_v3/test_modbus_*` | `spx-core/communications/modbus.md` | Documented as a legacy/compat adapter (avoid for new models; prefer `modbus_slave`). |
| `modbus_slave` | `spx_core/communications/modbus_slave/server.py` | `tests/test_spx_core/test_communications/test_modbus/*` | `spx-core/communications/modbus.md` | Documented (auto-port behaviour, mapping vs bindings, blackhole `detach/attach`). |
| `modbus_master` | `spx_core/communications/modbus_master/master.py` | `tests/test_spx_core/test_communications/test_modbus_master/*` | `spx-core/communications/modbus.md` | Documented (binding-based poller/client, inbound/outbound). |
| `bacnet` | `spx_core/communications/bacnet/bacnet.py` | `tests/test_spx_core/test_communications/test_bacnet/*` | `spx-core/communications/bacnet.md` | Minimal config + links to tests and `spx-examples` models. |
| `coap_server` | `spx_core/communications/coap/server.py` | `tests/test_spx_core/test_communications/test_coap/*` | `spx-core/communications/coap.md` | Minimal config + link to tests. |
| `dali` | `spx_core/communications/dali/client.py` | `tests/test_spx_core/test_communications/test_dali/*` | `spx-core/communications/dali.md` | Minimal config + link to tests. |
| `knx_ip` | `spx_core/communications/knx/knx_ip.py` | `tests/test_spx_core/test_communications/test_knx/*` | `spx-core/communications/knx.md` | Documented with a real `spx-examples` model. |
| `knx_ip_simulator` | `spx_core/communications/knx/simulator.py` | `tests/test_spx_core/test_communications/test_knx/*` | `spx-core/communications/knx.md` | Documented alongside `knx_ip`. |
| `lwm2m` | `spx_core/communications/lwm2m/client.py` | `tests/test_spx_core/test_communications/test_lwm2m/*` | `spx-core/communications/lwm2m.md` | Documented from server tests (spx-examples LwM2M model currently differs). |
| `matter` | `spx_core/communications/matter/server.py` | `tests/test_spx_core/test_communications/test_matter/*` | `spx-core/communications/matter.md` | Minimal config + link to tests and `spx-examples` model. |
| `mbus` | `spx_core/communications/mbus/client.py` | `tests/test_spx_core/test_communications/test_mbus/*` | `spx-core/communications/mbus.md` | Documented alongside `mbus_server`. |
| `mbus_server` | `spx_core/communications/mbus/server.py` | `tests/test_spx_core/test_communications/test_mbus/*` | `spx-core/communications/mbus.md` | Documented alongside `mbus`. |
| `ocpp` | `spx_core/communications/ocpp/protocol.py` | `tests/test_spx_core/test_communications/test_ocpp/*` | `spx-core/communications/ocpp.md` | Minimal config + link to tests and `spx-examples` models (EVSE + CSMS). |
| `opcua_server` | `spx_core/communications/opcua/opcua_server.py` | `tests/test_spx_core/test_communications/test_opcua/test_opcua_integration.py` | `spx-core/communications/opcua.md` | Minimal config + link to example model; tests are integration-style (and may be skipped in default runs). |
| `profinet_server` | `spx_core/communications/profinet/server.py` | `tests/test_spx_core/test_communications/test_profinet/*` | `spx-core/communications/profinet.md` | Documented (bindings + legacy mapping conversion + transport selection). |
| `profinet_snap7_adapter` | `spx_core/communications/profinet/server.py` | `tests/test_spx_core/test_communications/test_profinet/*` | `spx-core/communications/profinet.md` | Documented as a `profinet_server.transport` option (requires `python-snap7`). |
| `redfish` | `spx_core/communications/redfish/client.py` | `tests/test_spx_core/test_communications/test_redfish/*` | `spx-core/communications/redfish.md` | Documented alongside `redfish_server`. |
| `redfish_server` | `spx_core/communications/redfish/server.py` | `tests/test_spx_core/test_communications/test_redfish/*` | `spx-core/communications/redfish.md` | Documented alongside `redfish`. |
| `snmp` | `spx_core/communications/snmp/client.py` | `tests/test_spx_core/test_communications/test_snmp/*` | `spx-core/communications/snmp.md` | Documented alongside `snmp_server`. |
| `snmp_server` | `spx_core/communications/snmp/server.py` | `tests/test_spx_core/test_communications/test_snmp/*` | `spx-core/communications/snmp.md` | Documented alongside `snmp`. |

Additional shared test coverage:

- Protocol binding helpers: `spx-server/tests/test_spx_core/test_communications/test_bindings.py`

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

No occurrences of the “advanced” protocol names (BACnet / CoAP / DALI / KNX / LwM2M / Matter / M-Bus / OCPP / OPC UA / PROFINET / Redfish / SNMP) were found in `spx-docs` outside excluded sections.

## Remaining gaps / follow-ups

- Align the `spx-examples` LwM2M model schema with `spx-server` (`lwm2m` bindings-based schema is the current contract).
- Keep cross-doc pages consistent: `spx-development-guide/spx-sdk/communication.md` must not document fictional built-in adapters (`http_api`, `SimpleHttp`, etc.). Prefer linking to `spx-core/communications/**` and grounding examples in `spx-server` tests / `spx-examples`.
