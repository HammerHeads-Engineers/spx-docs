# Build Simulations

This chapter is the reference for model concepts, SDK components, server runtime
and the Python HTTP client. For a task-oriented start use
[Start here](../overview/start-here.md).

## Choose the execution layer

- **Local logic:** [SDK Quickstart](quick-start-spx-sdk-in-5-minutes.md), no server
  or product key. Use it to test actions and calculations in Python.
- **Hosted simulation:** [Python client tutorial](../simulation-and-modeling/using-spx-python.md),
  operating on a running server through API v3.
- **Agent-driven runtime:** [MCP onboarding](../getting-started/connect-llm-with-spx-mcp.md).
- **Model definitions:** [YAML/JSON reference](../simulation-and-modeling/model-definition-reference.md).
- **SUT communication:** [protocol capabilities](../spx-core/communications/capabilities.md).

A local SDK object and a remote client proxy do not have interchangeable timer
or lifecycle semantics. The runnable tutorials show the supported loop for each.
Use the [released version set](../release-notes.md), apply deployment-specific
communication parameters, and verify the actual output expected by your test.

## Reference chapters

[SDK](spx-sdk/README.md) describes local building blocks;
[Core](../spx-core/README.md) describes hosted runtime services;
[Python client](spx-python-client-wrapper/README.md) describes remote control.
Protocol reference examples are configuration fragments unless explicitly
identified as complete programs. Source or unit tests alone do not certify a
physical protocol implementation or manufacturer device.
