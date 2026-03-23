# Project Workflow Overview

This starter project separates the application into a few simple layers:

- `main.py`
  Starts the FastAPI app and includes the API router.
- `api/routes/`
  Holds the HTTP endpoints.
- `services/`
  Holds the business logic used by the routes.
- `models/`
  Holds the SQLAlchemy ORM models.
- `schemas/`
  Holds the Pydantic request and response shapes used by FastAPI validation.
- `db/`
  Holds the SQLAlchemy base, engine, and session setup.
- `alembic/`
  Holds the database migration configuration and revision files.

## Request Workflow

1. A client sends an HTTP request to the FastAPI app.
2. The route in `api/routes/` receives the request.
3. FastAPI parses the request body into a Pydantic schema from `schemas/`.
4. Pydantic validates the body before the route logic runs.
5. If validation fails, FastAPI returns `422 Unprocessable Entity`.
6. If validation succeeds, the route gets a database session from `db/session.py`.
7. The route calls a function in `services/`.
8. The service uses a model from `models/` with SQLAlchemy.
9. SQLAlchemy runs the database query against PostgreSQL.
10. The service returns the result to the route.
11. The route returns the response to the client.

## Database Change Workflow

1. Add a new model or update an existing model in `models/`.
2. Make sure the model is imported into `models/__init__.py` if needed for metadata discovery.
3. Generate a migration:

   ```bash
   alembic revision --autogenerate -m "describe the change"
   ```

4. Review the generated migration in `alembic/versions/`.
5. Apply the migration:

   ```bash
   alembic upgrade head
   ```

6. Run the API again and use the updated schema.

## Database URL Notes

1. The app reads `DATABASE_URL` from `.env` through `core/config.py`.
2. If the URL starts with `postgresql://`, the code normalizes it to `postgresql+psycopg://`.
3. This lets SQLAlchemy and Alembic use the installed `psycopg` v3 driver.
4. `alembic/env.py` overrides `sqlalchemy.url` from `alembic.ini` when `DATABASE_URL` is present.

## Current Sample Flow

1. `POST /api/tests` is called.
2. `api/routes/test.py` receives the request.
3. `TestCreate` in `schemas/test.py` validates the incoming body.
4. `name` is trimmed and must be non-blank, at least 3 characters, and at most 100 characters.
5. `services/test_service.py` creates a `TestRecord`.
6. `models/test.py` maps that object to the `tests` table.
7. SQLAlchemy commits the insert into PostgreSQL.
8. FastAPI returns the inserted record as JSON using `TestResponse`.
