---
name: python-clean-code
description: >-
  Opinionated Python conventions — strict typing, pydantic/dataclass data
  modeling, StrEnum, functions-first, dependency injection, custom errors,
  fail-fast, central typed config, ruff + mypy-strict + pytest + pixi tooling,
  and a src-layout project structure. Use whenever writing or editing ANY
  Python: modules, functions, classes, tests, config, or project setup.
---

# Python clean code

Opinionated defaults for writing Python. Apply them by default; deviate only
with a stated reason. Minimum floor: **Python 3.11** (`StrEnum`); write examples
against current Python.

The copy-paste tooling and layout templates live in [`references/`](references/).

## Typing

- Type everything. Code runs under `mypy --strict`; untyped is broken.
- Ban `typing.Any`. If you need an escape hatch at a genuine boundary, use
  `object` + narrowing, a `Protocol`, or a `TypeVar` — not `Any`.
- Prefer precise types: `Sequence`/`Mapping` for read-only inputs, concrete
  `list`/`dict` for owned data, `Literal`/`StrEnum` for closed sets.

## Data modeling

- Model data with **pydantic models** or **dataclasses** — never ad-hoc dicts or
  tuples for structured data.
- **Boundary vs. internal**: if a value is parsed or serialized (API payloads,
  config, external data) → **pydantic** (validation + serialization). If it is
  internal, already-trusted data just carried around → **frozen dataclass**
  (zero runtime cost, no dependency).
- **Data carriers are frozen by default.** Make them mutable only with a reason.

```python
# ✅ boundary: validated + serialized
class CreateUser(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: str
    role: Role

# ✅ internal trusted value
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# ❌ structured data as a dict
user = {"email": "a@b.c", "role": "admin"}
```

- **`StrEnum` for any closed, known set of string values** (states, kinds,
  modes, roles). `Literal[...]` is fine for a fixed set used only in type
  positions with no runtime membership/iteration. Never force an enum on
  open-ended strings (IDs, tags, free text).

```python
# ✅
class Role(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"

# ❌ bare strings for a closed set
def grant(role: str) -> None: ...
```

## Functions and classes

- **Functions first**: small, pure, single-purpose. Prefer immutable locals
  (don't reassign; don't mutate arguments).
- **Use a class only when you need one.** "Need one" = behavior/stateful
  objects. Data carriers (pydantic/dataclass/enum) and DI seams
  (`Protocol`/ABC) are always fine — they are not what "classes only if needed"
  restricts.
- **Composition over inheritance.** Inherit only for genuine subtyping; compose
  (and depend on `Protocol`s) otherwise.
- **Dependency injection over global state.** Pass collaborators in as
  arguments. No module-level singletons, no hidden globals.

```python
# ✅ inject the collaborator
def fetch_user(user_id: str, store: UserStore) -> User: ...

# ❌ reach for a global
def fetch_user(user_id: str) -> User:
    return GLOBAL_STORE.get(user_id)
```

## Comprehensions

- Use list/dict/set comprehensions instead of building collections with a `for`
  loop + `.append`/assignment. Reach for a `for` loop only when the comprehension
  hurts readability (multiple clauses, side effects, complex branching).

```python
# ✅
names = [user.name for user in users if user.is_active]

# ❌
names = []
for user in users:
    if user.is_active:
        names.append(user.name)
```

## Errors and failure

- **Define custom error types for your domain.** One base exception per domain
  (e.g. `class MyApiError(Exception): ...`), with specific subclasses. Callers
  catch the base broadly or a subclass narrowly.
- **Fail fast, no silent fallbacks:**
  - No bare `except:`.
  - No `except SomeError: pass` (swallowing).
  - No returning `None`/sentinel/default to hide a failure.
  - Raise at the first invalid state.
- **Validate up front.** Check inputs and preconditions at the top of the
  function / edge of the program, then proceed assuming validity.

```python
# ✅ validate up front, raise
def withdraw(account: Account, amount: Decimal) -> Account:
    if amount <= 0:
        raise InvalidAmountError(amount)
    if amount > account.balance:
        raise InsufficientFundsError(account.id, amount)
    return account.debit(amount)

# ❌ silent fallback
def withdraw(account, amount):
    try:
        return account.debit(amount)
    except Exception:
        return account  # swallows the failure
```

## Configuration

- **One central, typed config.** A plain pydantic `BaseModel` (frozen).
- **Load once, at the top.** Read raw values from the source(s) (env / CLI /
  file) inside `main()`, construct the model (validation happens by
  construction), then **inject it downward** as an argument.
- **No global config singleton.** Config is passed in, not imported.

```python
# ✅ built once in main(), injected
def main() -> None:
    config = AppConfig(**load_raw_config())  # validates here
    run(config)

# ❌ module-level global
CONFIG = AppConfig(**os.environ)  # import-time side effect + global state
```

## Entry points

- **One `main()` per program.** The only entry point.
- **No module-level side effects.** Importing a module must not run work, open
  files, read env, or configure logging. All of that happens inside `main()`.

## Logging

- Use `loguru` for logging.
- **Log and raise, never log and swallow.** Logging an error is not handling it;
  if you can't recover, let it propagate.

## Filesystem

- Use `pathlib.Path`, never `os.path` string munging.

## Docstrings and comments

- **Google-style docstrings.**
- Skip docstrings for self-evident private helpers — a good name and types beat
  a redundant sentence. Document public API, non-obvious behavior, and anything
  surprising.
- **Comment the *why*, not the *what*.** The code says what; comments explain
  intent, trade-offs, and context.

## Naming

- `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE`
  constants.
- Full words over abbreviations.
- Booleans read as predicates: `is_ready`, `has_items`.
- Prefix intentionally-unused names with `_`.
- Use standard verb prefixes consistently:
  - `get_` — retrieve, no side effects
  - `build_` / `make_` — construct something new
  - `to_` / `from_` — convert between representations
  - `is_` / `has_` — boolean predicates
  - `load_` / `save_` — I/O (read from / write to a store)

## Testing

- `pytest`. Mirror the `tests/{unit,integration,end2end}` tiering.
- **Mocking is a design smell.** If you reach for `monkeypatch` or
  `unittest.mock.patch`, the code under test probably needs a DI seam: inject a
  real object or a hand-written fake/stub instead. Use patching only as a last
  resort when there is genuinely no seam (e.g. patching a third-party global you
  don't control).
- Put shared fixtures in `conftest.py`.

```python
# ✅ inject a fake through the seam
class FakeUserStore:
    def get(self, user_id: str) -> User: ...

def test_fetch_user() -> None:
    user = fetch_user("u1", FakeUserStore())
    ...

# ❌ patch internals
def test_fetch_user(monkeypatch):
    monkeypatch.setattr(service, "GLOBAL_STORE", ...)
```

## Tooling

- **ruff** for linting and formatting (`ruff check` + `ruff format`).
- **mypy** in `strict` mode.
- **pytest** for tests.
- **pixi** for environments and dependency management.
- Pre-merge gate: `ruff format --check . && ruff check . && mypy && pytest`.

Copy the configs from [`references/`](references/):

- [`pyproject-tooling.toml`](references/pyproject-tooling.toml) — ruff (curated
  rule select + google pydocstyle) and mypy-strict blocks.
- [`pixi.toml`](references/pixi.toml) — environment / dependency skeleton.

## Project structure

Source layout, documented in
[`project-structure.md`](references/project-structure.md):

```
src/<package>/        # importable code, with py.typed
tests/{unit,integration,end2end}/
pyproject.toml
pixi.toml
```
