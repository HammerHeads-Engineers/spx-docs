"""Run from the Docs checkout: python examples/tutorials/sdk_sensor.py yaml."""
import argparse
import copy
import json

import yaml
from spx_sdk.model import Model

DEFINITION = {
    'attributes': {'temperature_c': {'type': 'float', 'default': 25.0, 'unit': 'degC'}},
    'actions': [{'function': '$ext(temperature_c)',
                 'call': '25 + 75 * (1 - 0.945 ** $(.timer.time))'}],
}


def simulate(format_name='dict'):
    definition = copy.deepcopy(DEFINITION)
    if format_name == 'yaml':
        definition = yaml.safe_load(yaml.safe_dump(definition, sort_keys=False))
    elif format_name == 'json':
        definition = json.loads(json.dumps(definition))
    sensor = Model(name='sensor', definition=definition)
    try:
        sensor.prepare()
        values = []
        for tick in range(601):
            seconds = tick / 10
            # Local SDK SimpleTimer: explicit absolute time, not the HTTP proxy.
            sensor['timer']['time'] = seconds
            sensor.run()
            values.append(sensor['attributes']['temperature_c'].external_value)
        return values
    finally:
        sensor.destroy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('format', choices=['yaml', 'json', 'dict'], default='dict', nargs='?')
    args = parser.parse_args()
    result = simulate(args.format)
    print(f't=0.0: {result[0]:.2f} degC; t=60.0: {result[-1]:.2f} degC')
