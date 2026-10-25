---
description: >-
  Develop and live-test your own SPX extensions inside the same Docker image
  that runs the server, without copying files back and forth.
icon: microsoft
---

# Quick Guide – Connecting VS Code to your running SPX-Server container in 5 minutes

### Requirements ✅

* **Docker image is available locally** – either built from the repo or pulled from Docker Hub (`spx-server`).
* **Container is running** and port **8000** is forwarded to the host.
* Hitting `http://localhost:8000` (browser or `curl`) returns a `200 OK` from SPX-Server.
* **VS Code** with the **Remote – Containers** extension is installed on your workstation.

> Once these checks pass, continue with mounting your extension workspace and attaching VS Code.

***

#### **Create (or pick) a workspace for your extensions**

1. On your host, make a parent folder for everything you’ll write:

```bash
mkdir -p ~/spx_extensions
cd ~/spx_extensions
```

2. Inside it, add (or clone) any extension packages you’re experimenting with.

Example:

```bash
mkdir my_first_extension
touch my_first_extension/__init__.py
```

> You can have many extension sub-folders here; the entire \~/spx\_extensions tree will be mounted into the container later.

#### **Add VS Code’s devcontainer description**

Create a folder called .devcontainer at the root of your workspace and drop a devcontainer.json file inside:

```bash
mkdir .devcontainer
code .devcontainer/devcontainer.json
```

Paste the snippet below and save.

{% code title=".devcontainer/devcontainer.json" %}
```json
{
  // VS Code will use this file to build and run the container
  "name": "SPX Server Dev",
  "image": "simplephysx/spx-server:v0.2.1-alpha.2", // tag

  // ports forwarded from container to host
  "forwardPorts": [8000],

  // VS Code settings inside the container
  "customizations": {
    "vscode": {
      // default VS Code settings inside the container
      "settings": {
        // default Python interpreter
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      },
      // extensions to automatically install in the container
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy"
      ]
    }
  },

  // volumes / bind-mounts (eases working on extensions)
  "mounts": [
    "source=${localWorkspaceFolder}/extensions,target=/app/extensions,type=bind,consistency=cached"
  ]
}
```
{% endcode %}

#### &#x20;**Open the folder inside the container**

1. Launch VS Code in your local workspace (code \~/spx\_extensions).
2.  When the _Dev Containers_ extension prompts “Rebuild and Reopen in Container” or "Rebuild Container", click it.

    VS Code will:

    * attach the container,
    * attach a VS Code server inside.

> First build can take a minute or two. Subsequent opens are instant.

**Verify the environment**

Create hello.py in the workspace root:

{% code title="hello.py" %}
```python
from spx_sdk import __version__ as sdk_ver
from spx_core import __version__ as core_ver

print("SPX-SDK:", sdk_ver)
print("SPX-Core:", core_ver)
```
{% endcode %}

Run it from VS Code

You should see the installed version numbers printed 🎉
