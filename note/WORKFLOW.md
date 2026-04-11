# Project Workflow Overview

This project splits the app into layers. See [README.md](../README.md) for setup and examples. This file describes how requests and schema changes move through the code.

## Layers

| Area | Role |
|------|------|
| `main.py` | Creates the FastAPI app and mounts `api_router` under `/api`. |
| `api/router.py` | Composes route modules (`/tests`, `/user`, …). |
| `api/routes/` | HTTP handlers: parse inputs, call services, return responses. |
| `api/deps.py` | Shared `Depends(...)` callables (for example internal API key check). |
| `core/config.py` | Environment-backed settings (`DATABASE_URL`, `INTERNAL_API_KEY`). |
| `services/` | Business logic and transactions; used by routes, not tied to HTTP details. |
| `models/` | SQLAlchemy ORM models and `models/__init__.py` for metadata registration. |
| `schemas/` | Pydantic request/response models for validation and OpenAPI. |
| `db/` | `Base`, engine, `SessionLocal`, and `get_db` generator. |
| `alembic/` | Migration config and revision files. |

## Request workflow (general)

1. The client sends an HTTP request to the FastAPI app.
2. For protected routes, FastAPI runs dependencies first (for example `verify_internal_api_key` reads `X-Internal-Api-Key` and compares it to `settings.internal_api_key`). Failure yields `401` or a configured error before the route body runs.
3. The route handler receives the request. FastAPI parses the body into a Pydantic model from `schemas/` when declared.
4. If validation fails, FastAPI returns `422 Unprocessable Entity` with field errors.
5. If validation succeeds, the route obtains a DB session via `Depends(get_db)`.
6. The route calls a function in `services/`.
7. The service uses SQLAlchemy models from `models/` and the injected session.
8. SQLAlchemy executes SQL against PostgreSQL.
9. The service returns a value (ORM instance, plain data, or message) to the route.
10. FastAPI serializes the response (optionally through a `response_model`).

**Design note:** Keep header checks and HTTP-specific logic in dependencies or routes. Services stay focused on domain rules and persistence so they are easier to test and reuse.

## Database change workflow

1. Add or change a model in `models/`.
2. Ensure the model is imported in `models/__init__.py` so Alembic autogenerate sees it (`alembic/env.py` does `import models`).
3. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "describe the change"
   ```

4. Inspect the new file in `alembic/versions/` (autogenerate is not perfect).
5. Apply:

   ```bash
   alembic upgrade head
   ```

6. Run the API and exercise endpoints against the updated schema.

## Environment and database URL

1. `DATABASE_URL` and `INTERNAL_API_KEY` are read from `.env` through `core/config.py`.
2. URLs starting with `postgresql://` are normalized to `postgresql+psycopg://` for SQLAlchemy.
3. `alembic/env.py` sets Alembic’s SQLAlchemy URL from the same settings when present, overriding the placeholder in `alembic.ini`.

## Sample flow: `POST /api/tests` (scaffold, no API key)

1. Client calls `POST /api/tests` with JSON `{"name": "..."}`.
2. `api/routes/test.py` receives the request.
3. `TestCreate` in `schemas/test.py` validates the body (trimmed name, length rules).
4. `services/test_service.py` builds a `TestRecord` and commits.
5. `models/test.py` maps the object to the `tests` table.
6. FastAPI returns JSON shaped like `TestResponse`.

## Sample flow: `POST /api/user/register` (authenticated)

1. Client sends `POST /api/user/register` with header `X-Internal-Api-Key: <same value as INTERNAL_API_KEY in .env>` and JSON `{"discord_user_id": "..."}` (17–21 digit snowflake string per schema).
2. `verify_internal_api_key` in `api/deps.py` runs via `Depends`; invalid or missing key stops the request early.
3. `api/routes/user.py` validates the body with `UserCreate`.
4. `services/user_service.create_user` inserts a `User` row and handles conflicts (for example duplicate Discord id).
5. FastAPI returns `UserResponse` (id, ids, timestamps).

## Sample flow: `DELETE /api/user/delete` (authenticated)

1. Same header requirement as register.
2. Body validated as `UserDelete` (Discord user id).
3. `delete_user` in `services/user_service.py` loads the user, deletes, commits; business rules map “not found” and errors to the appropriate HTTP status.

Use header `X-Internal-Api-Key` with the same value as `INTERNAL_API_KEY` in `.env`. Copy-paste-friendly examples are easiest to maintain in [README.md](../README.md).
