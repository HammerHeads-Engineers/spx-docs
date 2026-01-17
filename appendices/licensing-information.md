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

Log in to `https://simplephysx.com` and retrieve your product key from your account/subscription area.
