# CLAUDE.md

## toolchain

- **uv** for everything -- deps, venv, running scripts. never use pip directly.
- `uv run` to execute. `uv add` to install. `uv sync` to install from lockfile.
- python 3.13+

## project structure

```
app/
  main.py          # FastAPI app instance, top-level routes
  routers/         # one file per domain (users.py, items.py, etc)
  models.py        # pydantic models
  deps.py          # shared dependencies (db session, auth, etc)
  config.py        # settings via pydantic-settings
tests/
  test_*.py
pyproject.toml
.env
```

## stack

- **FastAPI** -- framework
- **Pydantic v2** -- validation and schemas. always use model_validator and field_validator, not __init__
- **pydantic-settings** -- config/env. one Settings class in config.py, imported everywhere
- **uvicorn** -- dev server (`uv run uvicorn app.main:app --reload`)
- **pytest + httpx** -- testing. use AsyncClient, not TestClient
- **Ruff** -- lint and format. run before committing.

## conventions

- async everywhere. no sync route handlers unless there's a hard reason
- type everything. no untyped function signatures
- pydantic models for all request bodies and response shapes. no raw dicts crossing the API boundary
- routers use `APIRouter` with a prefix and tags. never define routes directly on `app` except health check
- deps.py for anything injected via `Depends()` -- don't inline dependency logic in route handlers
- errors: raise `HTTPException` with explicit status codes. don't let unhandled exceptions bubble
- env: nothing hardcoded. all config through `.env` + pydantic-settings

## what not to do

- no `print()` -- use `logging`
- no sync `requests` library -- use `httpx` with async client
- no global mutable state
- no `Any` type unless absolutely unavoidable and commented
- don't put business logic in route handlers -- handlers receive, delegate, return
