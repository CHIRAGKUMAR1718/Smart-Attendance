# SMAT Attendance

Express + Postgres + Redis backend for starting attendance sessions and letting students check in.

## Setup

1. Install dependencies

```bash
npm install
```

2. Configure environment variables

Create a `.env` file in the project root:

- `PORT` (default 3000)
- `JWT_SECRET` (required)
- `REDIS_URL` (required)
- `DB_URL` (required)

3. Create database schema

Run the SQL in `src/db/schema.sql` on your Postgres database.

> Note: the schema uses `gen_random_uuid()` so you may need:
> `CREATE EXTENSION IF NOT EXISTS pgcrypto;`

## Run

```bash
npm run start
```

## Run with Docker (recommended)

This repo includes `docker-compose.yml` that starts:
- Postgres on `localhost:5432`
- Redis on `localhost:6379`
- API on `localhost:3000`

Start everything:

```bash
docker compose up --build
```

Stop everything:

```bash
docker compose down
```

## API

- `POST /auth/register` { email, password, role? }
- `POST /auth/login` { email, password }
- `POST /sessions/start` (auth) { classId, duration }
- `POST /attendance/mark` (auth) { sessionId }
- `GET /attendance/list` (auth) ?limit=&offset=
- `GET /attendance/session/:sessionId` (auth) ?limit=
