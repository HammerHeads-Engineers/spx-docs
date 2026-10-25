# Validation Module

The validation layer checks raw component definitions before you instantiate or register them. It combines JSON Schema, SPX-specific extensions, and custom Python validators so user-provided YAML fails fast with actionable messages instead of blowing up halfway through a simulation.

## When to validate

Run validation whenever you accept definitions from outside your codebase:

- ingesting YAML/JSON sent to `spx_sdk.registry`,  
- generating components dynamically from templates,  
- exposing an HTTP endpoint that lets users upload models or actions.

The goal is to respond with structured `ValidationError` data (422, for example) instead of a generic stack trace.

## Describe shapes with `@definition_schema`

Decorate your component or attribute classes with JSON Schema so the engine can verify the structure of incoming definitions:

```python
from spx_sdk.components import SpxComponent
from spx_sdk.validation.decorators import definition_schema


@definition_schema({
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "safe_range": {
            "type": "object",
            "properties": {
                "min": {"type": "number"},
                "max": {"type": "number"},
            },
            "required": ["min", "max"],
            "additionalProperties": False,
        },
        "sensors": {
            "type": "object",
            "x-spx-children-of": "BaseSensor",   # expect registered subclasses
        },
    },
    "required": ["name", "safe_range"],
    "additionalProperties": False,
})
class MixerModule(SpxComponent):
    ...
```

The JSON Schema backend understands SPX extensions used heavily in test coverage:

- `x-spx-child-class`: a single nested object whose key is a registered class (see `tests/test_validation/test_engine.py::ParentSingle`).
- `x-spx-children-of`: a mapping where each value is `{ClassName: {...}}`, validating each child via its schema (`ParentMap` tests).
- `x-spx-list-of`: an array of class-tagged children (`ParentList` tests).

If your schema is expensive to build, supply a callable: `@definition_schema(lambda: {...})`. The decorator stores it as a `staticmethod` so the engine can call it lazily.

Set `validation_scope="parent"` when the surrounding mapping (not just the field value) must follow the schema (for example, enforcing that an action definition contains exactly one of `{"on_set", "on_get"}` keys).

## Add custom rules with `@definition_validator`

JSON Schema covers structure, but some rules require Python. Attach them with `@definition_validator`:

```python
from spx_sdk.validation.decorators import definition_validator
from spx_sdk.validation.errors import ValidationCode, ValidationError


def _ensure_thresholds(cls, definition, registry, path):
    errors = []
    hi = definition.get("safe_range", {}).get("max")
    lo = definition.get("safe_range", {}).get("min")
    if hi is not None and lo is not None and hi <= lo:
        errors.append(ValidationError(
            code=ValidationCode.INVALID_SHAPE,
            message="max must be greater than min",
            path=tuple(path) + ("safe_range",),
            context={"min": lo, "max": hi},
        ))
    return errors


@definition_validator(_ensure_thresholds)
class MixerModule(SpxComponent):
    ...
```

Validators receive:

- `cls`: the class being validated,
- `definition`: the raw dict/list,
- `registry`: the registry passed to the engine (or `None`),
- `path`: a tuple describing where in the JSON tree the validator runs.

Return a `ValidationError`, any iterable of errors, or a `ValidationResult`; the engine normalises all forms (see `_as_error_list` tests).

## Run validation programmatically

For point checks, call the helper:

```python
from fastapi import HTTPException
from spx_sdk.validation.engine import validate_component_definition

incoming = {
    "name": "heater-1",
    "safe_range": {"min": 15, "max": 80},
    "sensors": {
        "ambient": {"Thermocouple": {"channel": 1}},
    },
}

result = validate_component_definition("MixerModule", incoming, registry=my_registry)
if not result.ok:
    raise HTTPException(
        status_code=422,
        detail=result.to_compact_list(include_context=True),
    )
```

`validate_component_definition` accepts either a class object or a class name. When you pass a string, the engine resolves it through the supplied registry (or the global `spx_sdk.registry`). Unknown classes produce a single `ValidationError` with code `ValidationCode.UNKNOWN_CLASS`.

## Validate entire documents

When users upload a full YAML with models, instances, and wiring, use `validate_document` to walk the structure without bootstrapping the runtime:

```python
import yaml
from spx_sdk.validation.engine import validate_document

doc = yaml.safe_load(open("system.yaml"))
res = validate_document(doc, registry=my_registry, root_class="System")
if not res.ok:
    for err in res.errors:
        print(f"{err.code} at {err.path}: {err.message}")
```

The engine performs a depth-first traversal, attempts to resolve each mapping key as a registered class, and, when a schema exists, validates that node. Errors bubble with precise paths such as `("models", "Heater", "actions", 0, "set")`, which you can render via `pretty_path(err.path)` or the `path_str` returned by `ValidationError.to_dict()`.

## Reporting results back to clients

`ValidationResult` wraps a simple `ok` flag plus the list of errors. Each `ValidationError` contains:

- `code`: stable enum (`ValidationCode`) like `MISSING_REQUIRED` or `TYPE_MISMATCH`,
- `message`: human-readable explanation,
- `path`: tuple pointing to the failing location,
- `expected`/`actual` payloads for numeric comparisons,
- optional `context` dict for problem-specific hints.

Helper functions in `spx_sdk.validation.errors` make it easy to build responses:

```python
from spx_sdk.validation.errors import errors_summary

summary = errors_summary(result.errors)
# "missing_required at models.Heater.safe_range.max; type_mismatch at models.Heater.actions[0]"
```

Use `result.to_compact_list(include_context=True)` whenever you need a machine-friendly structure (ideal for HTTP JSON bodies).

## Typical workflow

1. Decorate every public component/attribute/action class with `@definition_schema`.
2. Attach `@definition_validator` for cross-field or domain-specific checks.
3. Run `validate_component_definition` or `validate_document` before persisting user input or attempting to instantiate the system.
4. Surface `ValidationResult` data to users; reserve `SpxFault` for runtime failures.
