# Release Notes

## SPX 1.0 — 5 November 2026

SPX 1.0 is the stable product baseline. Its native/portable installer is
version **1.1.0**, bundling **SPX Server 1.0.0** and **SPX UI 1.1.0**.
These components have separate version series. A portal card labelled
"SPX installer 1.1.0" and a website build version do not change the product baseline.

## Coherent documentation baseline

This documentation targets the released installer bundle below. Independent
repository tag counters are not compatibility guarantees.

<!-- release-bundle:start -->
| Artifact | Version | Exact commit |
| --- | --- | --- |
| `spx-installer` | `v1.1.0` | `5752dde71f7a4a3bbaad13ae67e32ebda4f2d721` |
| `spx-server` | `v1.0.0` | `215b9214c48c6c787b9a68b89178916239a57452` |
| `spx-ui` | `v1.1.0` | `b70c9ae521e40ef7d596f866d50707ba77d19728` |
| `spx-sdk` | `v1.0.0` | `1d7bb611af077cfdd4fabefa6e782a8a7cb3253b` |
| `spx-python` | `v1.0.0-rc.3` | `08e9bab29505b5e3fc6c35b068768cb6a99fdfa5` |
| `spx-examples` | `catalog-2026.11.05.1` | `f1b454568614f829bc71899f898c7036c61692ca` |
<!-- release-bundle:end -->

The machine-readable manifest is [sources.json](sources.json) in `spx-docs`.
It is the source for this generated table, tutorial package pins and the
website's reviewed release snapshot. SDK **1.0.0** is the server's locked dependency;
Python HTTP client **1.0.0rc3** is intentionally retained by the installer.
Do not substitute other package versions merely to match the product name.
The public device
catalog may advance independently through a reviewed catalog-sync PR; it does
not silently update this runtime baseline or the installer's context pin.

## Upgrade

Open the [SPX Downloads portal](https://www.simplephysx.com/downloads) and select
**Stable**, then choose installer **1.1.0** for your operating system.
During the website migration, use the working
[staging Downloads portal](https://staging.simplephysx.com/downloads) with the same
**Stable** selection. Development contains pre-release builds and is optional.
Record its version and the generated server/UI image tags. Use the supported
pair selected by the installer; do not substitute a newer alpha image because
its tag sorts later. Validate your MiL suite and any protocol integration you use
before adopting the new bundle. Export important snapshots before an upgrade.

### Upgrading from the documented RC baseline

The previous documentation baseline was installer **1.1.0-rc.115**,
Server/UI **1.0.0-rc.76**, SDK **1.0.0rc21** and Examples `be71a161`.
Use the complete stable installer to move to the table above. Its catalog is
the reviewed `catalog-2026.11.05.1` release, pinned at `f1b45456`.
The stable server adds model-defined SCPI status/error handling and binary-safe
KNX API serialization relative to that baseline. Test your own command dialect
and bindings when upgrading.

Save a disk snapshot or export configuration before replacing an existing stack.
Restore reconstructs configuration and model defaults; it does not resume live
measurements or chart history. Restart the restored instances and connections,
then reapply experiment inputs. Verify `/health`, the UI's managed connection,
and the [31.25°C first-device result](getting-started/README.md) before continuing.

Server, SDK and installer source repositories are private. Public Examples is
for models and runtime MCP modules; its fresh history does not retain the
installer's historical releases. Product packages are delivered through the
protected Downloads portal and its file-delivery host.
