"""Local SDK action with state: python hysteresis.py."""
from spx_sdk.actions import Action
from spx_sdk.registry import register_class
from spx_sdk.model import Model


@register_class(name='docs_hysteresis')
class Hysteresis(Action):
    def prepare(self, *args, **kwargs):
        result = super().prepare(*args, **kwargs)
        self.output = False
        return result

    def run(self):
        super().run()
        if self.source >= self.high:
            self.output = True
        elif self.source <= self.low:
            self.output = False
        return self.write_outputs(self.output)


def simulate():
    model = Model(name='hysteresis_sensor', definition={
        'attributes': {'k__temperature_c': 20.0, 'cooling_on': False},
        'actions': [{'docs_hysteresis': '$out(cooling_on)',
                     'source': '$in(k__temperature_c)', 'low': 18.0, 'high': 22.0}],
    })
    try:
        model.prepare()
        result = []
        for tick, temperature in enumerate((20.0, 23.0, 21.0, 17.0)):
            model['timer']['time'] = tick / 10
            model['attributes']['k__temperature_c'].internal_value = temperature
            model.run()
            result.append(model['attributes']['cooling_on'].external_value)
        assert result == [False, True, True, False], result
        return result
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
