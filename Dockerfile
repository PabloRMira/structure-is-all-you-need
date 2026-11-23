# syntax=docker/dockerfile:1

# ---- Build stage -----------------------------------------------------------
# Resolve and install the *production* pixi environment (no dev/test tooling).
FROM ghcr.io/prefix-dev/pixi:latest AS build

WORKDIR /app

# `myapi` is installed editable, and its version is derived by setuptools-scm,
# which shells out to the `git` binary at build time. The pixi base image ships
# without git, so install it here (kept in its own layer for caching).
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Copy the whole project. `.git` is intentionally kept (see .dockerignore) so
# setuptools-scm can derive the package version during the editable install.
COPY . .

# `.git` was copied in as root-owned; mark it safe so git doesn't refuse to run
# with a "dubious ownership" error during the setuptools-scm version lookup.
RUN git config --global --add safe.directory /app

# Install exactly what the lockfile pins for the production environment.
RUN pixi install --locked -e myapi-prod

# Emit an activation script so the environment works at runtime without pixi.
RUN pixi shell-hook -e myapi-prod -s bash > /shell-hook.sh && \
    echo 'exec "$@"' >> /shell-hook.sh

# ---- Runtime stage ---------------------------------------------------------
# Minimal image carrying just the solved environment + application source.
FROM debian:bookworm-slim AS runtime

WORKDIR /app

# The production environment (Python interpreter + runtime dependencies).
COPY --from=build /app/.pixi/envs/myapi-prod /app/.pixi/envs/myapi-prod
# The source tree: the package is installed editable, so it points back here.
COPY --from=build /app/src /app/src
COPY --from=build /app/pyproject.toml /app/pixi.toml /app/README.md ./
# Activation entrypoint produced in the build stage.
COPY --from=build /shell-hook.sh /shell-hook.sh

# A default config so the image runs out of the box. Override it by mounting
# your own file at /app/config.json (or pass another path as the CMD argument).
COPY --from=build /app/docs/examples/config.example.json /app/config.json

EXPOSE 8000

# `/shell-hook.sh` activates the env and then `exec "$@"` runs the CMD.
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["myapi", "/app/config.json"]
