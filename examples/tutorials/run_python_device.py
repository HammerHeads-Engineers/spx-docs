"""Run beside python_device.py: python run_python_device.py."""
from pathlib import Path
from spx_sdk.model import Model


def simulate():
    device_path = str(Path(__file__).with_name('python_device.py').resolve())
    model = Model(name='python_sensor', definition={
        'attributes': {'temperature_c': 20.0},
        'import': {device_path: {
            'class': 'TemperatureDevice',
            'init': {'kwargs': {'start': 20.0, 'increment': 0.5}},
            'attributes': {'temperature_c': {'property': 'temperature_c'}},
            'methods': {'run': 'tick'},
        }},
    })
    try:
        model.prepare()
        result = []
        for tick in range(3):
            model['timer']['time'] = tick / 10
            model.run()
            result.append(model['attributes']['temperature_c'].internal_value)
        assert result == [20.5, 21.0, 21.5], result
        return result
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
