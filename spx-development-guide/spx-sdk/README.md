---
icon: hammer-brush
---

# SPX SDK

The SPX SDK is the Python toolkit that powers custom components, actions, and integrations inside the SPX runtime. These guides walk through the building blocks you use when extending simulations or authoring reusable libraries.

Start with the quick start to get a runnable environment, then drill into the individual subsystems:

- **Registry & Components** — how classes are registered and instantiated at runtime, plus the lifecycle guarantees provided by `SpxComponent` and `SpxContainer`.
- **Attributes, Actions, Logic** — the declarative primitives that shape model behaviour.
- **Communication & Hooks** — bridging simulations to external systems and reacting to lifecycle events.
- **Diagnostics & Validation** — surfacing meaningful faults and keeping definitions healthy.
- **Imports & Best Practices** — structuring larger projects, packaging helpers, and avoiding common pitfalls.

Each subpage links back to real code samples in the SDK and demonstrates the patterns we rely on across `spx-examples`.
