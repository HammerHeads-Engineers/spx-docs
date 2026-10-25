"""Seeded custom action: import this module before loading its model."""
import random
from spx_sdk.actions import Action
from spx_sdk.registry import register_class


@register_class(name='docs_contact_fault')
class ContactFault(Action):
    def prepare(self, *args, **kwargs):
        result = super().prepare(*args, **kwargs)
        self.rng = random.Random(self.seed)
        return result

    def run(self):
        super().run()
        value = self.value
        if self.rng.random() < self.probability:
            value = 0.0 if self.rng.random() < self.drop_ratio else self.spike_value
        return self.write_outputs(value)


def definition(seed=42):
    return {
        'attributes': {'temperature_c': {'type': 'float', 'default': 20.0, 'unit': 'degC'}},
        'actions': [{'docs_contact_fault': '$ext(temperature_c)',
                     'value': '$in(temperature_c)', 'seed': seed,
                     'probability': 0.5, 'drop_ratio': 0.5, 'spike_value': 500.0}],
    }
