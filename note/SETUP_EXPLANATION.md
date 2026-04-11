# Setup Explanation

SQLAlchemy, Alembic, and Pydantic have different jobs in this project. For install commands, env vars, and HTTP examples, see the repository [README.md](../README.md). This note explains how the pieces fit together.

## Why `__init__.py` Exists in Some Folders

- `__init__.py` marks a directory as a Python package so imports like `from services.user_service import create_user` resolve reliably.
- In this repo, `models/__init__.py` imports every model so one `import models` registers all tables on SQLAlchemy metadata (used by Alembic in `alembic/env.py`).
- `schemas/__init__.py` re-exports schema classes for a tidy import surface.
- Newer Python can use namespace packages without `__init__.py` in every folder; keeping these files makes the structure explicit as the codebase grows.

## Configuration (`core/config.py`)

- Loads `.env` via `python-dotenv`.
- Exposes `settings.database_url` and `settings.internal_api_key`.
- Normalizes `postgresql://` to `postgresql+psycopg://` so SQLAlchemy uses the installed **psycopg** v3 driver.
- Routes that need bot authentication read the expected key from `settings.internal_api_key` (see `api/deps.py`).

## SQLAlchemy

- ORM and database toolkit for the running FastAPI app.
- Models live under `models/` (for example `User`, `TestRecord`, `Project`).
- `db/base.py` defines the declarative `Base`; `db/session.py` creates the engine and session factory.
- Routes obtain a session with `Depends(get_db)`; services perform commits and queries using that session.

## Pydantic

- Request and response shapes live under `schemas/`.
- Examples: `TestCreate` / `TestResponse` for `POST /api/tests`; `UserCreate` / `UserResponse` / `UserDelete` for user routes.
- FastAPI validates JSON against these models before your route body runs; invalid input becomes `422 Unprocessable Entity`.
- `model_config = ConfigDict(from_attributes=True)` on response models lets FastAPI serialize SQLAlchemy instances.

## Alembic

- Tracks and applies **schema** changes (create/alter/drop tables) over time.
- Revision scripts are in `alembic/versions/`.
- `alembic/env.py` sets `target_metadata = Base.metadata` and imports `models` so autogenerate sees every table.
- `alembic.ini` points Alembic at the `alembic/` folder and baseline config; the live DB URL still comes from `DATABASE_URL` via `env.py`.
- The `alembic/` tree is usually created once with `alembic init alembic`, then customized (especially `env.py`).

## Database URL Note

- This project uses **psycopg** v3 (`psycopg[binary]`), not `psycopg2`.
- `.env.example` may show `postgresql+psycopg://` explicitly; plain `postgresql://` in `.env` is fine because `core/config.py` normalizes it.
- A Railway hostname ending in `.railway.internal` is private to Railway’s network and usually will not work from a local machine unless you are on that network.

## Why SQLAlchemy, Alembic, and Pydantic Together

- **SQLAlchemy** — how the app reads and writes rows at runtime.
- **Alembic** — how the real PostgreSQL schema stays in sync with the models across environments.
- **Pydantic** — how HTTP JSON is validated and documented at the API boundary.

## Typical Workflow

1. Change or add a model in `models/` and export it from `models/__init__.py` if it is new.
2. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "message"
   ```

3. Review the file under `alembic/versions/`, then apply:

   ```bash
   alembic upgrade head
   ```

4. Add or update `schemas/` when the public API shape changes.
5. Implement route + service logic; restart the dev server after `.env` changes.

## Team and migration hygiene

- Commit everything under `alembic/versions/` so everyone shares the same history.
- The database records the applied revision in `alembic_version`.
- Prefer **per-developer** or **per-branch** databases for migration experiments to avoid revision mismatch.
- If you see `Can't locate revision identified by '...'`, your DB points at a revision missing from your clone. Recover by restoring the file, resetting a disposable DB, or (only when schema already matches) `alembic stamp <revision>`. Use `alembic heads` on a clean checkout to see the current head id.

## Further reading

- [README.md](../README.md) — setup, environment variables, and API usage.
