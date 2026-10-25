#!/usr/bin/env python3
"""Export the released server routes. Local maintainer tool; never fetches private code in public CI."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    sha = json.loads((root / 'sources.json').read_text())['sources']['spx-server']['commit']
    archive = subprocess.check_output(['git', '-C', str(args.server), 'archive', sha])
    with tempfile.TemporaryDirectory() as directory:
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(directory, filter='data')
        # Execute our fixed exporter against an exact clean source tree, not the caller's checkout.
        program = '''import json, sys
from fastapi import FastAPI
from spx_server.api.api import router as root_router
from spx_server.api.api_v3 import router as v3_router
app = FastAPI(title="SPX Server API", version="3.0.0", openapi_url="/docs/openapi.json", docs_url="/docs", redoc_url="/redoc")
app.include_router(root_router)
app.include_router(v3_router)
spec = app.openapi()
spec["x-spx-source-commit"] = sys.argv[1]
print(json.dumps(spec, indent=2))
'''
        import os
        env = dict(os.environ, PYTHONPATH=directory)
        result = subprocess.check_output([sys.executable, '-c', program, sha], cwd=directory, env=env, text=True)
        spec = json.loads(result)
        target = root / 'api-v3-reference/openapi.json'
        target.write_text(json.dumps(spec, indent=2) + '\n')
        print(f'Exported {len(spec["paths"])} path templates from {sha}')


if __name__ == '__main__':
    main()
