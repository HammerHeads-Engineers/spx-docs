---
icon: satellite-dish
---

# Add Modbus TCP/IP to Your Simulation

Communication protocols are a first‑class part of SPX simulations: they expose your simulated signals to external tools (HMIs, test rigs, PLCs) and let real software interact with the model as if it were physical hardware.

This page uses **Modbus TCP** as an example adapter. For other protocols, start with: [Choose a protocol adapter](choose-a-protocol-adapter.md).

In this step we wire our **PT100‑style temperature sensor** from [Build Your First Simulation](build-your-first-simulation.md) to Modbus so any Modbus client can read the sensor value and a binary fault flag.

**What is Modbus TCP?** It is a widely used industrial protocol over TCP/IP. In SPX it ships **natively in the Core library**, so you can enable it directly in your model—no extra installation required.

{% code title="modbus_example.py" %}
```python
import os
import yaml
import spx_python

# 1) Connect to the running SPX Server
client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
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
  - modbus_slave:
      host: 0.0.0.0
      port: 502
      unit_id: 1
      mapping:
        temperature: { address: [0,1], group: h_r, type: float }
        sensor_fault: { address: 4, group: c_o, type: bool }
'''
# 3) Register the model and create an instance
model_def = yaml.safe_load(pt_100_yaml)
client["models"]["pt_100_modbus"] = model_def
client["instances"]["pt100_mb_1"] = "pt_100_modbus"
inst = client["instances"]["pt100_mb_1"]
client.prepare()
modbus = inst["communication"]["modbus_slave"]
modbus.start()
# 4) Step deterministically (so external tools see changing readings)
for k in range(1, 51):  # ~5 seconds with dt=0.1
    inst["timer"]["time"] = k * 0.1
    client.run()
    print("internal temperature:", inst["attributes"]["temperature"].internal_value)
    print("external temperature:", inst["attributes"]["temperature"].external_value)
    print("sensor_fault:", inst["attributes"]["sensor_fault"].internal_value)
# A Modbus TCP client can now read temperature at holding registers 0–1 and sensor_fault at coil 4.
```
{% endcode %}

## Next steps on simplephysx.com

Explore the Modbus pillar and testing workflow related to this guide:

- [Modbus TCP Simulator](https://www.simplephysx.com/modbus-simulator)
- [Embedded Software Testing](https://www.simplephysx.com/embedded-software-testing)

In this configuration:

* `port` and `host` define where the Modbus TCP server listens (inside the SPX Server container). Common default is `0.0.0.0:502`; in this example we set them explicitly for predictability.
* `mapping` binds model attributes to Modbus tables and addresses:
  * `temperature` → `group: h_r` (holding registers), `address: [0, 1]`, `type: float` — a float32 spanning two consecutive 16‑bit registers (Big Endian default).
  * `sensor_fault` → `group: c_o` (coils), `address: 4`, `type: bool` — a binary 0/1 flag indicating sensor contact fault.

**Attributes in this model**

* `temperature` (float) — internal logic drives the true value; external presentation may include noise.
* `sensor_fault` (0/1) — a binary flag you can set from the simulation (or a test) to indicate a contact error.

With this setup, any Modbus TCP client can read the **temperature** from holding registers **0–1** and the **sensor\_fault** flag from coil **4** in real time while the simulation advances deterministically.

## Quick Verification with a Modbus TCP Client

Note: your `docker-compose.yml` must expose the Modbus port for host-side clients.

For example:

```yaml
services:
  spx-server:
    ports:
      - "8000:8000"
      - "1502:502"   # Modbus TCP (avoid privileged host port 502 on Linux/rootless Docker)
```

Then connect your SUT to `127.0.0.1:1502`.

To verify the Modbus TCP server is working correctly, create a simple Python client that connects to your **host-exposed Modbus port** (for example `127.0.0.1:1502`), reads the mapped registers, and plots the temperature and fault flag. This example also demonstrates **Model‑in‑the‑Loop (MiL)**: the **Software Under Test (SUT)** is the Modbus TCP client (your real application code), while the **SPX model** plays the role of the plant/sensor. We use `spx-python` only as a control channel to start/stop the model so data capture stays in sync.

**Note:** Unlike the deterministic stepping shown earlier (where you set `instance["timer"]["time"]` and call `run()`), here we call `start()`, which hands time progression to the server’s internal scheduler. The simulation advances autonomously according to `timer.dt` and the server loop—great for live protocol testing—while deterministic stepping remains preferable for strictly reproducible unit tests.

{% code title="sut_example.py" %}
```python
import os
import struct
import time
import matplotlib.pyplot as plt

from modbus_tk import modbus_tcp
from modbus_tk import defines as c

import spx_python


class SUTSensor:
    """Software Under Test (SUT): thin Modbus TCP wrapper for reading measurements.
    Hides protocol details from the test/plotting logic.
    """
    def __init__(self, host="127.0.0.1", port=1502, unit=1, timeout=2.0):
        self.host = host
        self.port = port
        self.unit = unit
        self.timeout = timeout
        self._mb = None

    def connect(self):
        """Create master and set timeouts."""
        self._mb = modbus_tcp.TcpMaster(host=self.host, port=self.port)
        self._mb.set_timeout(self.timeout)

    @staticmethod
    def _float_from_two_u16_be(regs):
        """Decode float32 from two 16-bit holding registers (Big Endian)."""
        if len(regs) != 2:
            raise ValueError(f"Expected 2 registers, got {len(regs)}")
        payload = struct.pack(">HH", regs[0] & 0xFFFF, regs[1] & 0xFFFF)
        return struct.unpack(">f", payload)[0]

    def read_temperature_and_fault(self):
        """Temperature from HR 0–1 (float32 Big Endian), fault flag from coil 4 (0/1)."""
        if self._mb is None:
            raise RuntimeError("Modbus master not connected. Call connect() first.")

        # Read temperature (two 16-bit holding registers)
        hr = self._mb.execute(self.unit, c.READ_HOLDING_REGISTERS, 0, 2)
        temp = self._float_from_two_u16_be(hr)

        # Read fault flag (coil 4)
        coils = self._mb.execute(self.unit, c.READ_COILS, 4, 1)
        fault = int(bool(coils[0]))

        return temp, fault

    def close(self):
        """modbus_tk masters close automatically on GC; nothing required here."""
        self._mb = None


# 1) Control channel: connect to the running SPX Server
spx_client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

# 2) Get the model instance (created earlier in the guide)
model = spx_client["instances"]["pt100_mb_1"]  # adjust if you used a different name

# 3) SUT: Modbus client (modbus_tk)
sensor = SUTSensor(host="127.0.0.1", port=1502, unit=1, timeout=2.0)
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
{% endcode %}
