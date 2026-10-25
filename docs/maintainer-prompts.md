# Maintainer prompts

These instructions maintain spx-docs. They are not model-authoring or live MCP
workflows. Ordinary documentation work uses a task-specific branch based on main;
the reused catalog-sync branch belongs only to the catalog updater.

For general semantic changes, record the source commits, edit canonical pages,
run the applicable checks and submit a Docs PR. For generated content follow
[docs automation guidelines](../llm-first-model-authoring/docs-automation-guidelines.md).
Never hand-edit offline exports in Examples.

## Generated catalog update only

Use the existing catalog update workflow. Its source must be the public Examples
revision recorded in sources.json; do not repurpose the bot branch for general
prose, runtime changes or installer sources.

Historical broad prompt retired during task-navigation consolidation.
