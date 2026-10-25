# Protocol capabilities and verification scope

This matrix describes adapter roles in server RC76, not certification or a claim
that every physical deployment has been tested. Reference review is evidence of
configuration support; verify the selected transport with your SUT separately.
The documentation contracts do not execute these protocol/hardware checks.

| Adapter | SPX role / SUT counterpart | Required backend or environment | Limits and verification |
| --- | --- | --- | --- |
| [ASCII / SCPI](ascii.md) | TCP instrument endpoint / instrument client | mapped TCP port | Command dialect is model-defined; test the actual driver |
| [HTTP](http.md) | HTTP endpoint / HTTP client | reachable mapped port | Model routes differ from the SPX control API |
| [MQTT](mqtt.md) | publisher/subscriber / broker-connected application | external broker, topics and credentials | Broker routing, retain and QoS affect observations |
| [Modbus](modbus.md) | server or active master / complementary Modbus peer | TCP port, unit IDs and register map | Test codec, byte order, read/write direction and role |
| [OPC UA](opcua.md) | server / OPC UA client | endpoint, namespace and security configuration | Test exact node IDs and access policy |
| [BACnet](bacnet.md) | BACnet/IP endpoint / BMS client | UDP reachability and device ID | Broadcast discovery can require host/network setup |
| [KNX](knx.md) | IP bindings or local simulator / KNX peer | tunnel/router or supported simulator backend | Simulator behavior is not physical-bus qualification |
| [BLE](ble.md) | SPX bridge to peripheral service / BLE central | separate host BLE adapter, compatible OS/Bluetooth hardware | Container-only execution does not provide a host radio |
| [PROFINET / Snap7](profinet.md) | attribute bridge via configured transport / Siemens S7 peer | optional Snap7 transport and reachable PLC | Snap7 uses S7 TCP, not a complete PROFINET IO real-time device stack |
| [Matter](matter.md) | controller integration / commissioned Matter node | python-matter-server WebSocket controller and its CHIP environment | Does not itself emulate a commissioned Matter device |
| [CoAP](coap.md) | CoAP server / CoAP client | reachable CoAP endpoint | Verify resources and payload codecs |
| [LwM2M](lwm2m.md) | client / LwM2M server | reachable server, endpoint identity | Verify registration and object/resource support |
| [OCPP](ocpp.md) | configured client or server / complementary OCPP peer | WebSocket endpoint and identity | Reference targets OCPP 1.6J; verify supported messages |
| [DALI](dali.md) | client bindings / DALI backend | configured bus/backend access | Physical interface and backend are deployment prerequisites |
| [M-Bus](mbus.md) | client or server / complementary meter peer | configured transport/backend | Verify actual medium and supported telegrams |
| [SNMP](snmp.md) | client or agent / manager or agent peer | reachable endpoint and configured credentials/OIDs | Verify operations and version/security settings |
| [Redfish](redfish.md) | client or server / complementary management peer | HTTP endpoint and credentials | Verify implemented resources, not the entire standard |

For each qualification record: bundle versions, OS/container network, adapter
backend, model commit, SUT/version, endpoint parameters, read/write checks and
expected results. Mark hardware not exercised explicitly. Keep hostnames, ports,
IDs and topics in model `meta_parameters` bound by `$param(...)`.
