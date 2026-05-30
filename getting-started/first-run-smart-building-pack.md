---
description: >-
  First-run UI walkthrough after installing the Smart Building Pack with the
  current spx-examples installer.
---

# Smart Building Pack: First Run Walkthrough

This walkthrough assumes you generated and started the Smart Building Pack from
the installer or from `spx-examples`:

```bash
python -m installer generate \
  --packages smart_building_pack \
  --profile-ids bms_quickstart \
  --with-ui \
  --output build/spx-generated

cd build/spx-generated
./spx-start.sh
```

On Windows, use `pwsh ./spx-start.ps1` from the generated folder.

The current `bms_quickstart` profile includes MQTT, LwM2M/CoAP, HTTP, Modbus,
OPC UA, KNX, Matter, BACnet, Home Assistant, and SPX UI. The installer caps the
starter instance set to 5 running instances so the first run works with the
default licensing path.

## Starter instances

After startup, these instances should exist and be started:

| Instance | Model |
| --- | --- |
| `HVAC_Flexit_Nordic_BACnet` | `Building.HvacFlexitNordic.Bacnet` |
| `Energy_Meter_iEM3000_Modbus` | `Energy.EnergyMeterIem3000.Modbus` |
| `Victron_Cerbo_GX_ESS_Modbus` | `Energy.ESS.VictronCerboGx.Modbus` |
| `Weather_Gateway_WAGO_PFC200_Vaisala_WXT530_MQTT` | `Weather.WeatherGateway.WagoPfc200.VaisalaWxt530.Mqtt` |
| `Building_Physics` | `Building.Physics.Generic` |

The pack also contains many additional models, including lighting, safety,
security, room control, energy meters, PV physics, Matter devices, and Home
Assistant bridge assets. They are available in the generated bundle and catalog
even when only the starter instances run initially.

## Verify services

From the generated folder:

```bash
docker compose -f docker-compose.generated.yml --env-file .env ps
curl -fsS http://localhost:8000/health
```

Open:

- SPX UI: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`
- Home Assistant: `http://localhost:8123`

Home Assistant demo login:

- Username: `admin`
- Password: `spx-examples`

## UI walkthrough

1. Open `http://localhost:3000`.
2. Open the Instances view and confirm the 5 starter instances are listed.
3. Open `Weather_Gateway_WAGO_PFC200_Vaisala_WXT530_MQTT`.
4. Inspect attributes such as `k__outdoor_temperature_c` and
   `k__brightness_lux`. These are the attributes used by the Smart Building
   weather gateway notebook in `spx-examples`.
5. Open `Building_Physics` and confirm it is available for weather and energy
   interactions.
6. Open `Victron_Cerbo_GX_ESS_Modbus` and
   `Energy_Meter_iEM3000_Modbus` to confirm the energy devices are present.
7. Open the Logs or Logger view and confirm there are no startup errors.

Learn the UI structure here: [UI Overview](../ui-reference/general-view.md).

## Home Assistant walkthrough

1. Open `http://localhost:8123`.
2. Log in with the demo credentials above.
3. Confirm the SPX dashboard/theme loads and the bridge can reach `spx-server`.
4. Use Home Assistant as a high-level dashboard for the BMS demo, while SPX UI
   remains the primary tool for inspecting model attributes, logs, and runtime
   state.

## Optional notebook walkthrough

For a scripted flow, use the Smart Building notebook in `spx-examples`:

```bash
cd /path/to/spx-examples
jupyter notebook examples/packs/smart_building_pack/smart_building_pack_weather_gateway.ipynb
```

The notebook checks instance state and updates
`k__outdoor_temperature_c` and `k__brightness_lux` on the weather gateway
instance.

## Pass criteria

- `/health` returns JSON with `"status":"ok"`.
- SPX UI loads at `http://localhost:3000`.
- The 5 starter instances are visible.
- Weather Gateway, Building Physics, Victron ESS, and iEM3000 can be opened in
  the UI.
- Home Assistant loads at `http://localhost:8123` when the Smart Building Pack
  was generated with its default services.
- Logs show no startup errors during the check.

## If something fails

- See [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md).
- Use [How to Get Support](../troubleshooting-and-support/how-to-get-support.md) to collect logs and contact the team.
