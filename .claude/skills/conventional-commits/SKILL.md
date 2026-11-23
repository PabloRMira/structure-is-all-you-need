---
name: conventional-commits
description: >-
  Write git commit messages that follow the Conventional Commits 1.0.0
  specification — a structured `type(scope): description` subject, an optional
  body, and footers including `BREAKING CHANGE:`. Use whenever writing a commit
  message, amending one, crafting a PR title, or setting up commitlint/release
  tooling that depends on this format.
---

# Conventional Commits

A commit message convention that makes history machine-readable: it drives
automated changelogs, semantic version bumps, and clear intent. Follow it for
every commit unless the repo documents a different convention.

## Structure

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

- A blank line separates subject from body, and body from footers.
- The subject line is the only required part.

## Subject line

- **type**: a required, lowercase word from the list below.
- **scope**: optional, in parentheses — the area touched, e.g. `feat(parser):`.
  Use a consistent noun (a module, package, or domain), lowercase.
- **description**: a short summary in the **imperative mood** ("add", not
  "added"/"adds"), lowercase start, no trailing period.
- Keep the whole subject line **≤ 72 characters** (aim for ~50).

Good: `fix(auth): handle expired refresh tokens`
Bad: `Fixed the bug.` / `feat: Added new feature.`

## Types

- **feat** — a new feature (triggers a MINOR version bump).
- **fix** — a bug fix (triggers a PATCH version bump).
- **docs** — documentation only.
- **style** — formatting, whitespace, no code-behavior change.
- **refactor** — code change that neither fixes a bug nor adds a feature.
- **perf** — a performance improvement.
- **test** — adding or correcting tests.
- **build** — build system or external dependencies (e.g. pip, docker, npm).
- **ci** — CI configuration and scripts (e.g. GitHub Actions).
- **chore** — maintenance that doesn't touch src or tests.
- **revert** — reverts a previous commit.

## Body

- Optional. Explain **what** and **why**, not how. Wrap at ~72 columns.
- Use it whenever the subject alone doesn't justify the change.
- May span multiple paragraphs separated by blank lines.

## Footers

- Format: `Token: value` (or `Token #value`). Tokens use `-` instead of spaces,
  except `BREAKING CHANGE`.
- Reference issues: `Refs: #123`, `Closes: #456`.
- Co-authors: `Co-Authored-By: Name <email>`.

## Breaking changes

Signal an incompatible API change (triggers a MAJOR version bump) in **either**
way — or both:

1. Append `!` after type/scope: `feat(api)!: drop support for Node 18`
2. Add a footer: `BREAKING CHANGE: <explanation of what broke and migration>`

If `!` is used, the `BREAKING CHANGE:` footer is recommended but not required.

## Examples

```
feat(lang): add Polish translation
```

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
responses other than from the latest request.

Refs: #123
```

```
refactor(auth)!: replace session cookies with JWT

BREAKING CHANGE: clients must now send a Bearer token; session
cookies are no longer honored.
```

## Checklist before committing

1. Type is valid and lowercase.
2. Description is imperative, lowercase, no period, ≤ 72 chars.
3. Body explains why, if the change isn't self-evident.
4. Breaking changes are flagged with `!` and/or `BREAKING CHANGE:`.
5. Issues referenced in footers, not in the subject.
