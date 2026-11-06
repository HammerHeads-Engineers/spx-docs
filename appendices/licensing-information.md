# Licensing Information

SPX Server typically requires a product key to run authenticated operations. In this documentation and the reference repos it is always treated as a secret:

- Environment variable: `SPX_PRODUCT_KEY`
- Local dev: store it in a `.env` file consumed by `docker compose` and your test runner.
- CI: store it as a secret and inject it into the job environment.

## Safe handling rules

- Do not commit product keys to git.
- Treat personalized Docker Compose files (that embed keys) as secrets.
- Prefer passing keys via environment variables rather than hard-coding them into YAML.

## Where to get a key

Sign in to the [SPX portal](https://www.simplephysx.com/sign-in), select the
workspace with product access, and open **Product Keys**. A workspace owner or
admin can reveal/copy the key for its assigned license slot. Members should ask
an owner/admin to provide their assigned key securely.

During the website migration, use the [staging portal](https://staging.simplephysx.com/account/product-keys).
The [Installation Guide](../getting-started/installation-guide.md) explains how
to select the stable installer and configure its managed connection.

## Plans and installation targets

- **Community:** one license slot, up to five instances, non-commercial
  evaluation, valid for twelve months; no card required.
- **Team:** commercial license slots assigned to a person, workstation or CI
  installation. Each assigned slot has its own Product Key. Workspace membership
  alone does not assign a paid license slot.
- **Enterprise:** individually agreed commercial terms using the Team model.

Use **Billing** to review entitlements and **Seats** to manage their targets.
If no key is available, check the selected workspace and active entitlement.
For rejected or expired access, ask the workspace owner/admin to review its
license status before rerunning Setup. See the [current plans](https://www.simplephysx.com/pricing)
and [support guidance](../troubleshooting-and-support/how-to-get-support.md).

Community installations can send limited technical license telemetry, associated
with the assigned account by server-side license records. This does not send
model configuration or live values and is optional to server startup. Review the
[Privacy Policy](https://www.simplephysx.com/privacy) for scope and retention;
during migration use the [staging policy](https://staging.simplephysx.com/privacy).
