# Using spx-python for Simulation

`spx-python` RC3 is an HTTP client. It controls a running SPX Server; it does
not execute the model locally like `spx_sdk.model.Model`.

## Prerequisites

Use a disposable SPX Server RC76 and the [documented bundle versions](../release-notes.md).
Do not run introductory scripts against a shared system. Use Python 3.12 in a
virtual environment and install `spx-python==1.0.0rc3`. Set `SPX_PRODUCT_KEY` in
your environment and optionally `SPX_BASE_URL` (default `http://localhost:8000`).
For managed workspaces use [MCP onboarding](../getting-started/connect-llm-with-spx-mcp.md);
do not replace the workspace's private connection binding with a guessed `.env`.

<figure><img src="../.gitbook/assets/guide-code-client-source.jpg" alt="Execution record identifying client_sensor.py and the controlled-clock lifecycle."><figcaption><p>Prepare the complete program below, then run it with your own environment credentials.</p></figcaption></figure>

## Complete program

Save as `client_sensor.py` in any working directory and run
`python client_sensor.py`. It creates a model and instance with reserved demo
names, refuses to overwrite existing objects, then stops and deletes only the
objects it created. Expected output:

```text
[(0.0, 31.25), (0.1, 31.25), (0.2, 31.25)]
```

<!-- tutorial:client_sensor.py:start -->
```python
"""Use a disposable server: this creates and removes docs_pt100/docs_sensor."""
import os
import spx_python

DEFINITION = {
    'name': 'docs_pt100',
    'attributes': {
        'k__temperature_c': {'type': 'float', 'default': 20.0, 'unit': 'degC'},
        'temperature_c': {'type': 'float', 'default': 20.0, 'unit': 'degC'},
    },
    'actions': [{'function': '$in(temperature_c)', 'call': '$in(k__temperature_c)'}],
}


def simulate(client):
    # Refuse to replace a user's existing model or instance.
    if 'docs_pt100' in client['models'] or 'docs_sensor' in client['instances']:
        raise RuntimeError('docs_pt100/docs_sensor already exists; use a disposable server')
    client['models']['docs_pt100'] = DEFINITION
    try:
        client['instances']['docs_sensor'] = 'docs_pt100'
        inst = client['instances']['docs_sensor']
        inst.real_time = False
        inst.prepare()
        inst.start()
        assert inst.state == 'RUNNING', inst.state
        inst['attributes']['k__temperature_c'].internal_value = 31.25
        rows = []
        for tick in range(3):
            # HTTP proxy: set the property, not inst['timer']['time'].
            inst['timer'].time = tick / 10
            inst.run(time_step=0.1)
            rows.append((inst['timer'].time,
                         inst['attributes']['temperature_c'].external_value))
        return rows
    finally:
        if 'docs_sensor' in client['instances']:
            client['instances']['docs_sensor'].stop()
            del client['instances']['docs_sensor']
        del client['models']['docs_pt100']


if __name__ == '__main__':
    client = spx_python.init(
        address=os.environ.get('SPX_BASE_URL', 'http://localhost:8000'),
        product_key=os.environ['SPX_PRODUCT_KEY'],
    )
    print(simulate(client))
```
<!-- tutorial:client_sensor.py:end -->

## Clock and lifecycle contract

- `real_time = False` prevents automatic model polling. Prepare once, then start
  the model before stepping. Do not prepare the whole system on every iteration.
- The HTTP proxy writes the timer property with `inst["timer"].time = t`.
  `inst["timer"]["time"] = t` is not the supported proxy property setter.
- An absolute time write suppresses the next automatic increment: the next
  explicit `run(time_step=0.1)` evaluates at that assigned time. A subsequent
  step without another absolute write advances it by 0.1.
- A single explicit run while a runtime model is paused executes one admitted
  cycle and leaves it `PAUSED`; `start()` resumes it. SDK base components have
  different lifecycle details; see [lifecycle reference](../spx-development-guide/spx-sdk/components/spxcomponent.md).
- Check the actual clock and output, not just a successful request or `RUNNING`.

## Values, faults and connections

Read telemetry via `external_value`; write persistent simulation inputs through
the appropriate `k__*` attribute. An internal write clears an external override.
For a persistent fault, apply it after the model's internal update on each
relevant cycle, or implement a fault action in the model.

For instance-to-instance wiring use the [connections reference](../spx-core/system/connections.md).
An agent should prefer the structured MCP connection tools described in the
[MCP reference](../getting-started/mcp-reference.md).

## Repeatability and tests

A manual clock alone does not fix random numbers, network delivery or external
process scheduling. Pin definitions and versions, seed local random generators,
and assert expected values. [Custom actions](../getting-started/extend-with-custom-component.md)
show a generator isolated per instance. Snapshot import restores structure;
reapply test inputs explicitly after import.

Run server integration tests only when the configured test server and key are
available; a skipped integration test is not a passing runtime verification.

<figure><img src="../.gitbook/assets/guide-code-client-result.jpg" alt="Execution record with three 31.25°C samples at controlled times and cleanup."><figcaption><p>The program removes its demo resources before returning its samples.</p></figcaption></figure>

Continue with [Python connections](../guides/python-connections.md), or perform the [same task in the UI](../guides/ui-instance.md).
