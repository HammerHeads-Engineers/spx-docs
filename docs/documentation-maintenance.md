# Documentation maintenance and acceptance

Canonical source: spx-docs/main. Product version inputs live in `sources.json`;
changing a catalog pin does not change the runtime baseline. Current public
entry point: [Start here](../overview/start-here.md).

## Page contract

A task tutorial states its audience/execution layer, version prerequisites,
working directory, complete files, commands, expected result and cleanup.
Reference fragments and signatures are labelled as fragments/text; VS Code
configuration with comments is `jsonc`. Protocol recipes state their backend,
SUT and qualification limits. Do not label a successful API call as protocol proof.

Keep complete SDK/client tutorial programs under `examples/tutorials/` and
publish them through `<!-- tutorial:filename.py:start/end -->` markers.
After editing a program run `python scripts/render_tutorials.py`.

## Public checks (Python 3.12)

In a virtual environment from the Docs checkout:

```bash
python -m pip install -r requirements-tutorials.txt
python scripts/render_tutorials.py --check
python scripts/check_docs.py
python -m unittest discover -s tests -v
```

The CI also fetches the exact allowed public catalog revision and verifies
regeneration. It does not access private server sources or real product keys.
These checks distinguish links/parsing, generated source consistency and executed
SDK/client contracts; they are not an all-protocol test suite.

## Private runtime contracts

The private server repository's **Documentation runtime contracts** workflow
accepts a reviewed immutable public Docs SHA. It reads that manifest, checks out
the exact server revision, installs its dependency lock and runs:

```bash
python scripts/verify_tutorial_runtime.py -v
```

The working directory is the public Docs checkout and PYTHONPATH points to the
private released server sources. No real product key or Docker/hardware is needed;
the tests use in-process FastAPI and temporary snapshot storage. Untrusted fork
code is excluded. Record the tested Docs SHA and workflow result in the PR.

## Publication and offline references

After a reviewed merge, wait for GitBook main publication. Run:

```bash
python scripts/check_published.py --output /tmp/spx-published-check.json
```

This reads every URL in `llms.txt`, verifies corrected pages and the archive
redirect, and rejects unfinished UI/link placeholders. It is a deployment check,
not a required pre-merge check against the still-old site.

In public Examples use the existing `scripts/sync_docs_context.py` with the
exact merged Docs commit; never hand-edit generated MODEL_LANGUAGE/MCP exports.
Check the pinned export, README catalog and docs tests, then release the context
through the normal develop → main process. Do not change an installer pin or
publish a product release as a side effect of refreshing documentation.
