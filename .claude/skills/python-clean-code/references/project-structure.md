# Project structure (src layout)

Use a **src layout**: importable code lives under `src/`, never at the repo root.
This forces you to test the installed package (not the working-copy files) and
keeps imports honest.

```
<repo>/
├── src/
│   └── <package>/
│       ├── __init__.py
│       ├── py.typed            # ship type information
│       ├── main.py             # the single entry point: def main()
│       ├── config.py           # central typed config (frozen pydantic BaseModel)
│       ├── <domain modules>.py
│       └── errors.py           # custom domain exceptions
├── tests/
│   ├── conftest.py             # shared fixtures
│   ├── unit/
│   ├── integration/
│   └── end2end/
├── pyproject.toml              # build + tool config (see pyproject-tooling.toml)
├── pixi.toml                   # environment + deps (see pixi.toml)
└── README.md
```

## Conventions

- **`py.typed`** in the package so downstream consumers get your types; declare
  it as package data in `pyproject.toml`.
- **One `main()`** wired in `[project.scripts]` (e.g. `app = "<package>.main:main"`).
- **No module-level side effects** anywhere under `src/`.
- **Version** from `setuptools-scm` into `src/<package>/_version.py` (don't hand-edit).
- **Test tiers** map to the pixi `ptu` / `pti` / `pte` tasks.
