---
description: >-
  Connect your Python code to a running SPX Server and perform a 10-second
  “smoke test”.
icon: python
---

# Quick Start in Python

Make sure the server is running

{% code title="macOS/Linux" %}
```bash
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
docker compose up -d
```
{% endcode %}

{% code title="Windows PowerShell" %}
```powershell
$env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
docker compose up -d
```
{% endcode %}

Server should be reachable at http://localhost:8000/

```bash
curl http://localhost:8000
```

Result message in the shell should look like below:

{% code overflow="wrap" %}
```bash
{"message":"Welcome to SPX Server API","server_version":"0.2.1-alpha.1","api_version":"v3","supported_versions":["v3"]}
```
{% endcode %}

Install the SPX-Python client

```sh
pip install spx-python
```

Connect from Python (smoke test)

{% code title="spx_smoke_test.py" %}
```python
import os 
import spx_python
client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY")  #  required env var
)
print(client.keys())  # e.g., ['models', 'instances', 'timer', 'polling']
```
{% endcode %}

(Optional) Minimal CRUD

```python
# Add a model
client["models"]["TemperatureSensor"] = {
    "attributes": {"temperature": 25.0}
}

# Create an instance
client["instances"]["sensor"] = "TemperatureSensor"
sensor = client["instances"]["sensor"]

# Read / write an attribute
sensor["attributes"]["temperature"].internal_value = 30.0
assert sensor["attributes"]["temperature"].internal_value == 30.0
```
