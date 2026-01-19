---
icon: python
---

# SPX-PYTHON

**SPX-PYTHON**

`spx-python` is the officially supported client wrapper for the SPX Server API v3. It turns the REST surface into a Pythonic, dictionary-like interface and ships with helper utilities tailored for automated tests, CI pipelines, and exploratory notebooks.

Use this section to:

* Configure the wrapper against local or remote SPX deployments.
* Reuse the helpers that load models, create instances, and wait for state transitions.
* Capture unit-test assertions and test case results into SPX instances using `unittest` mixins and `pytest` plugins.
* Understand how the client surfaces faults and correlation IDs so automation can react intelligently.
* Extend the transport layer (e.g., plug in FastAPI `TestClient` or custom mocks) without rewriting call sites.

The section is split into three guides:

* [Overview & Installation](overview-and-installation.md) — how to install the package, initialize the client, and understand the available configuration toggles.
* [Usage & Examples](usage-and-examples.md) — practical snippets covering attribute access, model/instance management, transparent mode, and the helper toolkit used across the `spx-examples` test suite.
* [Testing Helpers & Logging Integration](testing-helpers-and-logging.md) — how to integrate the helper toolkit with `unittest` and `pytest` to log test runs into SPX attributes.
* [Advanced & Best Practices](advanced-and-best-practices.md) — deeper coverage of error handling, fault introspection, custom transports, and strategies for reliable integration tests.

Each page references real code from `spx_python.client`, `spx_python.helpers`, and the regression tests found in the `spx-python` and `spx-examples` repositories so you can cross-check behaviour quickly.
