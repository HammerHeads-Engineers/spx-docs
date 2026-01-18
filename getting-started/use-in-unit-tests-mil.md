---
icon: vial-circle-check
---

# Use in Unit Tests (MiL)

This guide shows how to exercise your **Software Under Test (SUT)** against an SPX simulation inside **Python’s `unittest`**. The approach is **Model‑in‑the‑Loop (MiL)**: the SUT is your real client application (e.g., a Modbus TCP reader), while the SPX model acts as the plant/sensor.

We will:
- spin up a model (PT100‑style temperature sensor) and expose it over **Modbus TCP**,  
- drive the simulation **deterministically** (no wall‑clock timing),  
- read the measurements via the SUT and assert expected behavior.

> For a hands‑on intro to wiring Modbus, see **“Add Modbus TCP/IP to Your Simulation”** in this Getting Started section.

---

## Prerequisites

- A running **SPX Server** (e.g., `http://localhost:8000`) and a valid `SPX_PRODUCT_KEY` in your environment.  
- If SPX Server runs in Docker, expose Modbus TCP from the container (for example `- "1502:502"` in Compose) and point your SUT at `127.0.0.1:1502`.
- Python packages:
  ```bash
  pip install spx-python modbus-tk pyyaml
  ```
- The example uses **`modbus-tk`** in the SUT. You can adapt it to your own stack (`pymodbus`, embedded code, etc.).

---

## Test structure at a glance

- **`setUpClass`**: connect to SPX, register the model (YAML), create an instance, start the Modbus server.
- **`setUp`**: create the SUT client (e.g., Modbus master).
- **Tests**:
  1) connectivity/read sanity,  
  2) temperature evolution under deterministic stepping,  
  3) fault flag round‑trip (write in SPX, read in SUT).
- **`tearDown`**: close SUT connection.
- **`tearDownClass`**: stop/cleanup the SPX instance.

---

## Full example (`unittest`)

> The model and mapping mirror the Modbus example from the previous guide.

```python
# test_sut_modbus_mil.py
import os
import time
import unittest
import yaml

import spx_python
from modbus_tk import modbus_tcp
from modbus_tk import defines as C


PT100_YAML = """
attributes:
  temperature: 25.0
  sensor_fault: 0
actions:
  - { ramp: $in(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $out(temperature), std: 0.01, mode: proportional }
communication:
  - modbus_slave:
      # Bind inside the SPX Server container. Expose the port via docker compose for host-side SUTs.
      host: 0.0.0.0
      port: 502
      unit_id: 1
      mapping:
        temperature: { address: [0, 1], group: h_r, type: float }
        sensor_fault: { address: 4, group: c_o, type: bool }
"""


class SUTSensor:
    """Software Under Test: minimal Modbus client used in assertions."""

    def __init__(self, host="127.0.0.1", port=1502, unit=1, timeout=2.0):
        self.host = host
        self.port = port
        self.unit = unit
        self.timeout = timeout
        self._mb = None

    def connect(self):
        self._mb = modbus_tcp.TcpMaster(self.host, self.port)
        self._mb.set_timeout(self.timeout)

    @staticmethod
    def _float_from_two_u16_be(regs):
        import struct
        if len(regs) != 2:
            raise ValueError(f"Expected 2 registers, got {len(regs)}")
        payload = struct.pack(">HH", regs[0] & 0xFFFF, regs[1] & 0xFFFF)
        return struct.unpack(">f", payload)[0]

    def read_temperature(self):
        regs = self._mb.execute(self.unit, C.READ_HOLDING_REGISTERS, 0, 2)
        return self._float_from_two_u16_be(regs)

    def read_fault(self):
        coils = self._mb.execute(self.unit, C.READ_COILS, 4, 1)
        return int(bool(coils[0]))

    def close(self):
        self._mb = None


class TestSUT_MiL_Modbus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1) Control channel: connect to SPX Server
        cls.client = spx_python.init(
            address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
            product_key=os.environ.get("SPX_PRODUCT_KEY", ""),
        )

        # 2) Register model and create instance
        model_def = yaml.safe_load(PT100_YAML)
        cls.client["models"]["pt_100_modbus"] = model_def
        cls.client["instances"]["pt100_mb_1"] = "pt_100_modbus"
        cls.inst = cls.client["instances"]["pt100_mb_1"]

        # 3) Prefer deterministic time stepping in unit tests
        # (We won't call .start(); we will advance time via prepare() + run()).
        cls.client.prepare()
        # Start the Modbus TCP server inside the model after prepare() built binding contexts.
        cls.inst["communication"]["modbus_slave"].start()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.inst["communication"]["modbus_slave"].stop()
        finally:
            # Best-effort cleanup (optional)
            pass

    def setUp(self):
        # Fresh SUT connection for each test
        self.sut = SUTSensor()
        self.sut.connect()

    def tearDown(self):
        self.sut.close()

    # --- Helpers ---
    def _step(self, seconds, dt=0.1):
        """Deterministically advance the simulation by 'seconds'."""
        # Use the instance's timer if available; otherwise use client.run() directly.
        # Many systems expose a timer and accept direct time setting:
        # self.inst["timer"]["time"] = t
        steps = int(round(seconds / dt))
        for k in range(steps):
            # If your system exposes a time attribute, set it here before run()
            # Example:
            #   current = self.inst["timer"]["time"]
            #   self.inst["timer"]["time"] = current + dt
            self.client.run()

    # --- Tests ---
    def test_connectivity_and_first_read(self):
        """SUT can read mapped points over Modbus TCP."""
        temp = self.sut.read_temperature()
        fault = self.sut.read_fault()
        self.assertIsInstance(temp, (float, int))
        self.assertIn(fault, (0, 1))

    def test_temperature_increases_over_time(self):
        """Temperature should change when we advance the model deterministically."""
        before = self.sut.read_temperature()
        self._step(1.0)  # ~1s (10 steps of 0.1)
        after = self.sut.read_temperature()
        # With ramp + noise the value should generally increase.
        self.assertGreater(after, before, msg=f"after={after}, before={before}")

    def test_fault_flag_roundtrip(self):
        """Setting sensor_fault in the model is observable by the SUT."""
        # Set fault in SPX
        self.inst["attributes"]["sensor_fault"].value = 1
        self._step(0.2)
        self.assertEqual(self.sut.read_fault(), 1)

        # Clear it again
        self.inst["attributes"]["sensor_fault"].value = 0
        self._step(0.2)
        self.assertEqual(self.sut.read_fault(), 0)


if __name__ == "__main__":
    unittest.main()
```

### Why deterministic stepping?
- **Repeatable**: `run()` advances the model one step, independent of machine load.
- **Stable assertions**: you can reason about expected state after N steps.
- **Protocol servers** still run in the background, so your SUT can poll/subscribe reliably.

> Prefer `prepare()` + `run()` for **unit tests**. Reserve `start()` (real‑time scheduler) for **interactive/manual** testing or HIL‑like demonstrations.

---

## What to assert in MiL tests

- **Connectivity**: your SUT can read at least once without errors.
- **Monotonic/shape properties**: e.g., with a ramp action, later readings should exceed earlier ones.
- **Round‑trips**: toggling flags/commands in the model is visible to the SUT (and vice versa if applicable).
- **Tolerance windows**: when noise is enabled, compare with deltas (±ε), not exact equality.

---

## Troubleshooting

- **“Connection refused”**: Ensure the SPX model’s Modbus server is started:  
  `inst["communication"]["modbus_slave"].start()`.
- **No change in values**: If you used deterministic stepping, make sure you call `client.run()` in your test loop, or explicitly advance model time if your system expects it.
- **Racey reads with `start()`**: In real‑time mode, add small sleeps (e.g., `time.sleep(0.1)`) to align with `timer.dt`, or switch back to deterministic stepping for unit tests.

---

## Next: CI integration

In the next article we’ll wire these tests into **GitHub Actions**: provisioning Python, exporting `SPX_PRODUCT_KEY` as a secret, starting the SPX Server service, and running the suite headlessly.
