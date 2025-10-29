---
icon: arrows-from-line
---

# Extending the Core

While the SDK lets you register custom classes in Python easily, the server core adds operational considerations: packaging, dependency management, and safe loading. This guide outlines how to ship your own actions, protocols, or modules to the runtime.

## Package layout

Place your extensions under `extensions/` in the server repository or bundle them in a wheel. Ensure each module registers classes on import using `@register_class`.

```
extensions/
  my_company/
    __init__.py
    actions/
      energy_balancer.py
    communications/
      websocket.py
```

## Loading modules

Use the registry helpers during server startup (configurable via CLI or environment variables):

```python
from spx_sdk.registry import load_modules_recursively, install_requirements_from_dir

install_requirements_from_dir("extensions/my_company")
load_modules_recursively("extensions/my_company")
```

The server provides hooks (see `spx_server/app/hooks/extensions.py`) to automate this.

## Dependency management

* Place Python dependencies in `requirements.txt` files alongside the code.
* Prefer pinned versions to avoid drift.
* Validate installation offline before shipping to production.

## Registering components

```python
from spx_sdk.registry import register_class
from spx_sdk.actions.action import Action

@register_class(name="energy_balance")
class EnergyBalance(Action):
    ...
```

The same registry handles server and SDK extensions, so definitions authored locally work remotely.

## Testing strategy

1. Unit test with the SDK (fast feedback).
2. Integration test in the server environment (`docker compose up`, run smoke scenarios).
3. Monitor diagnostics logs for `registry_*` errors during startup.

## Operational tips

* Namespaces: prefix class names (`myco_ramp`) to avoid collisions.
* Observability: instrument custom components with diagnostics (`@guard`) and logging.
* Rollouts: load new modules in staging first; use snapshots to capture state before upgrades.
* Documentation: add entries in GitBook under SPX-CORE so other teams know how to use your extensions.
