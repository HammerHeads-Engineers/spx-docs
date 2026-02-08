# Code Examples

These examples intentionally use **real file paths and workflows** you can run locally.

## 0) Sanity-check: server is reachable

```bash
curl -fsS http://localhost:8000/ | head
```

## 1) Load a model + create an instance (spx-python)

```bash
python - <<'PY'
import os
import yaml
import spx_python

client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

with open("model.yaml", "r", encoding="utf-8") as f:
    model_def = yaml.safe_load(f)

client["models"]["MyModel"] = model_def
client["instances"]["my_inst"] = "MyModel"

client.prepare()
client["instances"]["my_inst"]["timer"]["time"] = 1.0
client.run()

print("OK: instance stepped to t=1.0s")
PY
```

## 2) Inspect an instance tree (spx-python)

```bash
python - <<'PY'
import os
import spx_python

client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

inst = client["instances"]["my_inst"]
print("attributes:", list(inst.get("attributes", {}).keys()))
print("timer:", inst.get("timer", {}))
PY
```

## 3) Where to find endpoint details

- Use the embedded OpenAPI reference in this chapter to discover exact paths, payloads, and auth requirements.
- For logs-related endpoints, see [Logs](../spx-core/system/logs.md).

## 4) Delete a component and inspect status flags (curl)

```bash
curl -fsS -X DELETE \
  -H "Authorization: Bearer $SPX_PRODUCT_KEY" \
  http://localhost:8000/api/v3/system/instances/my_inst
```

Expected response shape (values may differ):

```json
{
  "detail": "Component 'my_inst' deleted",
  "destroyed": true,
  "removed_from_parent": true
}
```

`destroyed` reports whether the runtime cleanup succeeded; `removed_from_parent` indicates the node was removed from the parent container.
