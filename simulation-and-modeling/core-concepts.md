# Core Concepts

This page describes the foundational elements of simulation and modeling in SPX. Understanding these core concepts is essential for effectively creating, controlling, and interacting with simulations within the SPX framework.

## Models, Instances, and Connections

A model in SPX serves as a template that defines the structure and behavior of a simulated entity. An instance is a live object created from a model that participates in the simulation, maintaining its own state and attributes. Connections represent links between attributes of different instances, enabling data flow and interaction within the simulation environment.

## Attributes and Their Values

Attributes hold data defining the state of a simulation instance. SPX distinguishes between two types of attribute values, which are exposed in the API as `internal_value` and `external_value` properties:

- `internal_value`: This is used exclusively within the simulation’s internal logic and calculations, representing the “true” state of the attribute. It forms the basis for all simulation computations and state changes.
- `external_value`: This is used for exposing values externally, often to communication protocols or user interfaces. It may contain modified or noisy versions of the internal value without impacting the internal state. This separation ensures that any noise, filtering, or transformations added for output purposes do not affect the internal logic unless explicitly intended.

Developers have the option to feed the `external_value` back into the internal logic if desired, but this must be done intentionally to maintain full control and avoid unintended side effects.

The update flow between these values is one-way:

- Updating `internal_value` automatically updates `external_value` unless the external value is explicitly overridden.
- Updating `external_value` does not change the `internal_value`.

Simple update flow:

```
Internal → External (external is updated)
External → Internal (only external updated and internal not)
```

## Actions, Conditions, and Hooks

Actions are operations that perform calculations or modify the simulation state. Conditions control whether actions execute based on logical criteria, enabling dynamic decision-making within the simulation. Hooks provide event-driven behavior by triggering actions in response to specific simulation events or changes.

## Timer and Poller

SPX simulations operate with deterministic timing, where simulation time advances explicitly rather than in real time. The timer mechanism allows manual control of time progression, ensuring reproducibility. Pollers enable periodic execution of actions by polling at defined intervals, facilitating time-based behaviors within the simulation.

## Deterministic Control with Client Libraries

To achieve reproducible tests and explore edge-case scenarios, SPX provides client libraries such as SPX Python and SPX C++. These clients allow precise control over simulation state, parameters, and time advancement. This deterministic control is vital for debugging, validation, and automated testing of complex systems.

## Control Channel vs Protocol Channel

SPX separates simulation manipulation and communication through two distinct channels. The control channel is used to manage and modify the simulation state and parameters, while the protocol channel handles communication between the system under test (SUT) and the simulation model. This separation ensures clear boundaries between control logic and protocol interactions.

Together, these core concepts provide a comprehensive framework for building robust, testable, and repeatable simulation environments in SPX. By leveraging models, controlled timing, and precise client interaction, users can create sophisticated simulations that accurately represent and test complex systems.
