# Cody API

FastAPI backend for a Discord bot project.

## Requirements

- Python 3.10+
- `pip`
- PostgreSQL

## Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

For Linux:
```bash
source venv/bin/activate
```

For Windows:
```bash
venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Run the FastAPI development server:

```bash
fastapi dev main.py
```

Run the database migration:

```bash
alembic upgrade head
```

## PostgreSQL

This project is planned to use PostgreSQL as its database.

Make sure PostgreSQL is installed and running on your machine, then create a database for this project. A typical connection format looks like this:

```text
postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

Example:

```text
postgresql://postgres:password@localhost:5432/cody_api
```

You can place this value in your `.env` file as `DATABASE_URL`.

## Environment Variables

This project includes an example environment file at [.env.example].

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/cody_api
INTERNAL_API_KEY=change-this-secret-key
```

## Database Workflow

The project is already set up for SQLAlchemy and Alembic.

Recommended for local development: each developer should use their own local database or a separate dev database. Sharing one database while multiple people experiment with migrations makes it easy for the database state and local migration files to drift apart.

Apply the current migration:

```bash
alembic upgrade head
```

Create a new migration after changing your SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply that new migration:

```bash
alembic upgrade head
```

## Alembic Mismatch Recovery

If Alembic shows an error like `Can't locate revision identified by '...'`, the database is pointing at a revision that does not exist in your local `alembic/versions/` folder.

Common causes:

- Someone applied an old migration to the shared database and that migration file was later deleted or renamed.
- A teammate did not pull the same migration files before running `alembic upgrade head`.
- Multiple developers are using the same database for local experiments.

Safe recovery options:

- Best option: restore the missing migration file into `alembic/versions/` and commit it.
- If the database is disposable dev data, recreate/reset the database and run `alembic upgrade head`.
- If the schema already matches the current repo and you only need Alembic to catch up, use `alembic stamp <revision>` carefully.

Example for this repo's current revision:

```bash
alembic stamp 20260323_000001
```

Use `stamp` only when you are sure the schema already matches the current migration, because it updates Alembic's version tracking without running SQL changes.

The initial model in this project is a simple `tests` table with:

- `id`
- `name`

There is also a sample insert endpoint:

```http
POST /api/tests
Content-Type: application/json

{
  "name": "example"
}
```

## Current App

The current FastAPI app lives in [main.py](/home/fy-hr/Documents/akshara-dev/cody-api/main.py) and exposes a basic root route plus a sample `POST /api/tests` insert endpoint.
