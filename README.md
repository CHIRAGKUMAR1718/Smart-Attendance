
# SMAT Attendance

Express + Postgres + Redis backend for starting attendance sessions and letting students check in.

## Setup

1. Install dependencies

```bash
npm install
```

2. Configure environment variables

Create a `.env` file in the project root (see **`.env.example`**):

- `PORT` (default 3000)
- `JWT_SECRET` (required)
- `REDIS_URL` (required)
- `DB_URL` (required) — on Vercel, Neon integration may set `POSTGRES_URL` / `DATABASE_URL` instead (supported automatically)

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
- `POST /sessions/start` (auth) { classId, duration, chirpMinFreq?, chirpMaxFreq? }
- `POST /attendance/mark` (auth) { sessionId }
- `POST /attendance/mark-by-signal` (auth) { frequency }
- `GET /attendance/list` (auth) ?limit=&offset=
- `GET /attendance/session/:sessionId` (auth) ?limit=

## Deploy on Vercel (HTTPS for phones — recommended)

This app runs as one **serverless Express** function (`api/index.js`) with `public/**` bundled.

**Full checklist (Neon + Upstash + env vars + SQL):** see **[`DEPLOY_VERCEL.md`](./DEPLOY_VERCEL.md)**.

Quick summary:

1. Connect **[Neon from Vercel Marketplace](https://vercel.com/marketplace/neon)** *or* set **`DB_URL`** manually. The app also reads **`POSTGRES_URL`**, **`DATABASE_URL`**, **`POSTGRES_PRISMA_URL`**.
2. Add **`REDIS_URL`** from [Upstash](https://upstash.com) (`rediss://…`) *or* **`UPSTASH_REDIS_URL`** if your integration sets that.
3. Set **`JWT_SECRET`** (e.g. `openssl rand -hex 32`).
4. Run **`src/db/schema.sql`** in Neon’s SQL editor once (`pgcrypto` extension if needed).
5. Deploy from GitHub; use **`/teacher.html`** and **`/student.html`** on your `*.vercel.app` URL.

Optional local prod-like run: `npx vercel dev` (after `vercel link`).

### Notes

- **Cold starts:** first request after idle can be slower; normal for serverless.
- **Redis `KEYS`:** session listing uses `KEYS` in Redis; fine for class-scale traffic.
- **ngrok banned (ERR_NGROK_3208):** use Vercel or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/).
=======
