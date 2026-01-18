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
* **Python:** `>=3.9` (tested in CI on `3.9–3.12`). `pip` available (or Conda if you prefer Conda environments).
* **Account & Subscription:** An SPX account on `https://simplephysx.com` with an active subscription (e.g., Community). After choosing a plan, you can either download a personalized Docker Compose file (includes your key) or copy a product key to use as `SPX_PRODUCT_KEY`.
* **Network:** Internet access to pull images from Docker Hub and local port **8000** available.
* **Basics for verification:** A web browser or `curl`/PowerShell (`Invoke-WebRequest`) to check `http://localhost:8000/health`.

***

## Step-by-Step Installation Process

### Create your account & choose a subscription

* Go to `https://simplephysx.com` and create an account / sign in.
* Select a subscription plan.
* Retrieve your product key (`SPX_PRODUCT_KEY`) and (if available) a personalized Docker Compose file.

> The downloaded Compose file is personalized (it embeds your key). Treat it like a secret and do not share it publicly.

### Choose your setup path

#### **Path A** — Quickest start (recommended for most users)

Use the personalized Compose you just downloaded:

1. Save the file as **docker-compose.yml** in your project folder.
2. Start the server:

   ```bash
   docker compose up -d
   ```

3. Verify the server is healthy:

   ```bash
   docker compose ps
   curl -fsS http://localhost:8000/health
   ```

#### Path B — Custom image/tag (e.g., specific alpha) or team template

Create a minimal Compose + `.env` file (recommended for teams because the key stays out of YAML).

1) Create `.env` (do not commit it; treat it as a secret):

```dotenv
# .env
SPX_PRODUCT_KEY=REPLACE_ME

# Optional: pin the server image tag.
# If you want a known-good baseline, use the tag pinned in spx-examples/docker-compose.yml.
SPX_SERVER_IMAGE=simplephysx/spx-server:v1.0.0-rc.43
```

2) Create `docker-compose.yml`:

```yaml
# docker-compose.yml
services:
  spx-server:
    image: ${SPX_SERVER_IMAGE}
    ports:
      - "8000:8000"
    environment:
      SPX_PRODUCT_KEY: ${SPX_PRODUCT_KEY}
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:8000/health > /dev/null || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - ./extensions:/app/extensions
    command: ["--address", "0.0.0.0", "--product-key", "${SPX_PRODUCT_KEY}", "--extensions", "/app/extensions"]

```

Start the server:

```bash
docker compose up -d
```

## Common commands (both paths)

### Verify

Health endpoint:

```bash
curl -fsS http://localhost:8000/health
```

Expected response shape (values may differ):

```json
{"status":"ok","server_version":"<version>","api_version":"v3"}
```

### Logs

```bash
docker compose logs --tail=200 --no-color spx-server
```

### Stop

```bash
docker compose down --remove-orphans
```

## Next steps

- [Build Your First Simulation](build-your-first-simulation.md)
- [Add a Modbus TCP/IP to Your Simulation](add-communication-protocol.md)
- [Use in Unit Tests (MiL)](use-in-unit-tests-mil.md)
- [CI/CD Setup (GitHub Actions)](ci-cd-setup-github-actions.md)
