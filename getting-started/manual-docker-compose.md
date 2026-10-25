---
description: >-
  Advanced option: start the SPX Server directly via Docker Compose (server-only)
  without the Setup Wizard.
icon: terminal
---

# Advanced: Manual Docker Compose (server-only)

Use this page if you want to run only the **SPX Server API** via Docker Compose
(for example: for custom team templates, pinned image tags, or integration into
an existing stack).

If you want SPX UI + protocol services + packs, use the wizard flow instead:
[Installation Guide](installation-guide.md).

## Prerequisites

- Docker Desktop / Docker Engine with Docker Compose v2 (`docker compose`)
- A valid product key (`SPX_PRODUCT_KEY`) from `https://simplephysx.com`
- Local port `8000` available (or choose another host port)

## Option A: Use the personalized Compose from Product & Keys (if available)

Some subscriptions provide a downloadable Compose file.

1. Download it from **Product & Keys**.
2. Save it as `docker-compose.yml`.
3. Start the server:

   ```bash
   docker compose up -d
   docker compose logs -f spx-server
   ```

4. Verify:

   ```bash
   curl -fsS http://localhost:8000/health
   ```

> Security: a personalized Compose file may embed your product key. Treat it as
> a secret and do not share or commit it.

## Option B: Your own Compose + `.env` (recommended)

This keeps the product key out of YAML and works well for teams.

### 1) Create `.env`

Create a file named `.env` next to your `docker-compose.yml`:

```dotenv
SPX_PRODUCT_KEY=REPLACE_ME

# Optional: pin the image tag used by your team.
# SPX_SERVER_IMAGE=simplephysx/spx-server:<tag>
```

Do not commit `.env` to git.

Tip: if you already ran the Setup Wizard once, copy the image tag from the
generated `build/spx-generated/docker-compose.generated.yml` to keep the manual
Compose environment consistent with the wizard-based installs.

### 2) Create `docker-compose.yml`

Minimal server-only template:

```yaml
services:
  spx-server:
    image: ${SPX_SERVER_IMAGE:-simplephysx/spx-server}
    container_name: spx-server
    ports:
      - "8000:8000"
    environment:
      SPX_PRODUCT_KEY: ${SPX_PRODUCT_KEY}
    # Ensure host.docker.internal resolves on Linux (Docker Engine).
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - ./extensions:/app/extensions
    command: ["--address", "0.0.0.0", "--product-key", "${SPX_PRODUCT_KEY}", "--extensions", "/app/extensions"]
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:8000/health > /dev/null || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 3) Start and verify

```bash
docker compose up -d
docker compose ps
curl -fsS http://localhost:8000/health
```

Success criteria: `/health` returns JSON with `"status":"ok"`.

API docs are available at `http://localhost:8000/docs`.

## Logs and shutdown

Logs:

```bash
docker compose logs -f spx-server
```

Stop:

```bash
docker compose down --remove-orphans
```

## Common tweaks

- Port conflict on `8000`: change the mapping to (for example) `18000:8000`, then
  use `http://localhost:18000`.
- No extensions: remove the `./extensions:/app/extensions` volume and the
  `--extensions` CLI flag.
