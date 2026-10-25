"""SDK-only cooling action; run python examples/tutorials/heat_loss.py."""
from spx_sdk.actions import Action
from spx_sdk.model import Model
from spx_sdk.registry import register_class


@register_class(name='docs_heat_loss')
class HeatLoss(Action):
    def run(self):
        super().run()  # Resolve dynamic parameters before reading them.
        temperature = self.temperature_c
        return self.write_outputs(temperature - self.k * (temperature - self.ambient_c))


def simulate():
    model = Model(name='cooling_sensor', definition={
        'attributes': {'temperature_c': {'type': 'float', 'default': 100.0, 'unit': 'degC'}},
        'actions': [{'docs_heat_loss': '$in(temperature_c)',
                     'temperature_c': '$in(temperature_c)', 'k': 0.1, 'ambient_c': 20.0}],
    })
    try:
        model.prepare()
        values = []
        for tick in range(3):
            model['timer']['time'] = float(tick)
            model.run()
            values.append(model['attributes']['temperature_c'].internal_value)
        return values
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
