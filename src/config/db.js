import "./env.js";
import pkg from "pg";
const { Pool } = pkg;

const isVercel = process.env.VERCEL === "1";

/**
 * Must be a real libpq URL for `pg`. Rejects Prisma Accelerate (`prisma+...`) and broken hosts like `base`
 * (happens when the wrong Vercel/Neon env var is picked or a URL is truncated).
 */
function parsePostgresHost(connectionString) {
  const t = String(connectionString || "").trim();
  if (!/^postgres(ql)?:\/\//i.test(t)) return null;
  if (/^prisma\+/i.test(t)) return null;
  const at = t.indexOf("@");
  if (at === -1) return null;
  const afterAt = t.slice(at + 1);
  const end = afterAt.search(/[/:?]/);
  const host = (end === -1 ? afterAt : afterAt.slice(0, end)).trim();
  if (!host || host.toLowerCase() === "base") return null;
  const local = /^(localhost|127\.0\.0\.1)$/i.test(host);
  if (!local && !host.includes(".")) return null;
  return host;
}

function pickPostgresUrl() {
  const keys = [
    "DB_URL",
    "POSTGRES_URL",
    "DATABASE_URL",
    "POSTGRES_URL_NON_POOLING",
    "POSTGRES_PRISMA_URL",
  ];
  for (const key of keys) {
    const raw = process.env[key];
    if (!raw) continue;
    if (parsePostgresHost(raw)) return String(raw).trim();
  }
  return "";
}

/**
 * Vercel + Neon integration often injects POSTGRES_URL / DATABASE_URL.
 * Manual deploys use DB_URL — we accept all common names.
 */
const dbUrl = pickPostgresUrl();
/** Remote Postgres (Neon, Supabase, etc.) usually needs SSL; skip for local Docker */
const needsSsl =
  Boolean(dbUrl) && !/localhost|127\.0\.0\.1/i.test(dbUrl);

export const db = new Pool({
  ...(dbUrl ? { connectionString: dbUrl } : {}),
  max: isVercel ? 1 : 10,
  idleTimeoutMillis: isVercel ? 5000 : 30000,
  connectionTimeoutMillis: 20000,
  ...(needsSsl && { ssl: { rejectUnauthorized: false } }),
});
