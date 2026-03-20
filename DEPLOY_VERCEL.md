# Connect everything to Vercel (step-by-step)

I can’t log into your accounts from Cursor. Follow this once; after that, every `git push` to `main` can auto-deploy.

## 0. Security

If you ever pasted a Neon or Redis URL in chat, **rotate that password** in Neon / Upstash before continuing.

---

## 1. Neon Postgres ↔ Vercel (easiest)

### Option A — Vercel Marketplace (recommended)

1. Deploy the repo on Vercel (see §4) **or** open an existing project.
2. Vercel → your project → **Storage** tab **or** [Vercel Marketplace → Neon](https://vercel.com/marketplace/neon).
3. **Install / Connect** Neon and link it to this project.
4. Vercel will inject env vars such as **`POSTGRES_URL`** / **`DATABASE_URL`**.  
   **This app reads those automatically** (see `src/config/db.js`); you do **not** have to duplicate them as `DB_URL` unless you want to.

### Option B — Manual

1. [Neon](https://neon.tech) → copy the **pooled** connection string (good for serverless).
2. Vercel → Project → **Settings** → **Environment Variables** → add **`DB_URL`** = that string.  
   Enable **Production** and **Preview** as needed.

### Initialize tables (required once)

1. Neon → **SQL Editor**.
2. Run:

   ```sql
   CREATE EXTENSION IF NOT EXISTS pgcrypto;
   ```

3. Paste and run the full contents of **`src/db/schema.sql`** from this repo.

---

## 2. Upstash Redis ↔ Vercel

1. [Upstash](https://upstash.com) → **Redis** → create a database (same region as Neon if possible).
2. **Connect** → copy the **Redis** URL (starts with `rediss://`).
3. Vercel → **Environment Variables** → **`REDIS_URL`** = that URL (Production + Preview).

If you use a Vercel integration that sets **`UPSTASH_REDIS_URL`** instead, this app also reads that (see `src/config/redis.js`).

---

## 3. JWT secret

Vercel → **Environment Variables** → add:

| Name | Value |
|------|--------|
| `JWT_SECRET` | Long random string (e.g. run `openssl rand -hex 32` in a terminal) |

Same for Production + Preview.

---

## 4. First deploy from GitHub

1. Repo on GitHub (this project).
2. [vercel.com/new](https://vercel.com/new) → **Import** the repo.
3. **Framework Preset:** Other (default is fine).
4. **Root directory:** repo root (where `vercel.json` lives).
5. Add env vars from §1–3 **before** or **after** first deploy; if you add after, click **Redeploy**.

---

## 5. URLs to share

After deploy:

- **Teacher:** `https://<your-project>.vercel.app/teacher.html`
- **Student:** `https://<your-project>.vercel.app/student.html`

HTTPS is automatic (microphone + audio work on phones).

---

## 6. Optional: CLI on your PC

```bash
npm i -g vercel
cd /path/to/smat-attendance
vercel login
vercel link
vercel env pull .env.local
```

Useful to test production env locally with `npx vercel dev`.

---

## Troubleshooting

| Symptom | Check |
|--------|--------|
| 500 on `/auth/*` | `JWT_SECRET`, `DB_URL` / `POSTGRES_URL`, schema ran on Neon |
| Redis errors | `REDIS_URL` is `rediss://…` from Upstash, not the REST URL only |
| Static 404 | Redeploy; `vercel.json` includes `public/**` in the function bundle |

---

## Env names this app understands

| Purpose | Variables tried (first match wins) |
|---------|-------------------------------------|
| Postgres | `DB_URL`, `POSTGRES_URL`, `DATABASE_URL`, `POSTGRES_PRISMA_URL` |
| Redis | `REDIS_URL`, `UPSTASH_REDIS_URL` |
| Auth | `JWT_SECRET` |
