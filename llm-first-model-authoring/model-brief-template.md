---
hidden: true
---

# Model Brief template

Copy this template into an issue/PR description before asking an LLM to generate or modify a model.

## 0) Branch and target

* Working branch (docs automation): `codex/docs-sync-latest-commits-v1-0-0`
* Rebase base branch: `origin/version-1.0.0`
* PR target branch: `version-1.0.0`

## 1) Goal

* What device/system are we modeling?
* What is the Software Under Test (SUT)?
* What protocols must the SUT use (Modbus/MQTT/HTTP/SCPI/BLE/etc.)?
* What exact behavior must be testable (happy path + fault path)?

## 2) Source snapshot (pin required)

* Source repo(s): `spx-examples`, `<other repo if any>`
* Source commit SHA(s):
  * `spx-examples`: `<sha>`
  * `<other repo>`: `<sha>`
* External docs (datasheet/spec/register map URLs):
  * `<url_1>`
  * `<url_2>`

## 3) Starting point (spx-examples template)

* Template file: `library/domains/<domain>/<vendor|generic>/<template>.yaml`
* Template URL: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/<domain>/<vendor|generic>/<template>.yaml`
* New model path: `library/domains/<domain>/<vendor|generic>/<new_model>.yaml`

## 4) Protocol mapping scope

* Attributes to expose:
  * `<attr_name>`: `<type>`, unit `<unit>`, direction `<read|write|rw>`
* Protocol mapping:
  * `<protocol detail (register/topic/endpoint/command)>`
* Non-goals (must not be implemented/invented):
  * `<out of scope items>`

## 5) Catalog and pack impact

* `library/catalog/models.yaml`: `<add/update/no change>`
* `library/catalog/domains.yaml`: `<add/update/no change>`
* `library/catalog/services.yaml`: `<add/update/no change>`
* `library/catalog/industries.yaml` + `profiles/<pack>/*.yaml`: `<add/update/no change>`

## 6) Tests and validation

* New/updated test files:
  * `<tests/.../test_*.py>`
* Deterministic constraints:
  * no wall-clock coupling
  * time driven from tests
* Validation commands:
  * `python tools/validate_models.py`
  * `pytest` (or `poetry run pytest`)

## 7) Documentation impact

* Pages to update in `spx-docs`:
  * `<path/to/page.md>`
* Generated pages impacted:
  * `usage-scenarios-and-examples/device-catalog.md` (`yes/no`)
* If yes, regeneration command:
  * `python scripts/generate_device_catalog.py --spx-examples ../spx-examples`

## 8) Required output from automation

* File-by-file patch summary.
* Source snapshot commit SHA(s).
* Evidence matrix (`docs section -> source -> commit -> rationale`).
* Open assumptions/questions (if data is incomplete).
