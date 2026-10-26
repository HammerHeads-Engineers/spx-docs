"""Two HTTP-controlled sensors; refuses name collisions and cleans up its resources."""
import os
import spx_python
from client_sensor import DEFINITION


def simulate(client):
    model = 'docs_link_model'
    names = ('docs_source', 'docs_target')
    link = 'docs_temperature_link'
    if model in client['models'] or any(n in client['instances'] for n in names) or link in client['connections']:
        raise RuntimeError('Demo names already exist; use a disposable server')
    made = []
    client['models'][model] = DEFINITION
    try:
        for name in names:
            client['instances'][name] = model
            made.append(name)
            inst = client['instances'][name]
            inst.real_time = False
            inst.prepare()
            inst.start()
        client['connections'][link] = {
            'from': '$out(docs_source.temperature_c)',
            'to': '$in(docs_target.k__temperature_c)',
        }
        connection = client['connections'][link]
        # Explicit manual propagation: do not start the global background container.
        connection.start()
        result = []
        source, target = (client['instances'][n] for n in names)
        for tick, expected in enumerate((28.0, 34.0)):
            source['attributes']['k__temperature_c'].internal_value = expected
            for inst in (source, target):
                inst['timer'].time = tick / 10
            source.run(time_step=0.1)
            connection.run()
            target.run(time_step=0.1)
            actual = target['attributes']['temperature_c'].external_value
            assert actual == expected, (actual, expected)
            result.append((expected, actual))
        return result
    finally:
        if link in client['connections']:
            client['connections'][link].stop()
            del client['connections'][link]
        for name in made:
            client['instances'][name].stop()
            del client['instances'][name]
        del client['models'][model]


if __name__ == '__main__':
    client = spx_python.init(address=os.environ.get('SPX_BASE_URL', 'http://localhost:8000'),
                             product_key=os.environ['SPX_PRODUCT_KEY'])
    print(simulate(client))
