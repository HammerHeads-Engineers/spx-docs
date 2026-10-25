# Code Examples

These recipes target the [released version set](../release-notes.md). Use a
disposable local server, not a shared production system.

## Health and authentication

```bash
curl -fsS http://localhost:8000/health
curl -fsS -H "Authorization: Bearer $SPX_PRODUCT_KEY" http://localhost:8000/api/v3/system
```

`/health` is public; `/api/v3/` requires the product key. A health response alone
does not prove authenticated access. Never put your key in a URL or commit it.

## Load, create, step, read and clean up

Use Python 3.12 and `python -m pip install spx-python==1.0.0rc3` in a virtual
environment. Export `SPX_PRODUCT_KEY`; optionally export `SPX_BASE_URL`.
Save the following as `client_sensor.py`, then run `python client_sensor.py`.
No separate `model.yaml` is required: the complete definition is included.

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

Expected result: `[(0.0, 31.25), (0.1, 31.25), (0.2, 31.25)]`.
The program deletes its demo instance and model in `finally`.
See [client clock semantics](../simulation-and-modeling/using-spx-python.md#clock-and-lifecycle-contract)
before adapting the loop.

## API schemas versus simulation models

The generated **Models** section contains OpenAPI request/response schemas,
including `HTTPValidationError` and `ValidationError`. These are API schemas,
not catalog devices or simulation definitions. Use the
[model language reference](../simulation-and-modeling/model-definition-reference.md)
for simulation YAML/JSON and the generated endpoint pages for HTTP payloads.
