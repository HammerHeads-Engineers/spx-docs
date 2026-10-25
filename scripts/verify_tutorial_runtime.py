#!/usr/bin/env python3
"""Private CI contracts: released server sources/dependencies, no real product key."""
import copy
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples/tutorials'))
from client_sensor import simulate, DEFINITION
from fastapi import FastAPI
from fastapi.testclient import TestClient
from spx_core.system import System
from spx_server.api.api import router as root_router
from spx_server.api.api_v3 import router
import spx_python


class RuntimeContracts(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.system = System(name='docs_contract', definition={
            'models': {}, 'instances': {},
            'snapshots': {'base_dir': self.directory.name},
        })
        self.app = FastAPI()
        self.app.state.system = self.system
        self.app.state.product_key = 'documentation-test-only'
        self.app.include_router(root_router)
        self.app.include_router(router)
        self.http = TestClient(self.app)
        self.client = spx_python.init(address='http://testserver',
                                      product_key=self.app.state.product_key,
                                      http_client=self.http)

    def tearDown(self):
        self.app.state.system.stop()
        self.http.close()
        self.directory.cleanup()

    def test_published_client_program_and_cleanup(self):
        self.assertEqual(simulate(self.client), [(0.0, 31.25), (0.1, 31.25), (0.2, 31.25)])
        self.assertNotIn('docs_sensor', self.client['instances'])
        self.assertNotIn('docs_pt100', self.client['models'])

    def make_instance(self):
        self.client['models']['sensor'] = copy.deepcopy(DEFINITION)
        self.client['instances']['sensor_1'] = 'sensor'
        inst = self.client['instances']['sensor_1']
        inst.real_time = False
        inst.prepare()
        return inst

    def test_manual_clock_is_stable_and_first_absolute_step_does_not_increment(self):
        inst = self.make_instance()
        inst.start()
        self.assertEqual(inst.state, 'RUNNING')
        inst['timer'].time = 1.0
        inst.run(time_step=0.1)
        self.assertEqual(inst['timer'].time, 1.0)
        inst.run(time_step=0.1)
        self.assertAlmostEqual(inst['timer'].time, 1.1)
        before = inst['timer'].time
        time.sleep(0.03)
        self.assertEqual(inst['timer'].time, before)
        inst.pause()
        self.assertEqual(inst.state, 'PAUSED')
        inst.run(time_step=0.1)
        self.assertEqual(inst.state, 'PAUSED')
        inst.start()
        inst.stop()
        self.assertEqual(inst.state, 'STOPPED')

    def test_snapshot_restores_defaults_not_runtime_checkpoint(self):
        inst = self.make_instance()
        attr = inst['attributes']['k__temperature_c']
        attr.internal_value = 42.0
        response = self.client['snapshots'].save()
        saved = response['result']
        self.assertTrue(Path(saved['persisted_path']).is_file())
        attr.internal_value = 77.0
        self.client['snapshots'].load(id=saved['id'])
        restored = self.client['instances']['sensor_1']
        self.assertEqual(restored['attributes']['k__temperature_c'].internal_value, 20.0)
        # Reapply runtime fixture explicitly after the structural import.
        restored.real_time = False
        restored.prepare()
        restored.start()
        restored['attributes']['k__temperature_c'].internal_value = 42.0
        restored.run(time_step=0.1)
        self.assertEqual(restored['attributes']['temperature_c'].external_value, 42.0)

    def test_auth_and_yaml_json_reference(self):
        self.assertEqual(self.http.get('/health').status_code, 200)
        self.assertIn(self.http.get('/api/v3/system').status_code, (401, 403))
        import verify_runtime_sample
        verify_runtime_sample.main()


if __name__ == '__main__':
    unittest.main()
