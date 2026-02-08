---
description: >-
  Install SPX locally using the Setup Wizard from the package you download from
  simplephysx.com, then verify the UI and API on localhost.
icon: up-to-dotted-line
---

# Installation Guide

This page is the detailed, step-by-step version of the short instructions you
see on **Product & Keys**. Follow it to install SPX locally via the Setup Wizard
and verify:

- **UI**: `http://localhost:3000`
- **API**: `http://localhost:8000` (docs: `http://localhost:8000/docs`)

If you only need the SPX Server (no packs/services/UI), see
[Advanced: Manual Docker Compose (server-only)](manual-docker-compose.md).

## Prerequisites (quick checklist)

- **Account + subscription** on `https://simplephysx.com` (e.g., Community).
- **Docker Desktop / Docker Engine** with **Docker Compose v2** (`docker compose`).
- **Python 3.9+** available from a terminal (`python` or `python3`).
- Local ports **3000** (UI) and **8000** (API) available.
- Internet access (to pull Docker images and Python packages on first run).

> Security: treat your **SPX product key** as a secret. Do not commit it to git,
> paste it into public issues, or share bundles that contain it.

## 1) Get a subscription, your key, and the installer package

1. Log in to `https://simplephysx.com`.
2. Choose a subscription in **Pricing** (for example: Community).

   > **Screenshot placeholder:** Pricing page with the selected subscription plan.

3. Open **Product & Keys** in your profile (visible only when logged in).
4. Copy your **SPX product key** (you will paste it into the wizard).

   > **Screenshot placeholder:** Product & Keys page showing the product key and the download link.

5. Download the installer package (for example: `spx-examples-1.0.2.zip`).

## 2) Extract the package

Extract the `.zip` into a dedicated folder, for example:

- `spx-examples-1.0.2/`

In the extracted folder you should see platform launchers like:

- Windows: `spx-setup.bat`
- macOS: `spx-setup.command`
- Linux desktop: `spx-setup.desktop`
- macOS/Linux shells: `spx-setup.sh`

> **Screenshot placeholder:** Extracted folder showing `spx-setup.*` launchers.

## 3) Verify Docker + Python are available

The setup wizard will run checks, but doing a quick pre-flight saves time.

### Docker (all OS)

```bash
docker --version
docker compose version
docker info
```

If `docker info` fails, Docker Desktop / the Docker service is not running yet.

### Python

macOS/Linux:

```bash
python3 --version || python --version
python3 -m pip --version || python -m pip --version
```

Windows (PowerShell):

```powershell
python --version
python -m pip --version
```

If you have multiple Python installations, you can force the installer to use a
specific one by setting `PYTHON_BIN` before running setup.

## 4) Run the Setup Wizard (`spx-setup.*`)

From the extracted folder, run the launcher that matches your OS:

- **Windows:** double-click `spx-setup.bat`
- **macOS:** double-click `spx-setup.command`
- **Linux desktop:** double-click `spx-setup.desktop`
- **Terminal (macOS/Linux):** `./spx-setup.sh`

The launcher starts an interactive console wizard, generates a local bundle
(by default under `build/spx-generated/`), and then offers to start the stack.

### If your OS blocks running the launcher (common fixes)

**macOS**

- If you see “cannot be opened”, try right click → **Open**, or:

  ```bash
  chmod +x spx-setup.command spx-setup.sh
  xattr -dr com.apple.quarantine .
  ```

**Linux**

- If the `.desktop` file does not run, mark it as trusted/executable (desktop UI
  usually shows “Allow Launching”), or run:

  ```bash
  chmod +x spx-setup.sh
  ./spx-setup.sh
  ```

**Windows**

- If PowerShell script execution is blocked in your environment, run the engine
  directly from PowerShell:

  ```powershell
  powershell -ExecutionPolicy Bypass -NoProfile -File .\spx-install.ps1
  # Or (PowerShell 7):
  pwsh -ExecutionPolicy Bypass -File .\spx-install.ps1
  ```

## 5) Complete the wizard (packs / protocols / UI)

The wizard runs in the terminal and guides you through:

1. Selecting **industry packs** or choosing **by protocols** (ENTER accepts the defaults).

   > **Screenshot placeholder:** Wizard screen with “Available packages” and the selection prompt.

2. (Optional) Selecting quickstart **profiles** (if you selected packs).
3. Choosing whether to install bundled **examples** (models/instances) and which instances to start (pack flow).
4. Choosing whether to include the **SPX UI** container (recommended).
5. Pasting your **SPX product key** (copy/paste from Product & Keys).

   > **Screenshot placeholder:** Wizard prompt for “SPX Product Key”.

   If you already set `SPX_PRODUCT_KEY` in your environment, the wizard will
   detect and reuse it.

6. Reviewing the **Summary**, then starting the stack when prompted.

   > **Screenshot placeholder:** Wizard “Summary” section and the “Start the stack now?” prompt.

Tip: the wizard is designed so pressing **ENTER** keeps you on the safe default
path (recommended options enabled).

## 6) Verify the installation

After the stack starts:

1. Open the UI: `http://localhost:3000`

   > **Screenshot placeholder:** SPX UI home screen (Instances list).

2. Verify the API health:

   macOS/Linux:

   ```bash
   curl -fsS http://localhost:8000/health
   ```

   Windows (PowerShell):

   ```powershell
   (Invoke-WebRequest http://localhost:8000/health).Content
   ```

   Expected result: JSON with `"status":"ok"`.

3. Open API docs: `http://localhost:8000/docs`

   > **Screenshot placeholder:** API docs page on `/docs`.

## Where the bundle is generated

By default, the wizard writes a self-contained folder under:

- `build/spx-generated/`

Inside it you will find start/stop scripts and a generated
`docker-compose.generated.yml`. See
[Installer Wizard & Packs (Reference)](installer-and-packs.md) for the full
breakdown and automation options.

## If something fails (quick fixes)

- Wizard says Docker is not reachable: start Docker Desktop / the Docker service and retry (`docker info` should succeed).
- Wizard cannot find Python: install Python 3.9+ or set `PYTHON_BIN` to a working interpreter, then re-run setup.
- UI is not reachable on `localhost:3000`: check that the `spx-ui` container is running (see the generated bundle's start script output), and confirm port 3000 is free.
- API is not reachable on `localhost:8000`: confirm `spx-server` is up and healthy; inspect logs from the generated stack.
- Auth errors (`401`/`403`): re-copy your key from Product & Keys and re-run setup, or update the generated bundle files and restart.

For a fuller runbook, see:
[Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md).
## CORS configuration (UI access)

If you access SPX Server from the SPX UI running on a different origin (host/port), configure CORS via environment variables. In Docker runs, you can set them in `.env` and keep Compose unchanged.

Supported variables:

- `SPX_CORS_ALLOW_ORIGINS` (CSV list, default in Docker image: `*`)
- `SPX_CORS_ALLOW_CREDENTIALS` (`1` or `0`, default in Docker image: `0`)
- `SPX_CORS_ALLOW_ORIGIN_REGEX` (optional regex)

Example `.env` overrides:

```dotenv
SPX_PRODUCT_KEY=REPLACE_ME
SPX_CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
SPX_CORS_ALLOW_CREDENTIALS=1
```

> Image placeholder: Docker `.env` CORS settings with allowed UI origin.

### Verify

Health endpoint:

```bash
docker compose ps
curl -fsS http://localhost:8000/health
```

Expected response shape (values may differ):

```json
{"status":"ok","server_version":"<version>","api_version":"v3"}
```

### Logs

```bash
docker compose logs -f spx-server
docker compose logs --tail=200 --no-color spx-server
```

### Stop

```bash
docker compose down --remove-orphans
```

## Next steps

- If you installed Smart Building Pack: [Smart Building Pack: First Run Walkthrough](first-run-smart-building-pack.md)
- Start building: [Build Your First Simulation](build-your-first-simulation.md)
- Troubleshooting: [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)
