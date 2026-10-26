"""Run beside contact_fault.py: python run_fault.py."""
from spx_sdk.model import Model
from contact_fault import definition


def simulate():
    model = Model(name='fault_sensor', definition=definition(seed=42))
    try:
        model.prepare()
        values = []
        for tick in range(20):
            model['timer']['time'] = tick / 10
            model.run()
            values.append(model['attributes']['temperature_c'].external_value)
        return values
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
