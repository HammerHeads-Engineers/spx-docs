# How to Get Support

Contact [info@simplephysx.com](mailto:info@simplephysx.com) with the subject
`SPX support — <short problem>`. Include a small reproducible example and the
information below. Do not send product keys or credentials.

## Minimal diagnostic package

- Expected versus actual result and exact sanitized error.
- Installer version, generated server/UI image tags, SDK/client versions when used.
- Installation shape: managed SPX Tools, managed MCP workspace, public checkout,
  or project-owned Compose; OS, Docker and Python/interpreter where relevant.
- Minimal model and steps/commands, including relevant instance keys and inputs.
- Sanitized server logs around the failure; adapter/backend/SUT versions and
  non-sensitive port/mapping details for protocol failures.

For a managed environment locate the Setup-selected generated directory and run:

```bash
docker compose -f docker-compose.generated.yml logs --tail=200 --no-color spx-server
```

For a custom deployment substitute its actual Compose filename. For MCP, include
the doctor/error result and interpreter path, not the private connection file.
See [Common Issues](common-issues-and-solutions.md) for installation-specific checks.

## Before sharing

Remove `SPX_PRODUCT_KEY`, Authorization/Bearer headers, tokens, passwords, private
connection bindings, signed download URLs and unrelated personal/device data.
Review generated Compose, `.env`, snapshots and logs manually. Replace secrets
with `<redacted>` while preserving field names and the sequence that reproduces
the problem. Prefer a minimal sanitized model over a full workspace archive.
