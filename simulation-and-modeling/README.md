# Simulation and Modeling

SPX is the simulation and modeling layer of the SPX platform that allows the creation, configuration, and execution of simulated models to represent devices, systems, or environments. Its purpose is to enable Model-in-the-Loop, hardware-free development, rapid prototyping, system integration, and scenario testing.

This section of the documentation covers the core concepts of simulation and modeling in SPX, guides for using different client libraries (e.g., SPX Python, SPX C++, or other future clients) necessary for deterministic control of simulations, example scenarios demonstrating practical uses, and best practices for building scalable and realistic simulation environments.

Deterministic control of simulations is critical for preparing simulations for unit tests or specific test cases, including edge cases, so that the main software can be validated under various conditions.

SPX simulations are controlled via the SPX Server API, which allows external clients to influence the simulation's state, parameters, and timing, enabling reproducible testing and precise manipulation of model instances.

This section is designed for both newcomers and experienced developers, providing both a conceptual overview and hands-on guides.

Explore the subsections to learn both the theory and practical application of simulation and modeling with SPX.
