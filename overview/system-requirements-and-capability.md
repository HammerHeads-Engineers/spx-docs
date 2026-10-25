# System Requirements and Capability

Use the coherent bundle in [Release Notes](../release-notes.md), not independent
repository tag numbers. Python package minimums are not whole-product requirements.

| Component / task | Documented version | Python and installation |
| --- | --- | --- |
| Native installer | RC115 | macOS/Windows supplies Python 3.12; Docker/Compose v2 required |
| Portable installer | RC115 | host Python >=3.9 for setup; >=3.10 for MCP; recommend 3.12 |
| Server | RC76 | >=3.12,<3.14 inside the supplied container; host Python not required for UI use |
| UI | RC76 | modern browser; no host Python needed |
| SDK | 1.0.0rc21 | package metadata >=3.9,<4; these tutorials execute on 3.12 |
| Python HTTP client | 1.0.0rc3 | package metadata >=3.9,<4; these tutorials execute on 3.12 |
| Public Examples development | pinned context in Release Notes | Python 3.12 for repository validation; MCP >=3.10 |

For standalone SDK/client tutorials create and activate a virtual environment,
then install only the packages required by that tutorial:

```bash
python -m pip install spx-sdk==1.0.0rc21 spx-python==1.0.0rc3 PyYAML==6.0.3
```

The server container owns its runtime dependencies. Do not repair it by installing
packages into the host Python. Use the installer-provided interpreter for managed
workspaces rather than an unrelated `pip --user` environment.

## Runtime prerequisites

Docker must be running. Reserve ports 8000 (API) and 3000 (optional UI), and
obtain your product key through the account page linked from
[Installation](../getting-started/installation-guide.md). Additional protocol
ports and external services depend on the [capability matrix](../spx-core/communications/capabilities.md).
Keep host port mappings aligned with the generated Compose file.

## What has been verified

Documentation CI parses files, checks links and executes SDK/client contracts on
Python 3.12. Private runtime checks use the pinned server and a local test key.
Neither check certifies physical devices, all operating systems or every Python
version permitted by individual package metadata. Protocol/hardware verification
must be recorded separately for the SUT and deployment in question.
