---
name: docker-patterns
description: Use when writing or changing a Dockerfile, docker-compose, or container image build — choosing a base image, ordering layers, handling secrets/build args, setting the run user, or shrinking image size. Symptoms: image is huge or slow to build, secret or .env baked into a layer, container runs as root, unpinned :latest base, cache busts on every build, no healthcheck, dev and prod images diverge.
---

# Docker Patterns

## Overview

A container that "works on my machine" can still be bloated, insecure, or unreproducible. The failure mode isn't not knowing Docker — it's skipping the boring checks: pinning the base, keeping secrets out of layers, not running as root, ordering layers for cache. Each is cheap now and expensive after it ships.

Core principle: **small, reproducible, least-privilege images; secrets never in a layer.**

For app-level auth/injection use `web-security`; for release/rollout use `deployment-patterns`. This skill is the *image*.

## The checklist

**Pin the base.** `FROM node:22.3-slim`, not `node:latest`. `latest` makes builds non-reproducible and silently changes under you. Prefer `-slim`/`-alpine`/distroless for a smaller surface.

**Order layers cache-first.** Put things that change rarely (deps) before things that change often (source). Copy the lockfile + install deps, *then* copy source — so a code edit doesn't reinstall every dependency.

**Multi-stage build.** Build/compile in a fat stage; copy only the artifact into a slim runtime stage. Toolchains, dev deps, and build caches never reach the final image.

**Secrets never in a layer.** `COPY .env`, `ARG SECRET=`, or `RUN export TOKEN=...` bake into image history — recoverable by anyone with the image. Use `--secret` mounts (BuildKit) at build time, and real env/secret injection at *run* time. `.dockerignore` the `.env`.

**Run as non-root.** Default is root; a container escape then owns more. Create a user and `USER app`. Distroless/`nonroot` variants do this for you.

**`.dockerignore` is required.** Exclude `.git`, `node_modules`, `.env`, build output. Keeps the build context small and secrets/junk out of the image.

**One concern per container.** One process, not an init-system running app+db+cron. Compose separate services instead.

**Healthcheck + explicit stop.** Add a `HEALTHCHECK` so the orchestrator knows readiness. Ensure the app handles `SIGTERM` for graceful shutdown (PID 1 signal handling — use an init like `tini` or exec-form `CMD`).

**Exec-form CMD/ENTRYPOINT.** `CMD ["node","server.js"]`, not `CMD node server.js`. Shell form wraps in `/bin/sh -c` and swallows signals.

## Common mistakes

- **`COPY . .` before `npm install`.** Every source edit busts the dep cache → full reinstall each build. Copy manifest first.
- **`:latest` everywhere.** Reproducible builds are impossible; a rebuild months later pulls a different base. Pin.
- **Secrets via `ARG`.** Build args are visible in `docker history` and image metadata. Not secret.
- **Installing dev tooling in the runtime image.** Compilers, `curl`, package caches inflate size and attack surface. Multi-stage, then drop them.
- **`apt-get install` without cleanup in the same layer.** Left-over apt lists bloat the layer. Clean in the same `RUN`.
- **Running as root "because it's easier".** One privilege-escalation bug and root in the container is a bigger problem. Add a user.

## When NOT to over-do it

- **No multi-stage for an interpreted app with no build step** — if there's nothing to compile, a single slim stage is fine. (YAGNI)
- **No custom base image** to shave a few MB when an official slim tag is close enough. Maintenance cost outweighs it.
- **Compose is not Kubernetes.** For local dev, don't reach for a full orchestrator; compose covers it.
