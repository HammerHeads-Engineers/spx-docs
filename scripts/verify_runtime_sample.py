#!/usr/bin/env python3
"""Maintainer smoke: run the documented YAML/JSON through the released API and Python client.

Run with server RC76 sources on PYTHONPATH and the pinned server dependency
lock, SDK RC21 and client RC3 installed. No real key, Docker or hardware needed.
"""
from pathlib import Path
import json
import re
import yaml
from fastapi import FastAPI
from fastapi.testclient import TestClient
import spx_python
from spx_core.system import System
from spx_server.api.api import router as root_router
from spx_server.api.api_v3 import router as v3_router


def main():
    root = Path(__file__).resolve().parents[1]
    text = (root / 'simulation-and-modeling/model-definition-reference.md').read_text()
    yml = yaml.safe_load(re.search(r'```yaml\n(.*?)\n```', text, re.S).group(1))
    jsn = json.loads(re.search(r'```json\n(.*?)\n```', text, re.S).group(1))
    assert yml == jsn
    app = FastAPI()
    system = System(name='documentation_smoke', definition={'models': {}, 'instances': {}})
    app.state.system = system
    app.state.product_key = 'local-documentation-test-only'
    app.include_router(root_router)
    app.include_router(v3_router)
    http = TestClient(app)
    assert http.get('/health').status_code == 200
    assert http.get('/api/v3/system').status_code in (401, 403)
    assert http.get('/api/v3/system', headers={'Authorization': 'Bearer incorrect'}).status_code in (401, 403)
    client = spx_python.init(address='http://testserver', product_key=app.state.product_key, http_client=http)
    try:
        for suffix, definition in [('yaml', yml), ('json', jsn)]:
            name = 'pt100_' + suffix
            client['models'][name] = definition
            client['instances'][name] = name
            instance = client['instances'][name]
            instance.real_time = False
            instance.prepare()
            instance.start()
            assert instance.state == 'RUNNING', instance.state
            instance['attributes']['k__temperature_c'].internal_value = 31.25
            instance.run(time_step=0.1)
            assert instance['attributes']['temperature_c'].internal_value == 31.25
            instance.stop()
    finally:
        system.stop()
    print('OK: YAML/JSON registration, API auth, Python RC3, RUNNING state and telemetry')


if __name__ == '__main__':
    main()
