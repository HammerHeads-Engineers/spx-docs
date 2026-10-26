"""Executable contracts for published SDK/client tutorials (no server required)."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples/tutorials'))
from sdk_sensor import simulate
from heat_loss import simulate as cooling
from contact_fault import definition
from spx_sdk.model import Model
from spx_sdk.attributes.attribute import SpxAttribute
from spx_sdk.components import SpxComponent
from spx_sdk.registry import load_instances_from_yaml_data, get_instance, register_class
import spx_python


class TutorialContracts(unittest.TestCase):
    def test_all_serializations_produce_same_temperature_curve(self):
        curves = [simulate(fmt) for fmt in ('yaml', 'json', 'dict')]
        self.assertEqual(curves[0], curves[1])
        self.assertEqual(curves[1], curves[2])
        self.assertEqual(curves[0][0], 25.0)
        self.assertAlmostEqual(curves[0][-1], 25 + 75 * (1 - 0.945 ** 60))
        self.assertTrue(all(a <= b for a, b in zip(curves[0], curves[0][1:])))

    def test_custom_heat_loss_action(self):
        self.assertEqual(cooling(), [92.0, 84.8, 78.32])

    def test_client_keywords_keep_credentials_separate(self):
        client = spx_python.init(product_key='documentation-dummy', address='http://testserver')
        self.assertEqual(client.base_url, 'http://testserver')
        self.assertEqual(client.product_key, 'documentation-dummy')

    def test_sdk_lifecycle_is_not_run_then_stopped(self):
        c = SpxComponent(name='lifecycle')
        for operation, expected in [('prepare', 'PREPARED'), ('start', 'RUNNING'),
                                    ('pause', 'PAUSED'), ('run', 'RUNNING'),
                                    ('start', 'RUNNING'), ('stop', 'STOPPED')]:
            getattr(c, operation)()
            self.assertEqual(str(c.state), expected)
        c.destroy()
        self.assertEqual(str(c.state), 'DESTROYED')

    def test_internal_write_clears_external_override(self):
        attr = SpxAttribute(name='temperature_c', definition={'type': 'float', 'default': 20.0})
        attr.external_value = 99.0
        self.assertEqual(attr.internal_value, 20.0)
        attr.internal_value = 21.0
        self.assertEqual(attr.external_value, 21.0)

    def test_registry_accepts_plain_safe_yaml(self):
        @register_class(name='docs_heater')
        class Heater(SpxComponent):
            pass
        load_instances_from_yaml_data('heater_instance:\n  class: docs_heater\n  parameters:\n    name: heater_instance\n')
        obj = get_instance('heater_instance')
        self.assertIsInstance(obj, Heater)
        obj.destroy()

    def test_seed_is_per_instance_and_reproducible(self):
        from contact_fault import ContactFault  # Registration happens at import.
        a = Model(name='a', definition=copy.deepcopy(definition()))
        b = Model(name='b', definition=copy.deepcopy(definition()))
        a.prepare()
        left = []
        for _ in range(20):
            a.run()
            left.append(a['attributes']['temperature_c'].external_value)
        b.prepare()  # Preparing another instance must not reset a's RNG.
        right = []
        for _ in range(20):
            b.run()
            right.append(b['attributes']['temperature_c'].external_value)
        self.assertEqual(left, right)
        # Interleave preparation/execution to detect a shared process-wide RNG.
        control = Model(name='control', definition=copy.deepcopy(definition()))
        control.prepare()
        expected = []
        for _ in range(40):
            control.run()
            expected.append(control['attributes']['temperature_c'].external_value)
        for _ in range(20):
            a.run()
            left.append(a['attributes']['temperature_c'].external_value)
        self.assertEqual(left, expected)
        control.destroy()
        self.assertGreater(len(set(left)), 1)
        a.destroy(); b.destroy()


class GuideExampleContracts(unittest.TestCase):
    def test_filter_warmup_and_sliding_window(self):
        from moving_average import simulate
        self.assertEqual(simulate(), [0.0, 1.5, 3.0, 6.0])

    def test_hysteresis_retains_state_inside_band(self):
        from hysteresis import simulate
        self.assertEqual(simulate(), [False, True, True, False])

    def test_python_property_and_lifecycle_import(self):
        from run_python_device import simulate
        self.assertEqual(simulate(), [20.5, 21.0, 21.5])


if __name__ == '__main__':
    unittest.main()
