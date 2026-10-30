# Documentation source audit

## Baseline and scope

The portal inventory below covers every Markdown page in SUMMARY. All local
links, fragments, HTML image paths, navigation targets and model-serialization
parity are checked by `scripts/check_docs.py`. Implementation sources were read
from the exact released versions in `sources.json`; public catalog pinning is
separate from the released installer context. This is an implementation and
simulation audit, not physical device or manufacturer certification.

## Executed technical checks

- Server RC76 / SDK RC21 dependency lock exported from the tagged server tree.
- 85 API/model/meta-parameter tests passed in one isolated run.
- 27 connection tests passed in a separate process.
- 15 OPC UA binding/export and OCPP generated-response tests passed.
- `scripts/verify_runtime_sample.py`: identical YAML/JSON registration through
  the real API v3 router and Python RC3, rejected missing/incorrect credentials,
  RUNNING instances, deterministic input-to-telemetry propagation and cleanup.
- OpenAPI regenerated from both released routers: 10 path templates, correct
  product title/version, bearer security on API v3 and public health/version routes.
- UI RC76: 13 Jest suites / 55 unit tests passed with locked dependencies
  under the available Node 24 runtime; the application declares Node 22. This
  verifies client/state utilities, not a fresh browser/hardware qualification.
- Generator guards cover invalid/missing revisions, public-source allowlisting,
  meaningful-content comparison and Markdown anchors.

No physical BLE, PROFINET, Matter, KNX, BACnet or other hardware qualification
was performed. Protocol pages describe implemented roles and optional bridges;
source/test evidence does not establish physical conformance.

## Corrections applied

- Replace public-repository installer/Compose commands with installed SPX Setup
  and explicitly separate private maintainer workflows.
- Align download UI and EXE/PKG/TGZ delivery with the migrated release system.
- Centralize YAML/JSON semantics, preserve complete offline model/MCP context,
  and clarify persistent controls, commands, units, wrapper direction and ports.
- Correct API v3 method/property routes, action shapes, initialization parameters,
  module declarations, snapshot configuration and unsupported CLI claims.
- Remove duplicated stale catalog counts and invalid GitBook page references.
- Document current UI Settings/managed proxy and RC76 OPC UA write-direction policy.
- Replace old version-branch instructions with main and two reviewed bot flows.

## Readability follow-up — 30 October 2026

This change addresses the five instruction/structure findings against Docs
baseline `67f0c8123fc309069b7a19c7870a3ca15164de32` (abbreviated `67f0c81`
below). It keeps the public page locations, runtime version set and generated
tutorial programs unchanged.

| Changed instructions | Source / exact revision | Correction and evidence |
| --- | --- | --- |
| [First Python program](../simulation-and-modeling/using-spx-python.md) and its follow-up | Docs `requirements-tutorials.txt` and `examples/tutorials/client_sensor.py`, `67f0c81`; published `spx-python==1.0.0rc3` | Added working-directory, venv, installation and session-variable commands for macOS/Linux and PowerShell. The POSIX blocks were executed on macOS/Python 3.12 with a placeholder key and package-version assertions. PowerShell was reviewed, not executed on Windows. |
| UI prerequisites in the [first exercise](../getting-started/README.md) and [UI path](../guides/ui.md) | Docs `ui-reference/settings.md`, `67f0c81`; UI baseline `e339deb98b9f83e4bbd0333ae7406320805e5252` | Replaced server-selection instructions with managed connection checks, Setup/start and Retry. This is a wording alignment with the existing reference, not a fresh browser run. |
| First UI exercise and [main walkthrough](../guides/ui-instance.md) | Docs UI guides, `67f0c81` | One main instance walkthrough; paste-YAML prepares only the same model. Both paths continue to connections without recreating the sensor. |
| [Agent contribution workflow](../llm-first-model-authoring/workflow-generate-validate-iterate.md), catalog guidance and completion checklist | Public Examples `AGENTS.md`, `library/catalog/models.yaml` and `tools/validate_models.py`, `be71a161e97eb7a112d0581136a7b702b34cd98a` | Fixed shell continuation and provided a complete standalone catalog entry. The exact copy command and YAML fragments were applied to a temporary copy of that public revision; its model/catalog validator passed. The fault is opt-in and started explicitly by its test. |
| Model/Docs task boundaries and [Docs maintenance checklist](documentation-maintenance.md) | Docs maintenance/automation guides, `67f0c81`; public Examples `AGENTS.md`, `be71a161e97eb7a112d0581136a7b702b34cd98a` | Removed Docs generation commands from the model workflow/template and moved the Docs checklist to maintenance instructions. Examples and Docs commands identify their own checkout and PR target. |

Validation on Python 3.12: 19 public tests passed; Markdown links/anchors/assets,
navigation, generated tutorial blocks and the device catalog at the exact public
pin passed. Publication verification applies after merge; local edits do not
change the currently published site. No new live server or protocol exchange
was required for these editorial corrections.

## Runtime test issue observed (outside documentation scope)

Combining API helper tests and connection tests in a single pytest process
produced two connection failures because a test changed the global component
registry. The same connection suite passed 27/27 in isolation; the API/model
suite passed 85/85 separately. No runtime fix was introduced. Keep isolation
until the shared registry fixture is restored reliably in the source test suite.

## Publication and automation validation

GitBook's existing space was reconfigured from version-1.0.0 to main with
GitHub → GitBook as the initial direction. The same site/domain and OpenAPI
identity are retained. `hammerheadsengineers-api` imports the checked-in schema
from the public main URL, with GitBook's six-hour refresh interval.

Both daily/manual workflows were executed on GitHub Actions. Unchanged canonical
model/MCP pages and catalog content did not create new PRs or update provenance.
A second catalog run after the Examples README/context merge also produced no
changes, demonstrating that the two flows do not feed back into each other.
Installer staging accepted all 160 committed context files with full offline
provenance; existing agent/MCP guards, imports and tool inventory passed. The
50 installer context/workspace documentation tests also passed. The released
installer context pin was deliberately not changed by a documentation update.

## Page evidence inventory

The source column identifies the implementation section used for the page's
contract. Private source paths are maintainer evidence, not prerequisites for
public readers. Historical editorial reports under `docs/` are retained as
history and are not product-reference pages in SUMMARY.

| Documentation page | Source section | Exact source commit | Verification scope |
| --- | --- | --- | --- |
| [README.md](../README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [overview/introduction.md](../overview/introduction.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [overview/start-here.md](../overview/start-here.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [overview/purpose-and-key-features.md](../overview/purpose-and-key-features.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [overview/use-case-and-applications.md](../overview/use-case-and-applications.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [overview/system-requirements-and-capability.md](../overview/system-requirements-and-capability.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/README.md](../getting-started/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/installation-guide.md](../getting-started/installation-guide.md) | `spx-installer` `installer/compatibility.py` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` | Structural check; source contract review by section |
| [getting-started/connect-llm-with-spx-mcp.md](../getting-started/connect-llm-with-spx-mcp.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/mcp-reference.md](../getting-started/mcp-reference.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/manual-docker-compose.md](../getting-started/manual-docker-compose.md) | `spx-installer` `installer/compatibility.py` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` | Structural check; source contract review by section |
| [getting-started/first-run-smart-building-pack.md](../getting-started/first-run-smart-building-pack.md) | `spx-installer` `installer/compatibility.py` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` | Structural check; source contract review by section |
| [getting-started/build-your-first-simulation.md](../getting-started/build-your-first-simulation.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/choose-a-protocol-adapter.md](../getting-started/choose-a-protocol-adapter.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/add-communication-protocol.md](../getting-started/add-communication-protocol.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/modbus-client-controller.md](../getting-started/modbus-client-controller.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/extend-with-custom-component.md](../getting-started/extend-with-custom-component.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/advanced-setup.md](../getting-started/advanced-setup.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/installer-and-packs.md](../getting-started/installer-and-packs.md) | `spx-installer` `installer/compatibility.py` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` | Structural check; source contract review by section |
| [getting-started/code-defined-simulations.md](../getting-started/code-defined-simulations.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/snapshots-guide.md](../getting-started/snapshots-guide.md) | `spx-server` `spx_core/snapshots/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/use-in-unit-tests-mil.md](../getting-started/use-in-unit-tests-mil.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [getting-started/ci-cd-setup-github-actions.md](../getting-started/ci-cd-setup-github-actions.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [llm-first-model-authoring/README.md](../llm-first-model-authoring/README.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/docs-automation-guidelines.md](../llm-first-model-authoring/docs-automation-guidelines.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/repo-as-spec.md](../llm-first-model-authoring/repo-as-spec.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/model-brief-template.md](../llm-first-model-authoring/model-brief-template.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/workflow-generate-validate-iterate.md](../llm-first-model-authoring/workflow-generate-validate-iterate.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/prompt-recipes.md](../llm-first-model-authoring/prompt-recipes.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [llm-first-model-authoring/definition-of-done.md](../llm-first-model-authoring/definition-of-done.md) | `spx-examples` `AGENTS.md` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [usage-scenarios-and-examples/README.md](../usage-scenarios-and-examples/README.md) | `spx-examples` `library/catalog/models.yaml` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [usage-scenarios-and-examples/common-use-cases.md](../usage-scenarios-and-examples/common-use-cases.md) | `spx-examples` `library/catalog/models.yaml` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [usage-scenarios-and-examples/industry-packs.md](../usage-scenarios-and-examples/industry-packs.md) | `spx-examples` `library/catalog/models.yaml` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [usage-scenarios-and-examples/device-catalog.md](../usage-scenarios-and-examples/device-catalog.md) | `spx-examples` `library/catalog/models.yaml` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [spx-development-guide/README.md](../spx-development-guide/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/README.md](../simulation-and-modeling/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/core-concepts.md](../simulation-and-modeling/core-concepts.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/model-definition-reference.md](../simulation-and-modeling/model-definition-reference.md) | `spx-examples` `library/catalog/models.yaml` | `be71a161e97eb7a112d0581136a7b702b34cd98a` | Structural check; source contract review by section |
| [simulation-and-modeling/model-in-the-loop.md](../simulation-and-modeling/model-in-the-loop.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/using-spx-python.md](../simulation-and-modeling/using-spx-python.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/README.md](../simulation-and-modeling/extending-simulations/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/protocol-adapters.md](../simulation-and-modeling/extending-simulations/protocol-adapters.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/filters-and-signal-processing.md](../simulation-and-modeling/extending-simulations/filters-and-signal-processing.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/custom-actions-and-logic.md](../simulation-and-modeling/extending-simulations/custom-actions-and-logic.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/hardware-bridges-and-backends.md](../simulation-and-modeling/extending-simulations/hardware-bridges-and-backends.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/ble-device-simulation.md](../simulation-and-modeling/extending-simulations/ble-device-simulation.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [simulation-and-modeling/extending-simulations/testing-and-hot-reload.md](../simulation-and-modeling/extending-simulations/testing-and-hot-reload.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/README.md](../spx-development-guide/spx-sdk/README.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/quick-start-spx-sdk-in-5-minutes.md](../spx-development-guide/quick-start-spx-sdk-in-5-minutes.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/registry.md](../spx-development-guide/spx-sdk/registry.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/components/README.md](../spx-development-guide/spx-sdk/components/README.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/components/spxcomponent.md](../spx-development-guide/spx-sdk/components/spxcomponent.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/components/spxcontainer-the-smart-loader-that-wires-your-sub-components.md](../spx-development-guide/spx-sdk/components/spxcontainer-the-smart-loader-that-wires-your-sub-components.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/attributes.md](../spx-development-guide/spx-sdk/attributes.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/actions.md](../spx-development-guide/spx-sdk/actions.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/model.md](../spx-development-guide/spx-sdk/model.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/logic.md](../spx-development-guide/spx-sdk/logic.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/communication.md](../spx-development-guide/spx-sdk/communication.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/hooks.md](../spx-development-guide/spx-sdk/hooks.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/diagnostics.md](../spx-development-guide/spx-sdk/diagnostics.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/validation.md](../spx-development-guide/spx-sdk/validation.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/best-practices.md](../spx-development-guide/spx-sdk/best-practices.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/imports/README.md](../spx-development-guide/spx-sdk/imports/README.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-development-guide/spx-sdk/imports/pythonfile.md](../spx-development-guide/spx-sdk/imports/pythonfile.md) | `spx-sdk` `spx_sdk/` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` | Structural check; source contract review by section |
| [spx-core/README.md](../spx-core/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/README.md](../spx-core/system/README.md) | `spx-server` `spx_core/system/__init__.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/model.md](../spx-core/system/model.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/instances.md](../spx-core/system/instances.md) | `spx-server` `spx_core/system/instances.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/modules.md](../spx-core/system/modules.md) | `spx-server` `spx_core/system/modules.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/parameters.md](../spx-core/system/parameters.md) | `spx-server` `spx_core/system/init_parameters.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/connections.md](../spx-core/system/connections.md) | `spx-server` `spx_core/system/connections.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/timer.md](../spx-core/system/timer.md) | `spx-server` `spx_core/system/timer.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/polling.md](../spx-core/system/polling.md) | `spx-server` `spx_core/system/polling.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/logs.md](../spx-core/system/logs.md) | `spx-server` `spx_core/system/logs.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/scenarios.md](../spx-core/system/scenarios.md) | `spx-server` `spx_core/system/scenarios.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/system/templates.md](../spx-core/system/templates.md) | `spx-server` `spx_core/system/templates.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/actions.md](../spx-core/actions.md) | `spx-server` `spx_core/actions/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/README.md](../spx-core/communications/README.md) | `spx-server` `spx_core/communications/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/ascii.md](../spx-core/communications/ascii.md) | `spx-server` `spx_core/communications/ascii/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/http.md](../spx-core/communications/http.md) | `spx-server` `spx_core/communications/http/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/mqtt.md](../spx-core/communications/mqtt.md) | `spx-server` `spx_core/communications/mqtt/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/modbus.md](../spx-core/communications/modbus.md) | `spx-server` `spx_core/communications/modbus_slave/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/ble.md](../spx-core/communications/ble.md) | `spx-server` `spx_core/communications/ble/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/bacnet.md](../spx-core/communications/bacnet.md) | `spx-server` `spx_core/communications/bacnet/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/knx.md](../spx-core/communications/knx.md) | `spx-server` `spx_core/communications/knx/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/opcua.md](../spx-core/communications/opcua.md) | `spx-server` `spx_core/communications/opcua/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/profinet.md](../spx-core/communications/profinet.md) | `spx-server` `spx_core/communications/profinet/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/dali.md](../spx-core/communications/dali.md) | `spx-server` `spx_core/communications/dali/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/mbus.md](../spx-core/communications/mbus.md) | `spx-server` `spx_core/communications/mbus/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/coap.md](../spx-core/communications/coap.md) | `spx-server` `spx_core/communications/coap/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/lwm2m.md](../spx-core/communications/lwm2m.md) | `spx-server` `spx_core/communications/lwm2m/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/matter.md](../spx-core/communications/matter.md) | `spx-server` `spx_core/communications/matter/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/ocpp.md](../spx-core/communications/ocpp.md) | `spx-server` `spx_core/communications/ocpp/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/snmp.md](../spx-core/communications/snmp.md) | `spx-server` `spx_core/communications/snmp/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/communications/redfish.md](../spx-core/communications/redfish.md) | `spx-server` `spx_core/communications/redfish/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/snapshots.md](../spx-core/snapshots.md) | `spx-server` `spx_core/snapshots/` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-core/extending.md](../spx-core/extending.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-development-guide/spx-python-client-wrapper/README.md](../spx-development-guide/spx-python-client-wrapper/README.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [spx-development-guide/spx-python-client-wrapper/overview-and-installation.md](../spx-development-guide/spx-python-client-wrapper/overview-and-installation.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [spx-development-guide/spx-python-client-wrapper/usage-and-examples.md](../spx-development-guide/spx-python-client-wrapper/usage-and-examples.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [spx-development-guide/spx-python-client-wrapper/testing-helpers-and-logging.md](../spx-development-guide/spx-python-client-wrapper/testing-helpers-and-logging.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [spx-development-guide/spx-python-client-wrapper/advanced-and-best-practices.md](../spx-development-guide/spx-python-client-wrapper/advanced-and-best-practices.md) | `spx-python` `spx_python/client.py` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` | Structural check; source contract review by section |
| [tooling-and-ui/README.md](../tooling-and-ui/README.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/README.md](../ui-reference/README.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/general-view.md](../ui-reference/general-view.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/instances.md](../ui-reference/instances.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/models.md](../ui-reference/models.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/connections.md](../ui-reference/connections.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/logs.md](../ui-reference/logs.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/timer-and-polling.md](../ui-reference/timer-and-polling.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/snapshots.md](../ui-reference/snapshots.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [ui-reference/settings.md](../ui-reference/settings.md) | `spx-ui` `app/` | `e339deb98b9f83e4bbd0333ae7406320805e5252` | Structural check; source contract review by section |
| [spx-development-guide/quick-guide-connecting-vs-code-to-your-running-spx-server-container-in-5-minutes.md](../spx-development-guide/quick-guide-connecting-vs-code-to-your-running-spx-server-container-in-5-minutes.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [operations-and-support/README.md](../operations-and-support/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [spx-development-guide/server-api/README.md](../spx-development-guide/server-api/README.md) | `spx-server` `spx_server/api/api_v3.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [api-v3-reference/README.md](../api-v3-reference/README.md) | `spx-server` `spx_server/api/api_v3.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [api-v3-reference/code-examples.md](../api-v3-reference/code-examples.md) | `spx-server` `spx_server/api/api_v3.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [testing-and-validation.md](../testing-and-validation.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [performance-optimization.md](../performance-optimization.md) | `spx-server` `spx_core/system/polling.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [security-considerations.md](../security-considerations.md) | `spx-server` `spx_server/server.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [integration-with-other-systems.md](../integration-with-other-systems.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [troubleshooting-and-support/README.md](../troubleshooting-and-support/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [troubleshooting-and-support/common-issues-and-solutions.md](../troubleshooting-and-support/common-issues-and-solutions.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [troubleshooting-and-support/faqs.md](../troubleshooting-and-support/faqs.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [troubleshooting-and-support/how-to-get-support.md](../troubleshooting-and-support/how-to-get-support.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [release-notes.md](../release-notes.md) | `spx-installer` `installer/compatibility.py` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` | Structural check; source contract review by section |
| [docs/DOCS_BACKLOG_V1_0_0_SYNC.md](../docs/DOCS_BACKLOG_V1_0_0_SYNC.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [appendices/README.md](../appendices/README.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [appendices/glossary-of-terms.md](../appendices/glossary-of-terms.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [appendices/licensing-information.md](../appendices/licensing-information.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
| [appendices/additional-resources-and-readings.md](../appendices/additional-resources-and-readings.md) | `spx-server` `spx_core/system/model.py` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` | Structural check; source contract review by section |
