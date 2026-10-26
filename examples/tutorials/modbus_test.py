"""Protocol integration test: python modbus_test.py -v (disposable server)."""
import copy
import os
import struct
import unittest
import spx_python
from modbus_tk import defines as codes
from modbus_tk.modbus_tcp import TcpMaster
from client_sensor import DEFINITION


def verify(client, host='127.0.0.1', port=15020):
    model, name = 'docs_modbus_model', 'docs_modbus_sensor'
    if model in client['models'] or name in client['instances']:
        raise RuntimeError('Demo names exist; use a disposable server')
    definition = copy.deepcopy(DEFINITION)
    definition['meta_parameters'] = {
        'modbus_host': {'type': 'str', 'default': '0.0.0.0'},
        'modbus_port': {'type': 'int', 'default': port},
        'modbus_unit_id': {'type': 'int', 'default': 1},
    }
    definition['communication'] = [{'modbus_slave': {
        'host': '$param(modbus_host)', 'port': '$param(modbus_port)',
        'unit_id': '$param(modbus_unit_id)',
        'mapping': {'temperature_c': {'address': [0, 1], 'group': 'h_r', 'type': 'float'}},
    }}]
    client['models'][model] = definition
    master = TcpMaster(host=host, port=port, timeout_in_sec=3.0)
    adapter = None
    try:
        client['instances'][name] = model
        instance = client['instances'][name]
        instance.real_time = False
        instance.prepare()
        adapter = instance['communication']['modbus_slave']
        adapter.start()
        result = []
        for tick, expected in enumerate((28.0, 34.0)):
            instance['timer'].time = tick / 10
            instance['attributes']['k__temperature_c'].internal_value = expected
            instance.run(time_step=0.1)
            words = master.execute(1, codes.READ_HOLDING_REGISTERS, 0, 2)
            actual = struct.unpack('>f', struct.pack('>HH', *words))[0]
            assert abs(actual - expected) < 0.001, (words, actual, expected)
            result.append(actual)
        return result
    finally:
        master.close()
        if name in client['instances']:
            if adapter is not None:
                adapter.stop()
            client['instances'][name].stop()
            del client['instances'][name]
        del client['models'][model]


class ModbusIntegration(unittest.TestCase):
    def test_temperature_readback(self):
        client = spx_python.init(address=os.environ.get('SPX_BASE_URL', 'http://localhost:8000'),
                                 product_key=os.environ['SPX_PRODUCT_KEY'])
        self.assertEqual(verify(client, host=os.environ.get('SPX_MODBUS_HOST', '127.0.0.1'),
                                port=int(os.environ.get('SPX_MODBUS_PORT', '15020'))), [28.0, 34.0])


if __name__ == '__main__':
    unittest.main()
