# Release Notes

## Coherent documentation baseline

This documentation targets the released installer bundle below. Independent
repository tag counters are not compatibility guarantees.

| Artifact | Version | Exact commit |
| --- | --- | --- |
| `spx-installer` | `v1.1.0-rc.115` | `fed6e2ab3e21efd07b7307ad7a22dcef3cfece17` |
| `spx-server` | `v1.0.0-rc.76` | `bc23bdb4fc6c9391981bb5e2180d24081993a3bf` |
| `spx-ui` | `v1.0.0-rc.76` | `e339deb98b9f83e4bbd0333ae7406320805e5252` |
| `spx-sdk` | `v1.0.0-rc.21` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` |
| `spx-python` | `v1.0.0-rc.3` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` |
| `spx-examples` | `public context snapshot` | `be71a161e97eb7a112d0581136a7b702b34cd98a` |

The machine-readable manifest is `sources.json` in `spx-docs`. The public device
catalog may advance independently through a reviewed catalog-sync PR; it does
not silently update this runtime baseline or the installer's context pin.

## Upgrade

Obtain the chosen installer from [staging Downloads](https://staging.simplephysx.com/downloads).
Record its version and the generated server/UI image tags. Use the supported
pair selected by the installer; do not substitute a newer alpha image because
its tag sorts later. Validate your MiL suite and any protocol integration you use
before adopting the new bundle. Export important snapshots before an upgrade.

Server, SDK and installer source repositories are private. Public Examples is
for models and runtime MCP modules; its fresh history does not retain the
installer's historical releases. Product packages are delivered through the
protected Downloads portal and its file-delivery host.
