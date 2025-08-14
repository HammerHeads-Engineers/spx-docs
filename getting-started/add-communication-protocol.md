# Adding a Communication Protocol (Modbus TCP) to Your Simulation

Communication protocols are a first‑class part of SPX simulations: they expose your simulated signals to external tools (HMIs, test rigs, PLCs) and let real software interact with the model as if it were physical hardware. In this step we wire our **PT100‑style temperature sensor** from *Build Your First Simulation* to **Modbus TCP** so any Modbus client can read the sensor value and a binary fault flag.

**What is Modbus TCP?** It is a widely used industrial protocol over TCP/IP. In SPX it ships **natively in the Core library**, so you can enable it directly in your model—no extra installation required.

```python
# All comments in English only.
import os
import yaml
import spx_python

# 1) Connect to the running SPX Server
client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY", "")  # required env var
)

# 2) Define the model (PT100-like sensor) + Modbus TCP mapping
pt_100_yaml = '''
attributes:
  temperature: 25.0
  sensor_fault: 0
actions:
  - { ramp: $in(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5}
  - { noise: $out(temperature), std: 0.01, mode: proportional}
communication:
  - modbus_tcp:
      mapping:
        temperature: {address: [0,1], group: h_r, type: uint_32}
        sensor_fault: {address: [4], group: c, type: uint_16}
'''

# 3) Register the model and create an instance
model_def = yaml.safe_load(pt_100_yaml)
client["models"]["pt_100_modbus"] = model_def
client["instances"]["pt100_mb_1"] = "pt_100_modbus"
inst = client["instances"]["pt100_mb_1"]

# 4) Step deterministically (so external tools see changing readings)
client.prepare()
for k in range(1, 51):  # ~5 seconds with dt=0.1
    inst["timer"]["time"] = k * 0.1
    client.run()

print("internal temperature:", inst["attributes"]["temperature"].internal_value)
print("external temperature:", inst["attributes"]["temperature"].external_value)
print("sensor_fault:", inst["attributes"]["sensor_fault"].internal_value)
# A Modbus TCP client can now read temperature at holding registers 0-1 and power at 2-3.
```

In this configuration:

- `port` and `host` define where the Modbus TCP server listens. **Defaults:** `port` = **502**, `host` = **127.0.0.1** (or `localhost`). You only need to declare them if you want a custom interface.
- `data_encoding` defines byte order for values. **Default:** **Big Endian**.
- `mapping` binds model attributes to Modbus tables and addresses:
  - `temperature` → `group: h_r` (holding registers), `address: [0, 1]`, `type: uint_32` — the value spans two consecutive 16‑bit registers.
  - `sensor_fault` → `group: c` (coils), `address: [4]`, `type: uint_16` — a binary 0/1 flag indicating sensor contact fault.

**Attributes in this model**
- `temperature` (float) — internal logic drives the true value; external presentation may include noise.
- `sensor_fault` (0/1) — a binary flag you can set from the simulation (or a test) to indicate a contact error.

With this setup, any Modbus TCP client can read the **temperature** from holding registers **0–1** and the **sensor_fault** flag from coil **4** in real time while the simulation advances deterministically.

## Quick Verification with a Modbus TCP Client

To verify the Modbus TCP server is working correctly, create a simple Python client that connects to `localhost:502`, reads the mapped registers, and plots the temperature and fault flag. This example also demonstrates **Model‑in‑the‑Loop (MiL)**: the **Software Under Test (SUT)** is the Modbus TCP client (your real application code), while the **SPX model** plays the role of the plant/sensor. We use `spx-python` only as a control channel to start/stop the model so data capture stays in sync.

**Note:** Unlike the deterministic stepping shown earlier (where you set `instance["timer"]["time"]` and call `run()`), here we call `start()`, which hands time progression to the server’s internal scheduler. The simulation advances autonomously according to `timer.dt` and the server loop—great for live protocol testing—while deterministic stepping remains preferable for strictly reproducible unit tests.

```python
# All comments in English only.
import os
import time
import matplotlib.pyplot as plt
from pymodbus.client.sync import ModbusTcpClient
import spx_python


class SUTSensor:
    """Software Under Test (SUT): thin Modbus TCP wrapper for reading measurements.
    Hides protocol details from the test/plotting logic.
    """
    def __init__(self, host="127.0.0.1", port=502, unit=1, scale=100.0):
        self.host = host
        self.port = port
        self.unit = unit
        self.scale = scale
        self._mb = None

    def connect(self):
        self._mb = ModbusTcpClient(self.host, port=self.port)
        assert self._mb.connect(), f"Could not connect to Modbus server at {self.host}:{self.port}"

    def read_temperature_and_fault(self):
        """Temperature from HR 0–1 (uint32 Big Endian), fault flag from coil 4 (0/1)."""
        # Read temperature (two 16-bit holding registers)
        rr = self._mb.read_holding_registers(0, 2, unit=self.unit)
        if rr.isError():
            temp = None
        else:
            raw = (rr.registers[0] << 16) + rr.registers[1]
            temp = raw / self.scale  # adjust scaling to your model if needed

        # Read fault flag (coil 4)
        rc = self._mb.read_coils(4, 1, unit=self.unit)
        fault = None if rc.isError() else int(rc.bits[0])

        return temp, fault

    def close(self):
        if self._mb:
            self._mb.close()
            self._mb = None


# 1) Control channel: connect to the running SPX Server
spx_client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY", "")  # required env var
)

# 2) Get the model instance (created earlier in the guide)
model = spx_client["instances"]["pt100_mb_1"]  # adjust if you used a different name

# 3) SUT: Modbus client
sensor = SUTSensor(host="127.0.0.1", port=502, unit=1, scale=100.0)
sensor.connect()

temperatures, fault_flags, timestamps = [], [], []

# 4) Start model, capture synchronously (server scheduler advances time)
model.reset()
model.start()
try:
    for i in range(50):  # ~5 seconds at 0.1 s interval
        temp, fault = sensor.read_temperature_and_fault()
        temperatures.append(temp)
        fault_flags.append(fault)
        timestamps.append(i * 0.1)
        time.sleep(0.1)  # optional: align with dt for easier inspection
finally:
    model.stop()
    sensor.close()

# 5) Plot results
plt.figure(figsize=(10, 4))
plt.subplot(2, 1, 1)
plt.plot(timestamps, temperatures, label="Temperature (HR 0–1)")
plt.ylabel("Temperature")
plt.legend()

plt.subplot(2, 1, 2)
plt.step(timestamps, fault_flags, label="Sensor Fault (coil 4)", where="post")
plt.ylabel("Fault Flag")
plt.xlabel("Time (s)")
plt.legend()
plt.tight_layout()
plt.show()
```
