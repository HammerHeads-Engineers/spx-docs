# Model-in-the-Loop (MiL) with SPX

Model-in-the-Loop (MiL) is a simulation-based testing approach where the system under test (SUT) interacts with a virtual model instead of physical hardware. This allows developers and testers to validate system behavior, control algorithms, and communication protocols in a controlled and repeatable environment.

## Core Idea

The primary purpose of MiL is to validate logic, control algorithms, and communication without the need for real devices. This is achieved by splitting the interaction into two channels:

- **Control channel**: Managed by an SPX client library such as SPX Python, this channel allows direct manipulation of the model's parameters, state, and simulation time.

- **Protocol channel**: The system under test communicates over the real communication protocol with the virtual instances, ensuring realistic interaction.

## How It Works in SPX

In the SPX ecosystem, the SPX Server hosts models and their live instances. Client libraries like SPX Python connect to the SPX Server API to manipulate these models, adjust parameters, and control simulation time progression.

The system under test communicates with the virtual instances over the real protocol, maintaining fidelity to actual device communication. Meanwhile, the control channel enables deterministic control such as pausing, stepping through time, or modifying the state of the simulation.

## Benefits of MiL with SPX

- **Hardware-independent development**: Test and develop without requiring physical devices.

- **Deterministic, reproducible testing**: Precisely control simulation time and state to reproduce scenarios.

- **Fault injection and edge-case simulation**: Introduce faults or unusual conditions to verify system robustness.

- **Scalability to many virtual devices**: Run large-scale simulations with multiple virtual instances.

- **Faster iteration and integration testing**: Rapidly test changes without hardware setup delays.

## Typical Workflow

1. Create and configure models in SPX.

2. Deploy instances on the SPX Server.

3. Connect your system under test to these instances via the real protocol.

4. Use SPX Python (or other clients) to drive simulation time, adjust parameters, and inject faults.

5. Observe and verify system behavior.

Explore the SPX Python and SPX C++ guides in this section for practical implementation examples of Model-in-the-Loop testing with SPX.
