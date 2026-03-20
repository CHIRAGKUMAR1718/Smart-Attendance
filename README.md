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
- `POST /sessions/start` (auth) { classId, duration, chirpMinFreq?, chirpMaxFreq? }
- `POST /attendance/mark` (auth) { sessionId }
- `POST /attendance/mark-by-signal` (auth) { frequency }
- `GET /attendance/list` (auth) ?limit=&offset=
- `GET /attendance/session/:sessionId` (auth) ?limit=

## Deploy on Vercel (HTTPS for phones — recommended)

This app runs as one **serverless Express** function (`api/index.js`) with `public/**` bundled so teacher/student pages and APIs share one deployment.

### 1. Create external services (Vercel does not include Postgres/Redis)

| Service | Free tier | What to copy |
|--------|-----------|--------------|
| **[Neon](https://neon.tech)** (Postgres) | Yes | Connection string → `DB_URL` |
| **[Upstash](https://upstash.com)** (Redis) | Yes | **Redis** URL (starts with `rediss://`) → `REDIS_URL` |

Run **`src/db/schema.sql`** in Neon’s SQL editor (same as local setup). Ensure `pgcrypto` extension if needed.

### 2. Import project in Vercel

1. Push this repo to GitHub.
2. [Vercel Dashboard](https://vercel.com/new) → **Add New Project** → import the repo.
3. **Environment variables** (Production + Preview):

   | Name | Example |
   |------|---------|
   | `DB_URL` | `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require` |
   | `REDIS_URL` | `rediss://default:xxx@xxx.upstash.io:6379` |
   | `JWT_SECRET` | Long random string (same idea as local `.env`) |

   Do **not** commit `.env`.

4. **Deploy**. Default **Build Command** can stay empty / `npm run vercel-build`; **Output** is handled by Vercel.

### 3. URLs to use after deploy

Replace `https://YOUR-PROJECT.vercel.app` with your real domain:

- **Student:** `https://YOUR-PROJECT.vercel.app/student.html`
- **Teacher:** `https://YOUR-PROJECT.vercel.app/teacher.html`
- **Home:** `https://YOUR-PROJECT.vercel.app/`

HTTPS is automatic — microphone + Web Audio work on real phones.

### 4. Optional: test like production locally

```bash
npm install
npx vercel dev
```

Uses your linked project env (after `vercel link`).

### Notes

- **Cold starts:** first request after idle can be slower; normal for serverless.
- **Redis `KEYS`:** session listing uses `KEYS` in Redis; fine for class-scale traffic. For huge scale, refactor to a Redis set of active session IDs.
- **ngrok banned (ERR_NGROK_3208):** that’s ngrok’s account policy — use Vercel or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/) (`cloudflared tunnel --url http://localhost:3000`) instead.
