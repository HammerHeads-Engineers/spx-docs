---
description: >-
  This page shows how to launch the SPX Server locally with Docker—using either
  the personalized Docker Compose from the License Keys page or your own
  template—and verify it responds on your machine.
icon: up-to-dotted-line
---

# Installation Guide

In this Installation Guide you’ll perform one simple task: start the SPX Server in Docker and confirm it’s reachable on your computer. After selecting a subscription on `https://simplephysx.com`, you can either use a personalized Docker Compose file (fastest) or a custom template (e.g., to pin an image tag). We’ll cover the prerequisites, show how to bring the container up, and how to check that the server answers locally.

## Requirements

* **Docker Desktop**
  * **Windows:** Install **Docker Desktop for Windows** (WSL 2 backend). Ensure **WSL 2** is enabled, the WSL kernel update is installed, and **virtualization** is enabled in BIOS/UEFI. Start Docker Desktop before proceeding.
  * **macOS:** Install **Docker Desktop for Mac** (Intel or Apple Silicon) and start it.
  *   Quick check:

      ```bash
      docker --version
      docker compose version
      ```
* **Python:** Version **3.9–3.12** (3.10+ recommended). `pip` available (or Conda if you prefer Conda environments).
* **Account & Subscription:** An SPX account on `https://simplephysx.com` with an active subscription (e.g., Community). After choosing a plan, you can either download a personalized Docker Compose file (includes your key) or copy a product key to use as `SPX_PRODUCT_KEY`.
* **Network:** Internet access to pull images from Docker Hub and local port **8000** available.
* **Basics for verification:** A web browser or `curl`/PowerShell (`Invoke-WebRequest`) to check `http://localhost:8000/`.

***

## Step-by-Step Installation Process

### &#x20;Create your account & choose a subscription

* Go to `https://simplephysx.com` and create an account / sign in.
* Select a subscription plan.
* Retrieve your product key (`SPX_PRODUCT_KEY`) and (if available) a personalized Docker Compose file.

> The downloaded Compose file is personalized (it embeds your key). Treat it like a secret and do not share it publicly.

### Choose your setup path

#### **Path A** — Quickest start **(recommended for most users)**&#x20;

Use the personalized Compose you just downloaded:&#x20;

1. Save the file as **docker-compose.yml** in your project folder.
2. Run:

```bash
docker compose up -d
```

#### Path B — Custom image/tag (e.g., specific alpha) or team template

Create your own Compose file and pass the key via an environment variable:

Set your key in the shell (do not hard-code it):

* macOS/Linux

```bash
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
```

* Windows PowerShell

```powershell
setx SPX_PRODUCT_KEY "YOUR_REAL_KEY"
$env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
```

Use a minimal **docker-compose.yml** and pin any image tag you need:

{% code title="docker-compose.yml" %}
{% tabs %}
{% tab title="YAML" %}
```yaml
services:
  spx-server:
    # Pick a tag that matches your environment (for example, align with spx-examples).
    image: simplephysx/spx-server:<tag>
    ports: ["8000:8000"]
    environment:
      SPX_PRODUCT_KEY: ${SPX_PRODUCT_KEY}
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/ || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      # Mount local SPX core and extensions for development/testing
      - ./extensions:/app/extensions:ro
    command: ["--address", "0.0.0.0", "--product-key", "${SPX_PRODUCT_KEY}", "--extensions", "/app/extensions"]

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "services": {
    "spx-server": {
      "image": "simplephysx/spx-server:<tag>",
      "ports": ["8000:8000"],
      "environment": {
        "SPX_PRODUCT_KEY": "${SPX_PRODUCT_KEY}"
      },
      "healthcheck": {
        "test": ["CMD-SHELL", "curl -f http://localhost:8000/ || exit 1"],
        "interval": "10s",
        "timeout": "5s",
        "retries": 5
      },
      "volumes": [
        "./extensions:/app/extensions:ro"
      ],
      "command": [
        "--address",
        "0.0.0.0",
        "--product-key",
        "${SPX_PRODUCT_KEY}",
        "--extensions",
        "/app/extensions"
      ]
    }
  }
}

```
{% endtab %}
{% endtabs %}

{% endcode %}

Start the server:

```bash
docker compose up -d
```

#### Verify the server is up Open [http://localhost:8000/](http://localhost:8000/) (or a simple status/root endpoint).&#x20;

You should get HTTP 200 / OK (example response shape):

```sh
{"message":"Welcome to SPX Server API","api_version":"v3","supported_versions":["v3"]}
```

If not, wait a few seconds and retry.
