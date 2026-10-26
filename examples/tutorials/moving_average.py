"""Local SDK filter: python moving_average.py. Register before loading the model."""
from collections import deque
from spx_sdk.actions import Action
from spx_sdk.registry import register_class
from spx_sdk.model import Model


@register_class(name='docs_moving_average')
class MovingAverage(Action):
    def prepare(self, *args, **kwargs):
        result = super().prepare(*args, **kwargs)
        self.samples = deque(maxlen=int(self.window))
        return result

    def run(self):
        super().run()
        self.samples.append(float(self.source))
        return self.write_outputs(sum(self.samples) / len(self.samples))


def simulate():
    model = Model(name='filtered_sensor', definition={
        'attributes': {'k__raw_signal': 0.0, 'filtered_signal': 0.0},
        'actions': [{'docs_moving_average': '$out(filtered_signal)',
                     'source': '$in(k__raw_signal)', 'window': 3}],
    })
    try:
        model.prepare()
        result = []
        for tick, value in enumerate((0.0, 3.0, 6.0, 9.0)):
            model['timer']['time'] = tick / 10
            model['attributes']['k__raw_signal'].internal_value = value
            model.run()
            result.append(model['attributes']['filtered_signal'].external_value)
        assert result == [0.0, 1.5, 3.0, 6.0], result
        return result
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
