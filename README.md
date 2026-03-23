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

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirement.txt
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
