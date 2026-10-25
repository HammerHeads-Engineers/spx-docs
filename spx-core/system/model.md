# Model Loader

`spx_core/system/model.py` defines the `Model` class that the server instantiates for every YAML document. It is responsible for:

- Holding top-level containers (`attributes`, `actions`, `communication`, etc.).
- Spinning up dedicated `Timer`, `Polling`, and `Scenarios` children when those sections appear in YAML.
- Driving the lifecycle (`prepare`, `start`, `run`) for the entire simulation.

## Model definitions

Use the complete [Model definition reference](../../simulation-and-modeling/model-definition-reference.md)
for equivalent runnable YAML and JSON examples. When registering through
`client["models"]["name"]`, pass the definition directly with top-level
`attributes`, `actions`, `communication` and optional timer/scenario sections.
Do not add an extra `model:` envelope. Examples with ellipses are schematic,
not copy-paste payloads.

### Key behaviors

- **Automatic extraction**: The loader pulls `timer`, `polling`, and `scenarios` from the model definition before instantiating other containers. This keeps the YAML tidy—no need to declare those sections separately.
- **Unique identifier**: Each model gets a `uid` (UUID string) you can query through the API for observability.
- **Real-time flag**: `model.real_time` controls whether the polling loop runs continuously (`true`) or waits for manual ticks (`false`). You can flip it through the API for deterministic testing.

### Lifecycle expectations

1. `prepare()` is called on every child (attributes, actions, communication, timer, polling, scenarios).
2. `start()` launches timer/polling threads when `real_time` is true.
3. `run()` is driven by either the polling loop or manual API calls through the API v3 method endpoint.

### Practical tips

- Always keep `attributes`, `actions`, and `communication` at the top level—nested models inherit the same pattern.
- Use the SDK to validate the structure before deploying; the server loader relies on the same class registry.
- For deterministic tests, configure the instance's `real_time` property before
  starting it and call its `run` method explicitly. API v3 component properties
  use `PUT /api/v3/system/instances/<id>/attr/real_time`; method calls use
  `POST /api/v3/system/instances/<id>/method/run`. See the generated OpenAPI for
  request bodies; `/models/<id>` and `/run` are not standalone REST routes.
