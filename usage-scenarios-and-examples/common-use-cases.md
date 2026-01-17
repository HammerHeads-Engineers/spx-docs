# Guided Use Cases & Scenarios

This consolidated page combines the earlier "Common Use Cases" and "Step-by-Step Guides" to keep scenario-driven guidance together.

## Common Use Cases

### 1. Validating device drivers against virtual hardware
- Model the target instrument or controller in YAML.
- Wire protocol adapters so the real driver talks to the simulation.
- Script deterministic scenarios to cover happy-path and fault modes.
- Collect logs/telemetry for debugging without touching real hardware.

### 2. Exercising QA smoke tests in CI
- Spin up the SPX Server or SDK model inside a pipeline job.
- Replay known-good scenarios to detect regressions in firmware or services.
- Export `FaultEvent`s when assertions fail to keep feedback actionable.

### 3. Training junior engineers
- Start from library models (for example the SCPI multimeter).
- Let new team members modify attributes/actions safely.
- Visualize protocol behavior without needing lab access.

## Step-by-Step Walkthroughs

### Scenario: SCPI Multimeter Smoke Test

Based on `spx-examples/library/domains/measurement_instruments/generic/multimeter__scpi.yaml`.

1. **Load the model**
   Use `spx-python` to push the model definition into a running server:

   ```python
   import os
   import yaml
   import spx_python

   client = spx_python.init(
       address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
       product_key=os.environ["SPX_PRODUCT_KEY"],
   )

   # In your local checkout of spx-examples:
   model_path = "library/domains/measurement_instruments/generic/multimeter__scpi.yaml"
   with open(model_path, "r", encoding="utf-8") as f:
       model_def = yaml.safe_load(f)

   client["models"]["generic_scpi_multimeter"] = model_def
   client["instances"]["scpi_inst_1"] = "generic_scpi_multimeter"
   ```

2. **Connect your SCPI client**
   - If you are using the `spx-examples/docker-compose.yml` baseline, point it to `127.0.0.1:5025`.
   - Use line endings `\n` (see `terminator` in the model).

3. **Baseline reading**
   ```text
   > MEAS:VOLT?
   < 0.0
   ```
   Verifies the default `voltage` attribute.

4. **Change measurement mode**
   ```text
   > CONF:CURR
   > MEAS:CURR?
   < 0.0
   ```
   Confirms the `measurement_mode` attribute updates and the mapping dispatches the correct attribute.

5. **Run the `voltage_static` scenario**
   - In YAML, the scenario slews voltage toward 230 V and injects noise.
   - Trigger via `spx-python`:
     - `client["instances"]["scpi_inst_1"]["scenarios"]["voltage_static"].start()`
   - Observe multiple reads drifting toward 230 with small jitter.

6. **Simulate protocol disruption**
   - Start `ascii_disconnect` scenario to detach the ASCII server for 2 seconds.
   - Ensure the driver handles timeouts gracefully.

7. **Inject latency spike**
   - Enable `ascii_response_delay_spike` and confirm retry logic handles slow responses.

8. **Record findings**
   - Note expected vs. observed behavior.
   - Capture any `FaultEvent`s emitted by the driver or simulation.

### Scenario Blueprint Template

Use this checklist when creating scenarios for other models:

| Step | Questions | Notes |
|------|-----------|-------|
| Define intent | What user story are we simulating? | e.g. "Operator reads voltage while unplugging sensor." |
| Select assets | Which YAML model and scenarios support it? | Start with `spx-examples/library/domains/...`. |
| Identify actors | Which services or scripts will interact with the model? | REST client, SCPI CLI, Modbus master. |
| Script stimuli | Which API/protocol calls drive the scenario? | Document command sequences. |
| Expected results | What readings/logs confirm success? | Use attribute wrappers or protocol responses. |
| Fault coverage | How do we simulate edge cases? | Add scenario overrides or temporary detachments. |
| Cleanup | How do we reset the model? | Call `stop()` on scenarios or reload the model. |

### Tips for Junior Engineers / QA

- Start with one scenario and make the happy-path pass before layering faults.
- Use the `spx-examples` repo as a library; copy models into your project as needed.
- When results look odd, inspect live instance state via `spx-python` and server logs.
- Commit updates to scenarios alongside test scripts so the team reviews both.
