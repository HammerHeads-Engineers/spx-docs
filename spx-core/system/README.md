---
icon: solar-system
---

# System Runtime

The system runtime is the part of SPX-CORE that turns your YAML file into a live simulation. The modules in `spx_core/system` load components, wire them together, advance time, and drive scenarios. This overview links to detailed pages for each module so you can configure them confidently.

## Runtime flow

1. **Model loader** reads the YAML definition, resolves templates, and creates top-level containers.
2. **Instances and modules** instantiate reusable subsystems and nested components.
3. **Parameters and connections** inject constants and route signals between attributes.
4. **Timer and polling** keep the simulation loop running deterministically.
5. **Scenarios** inject scripted events, while **templates** let you reuse proven configurations.

Each page below explains responsibilities, configuration fields, and practical examples aimed at junior developers and QA engineers.

* [Model Loader](model.md)
* [Instances Container](instances.md)
* [Modules Container](modules.md)
* [Parameters](parameters.md)
* [Connections](connections.md)
* [Timer](timer.md)
* [Polling](polling.md)
* [Scenarios](scenarios.md)
* [Logs](logs.md)
* [Templates](templates.md)
