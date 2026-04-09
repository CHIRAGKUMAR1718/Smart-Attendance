import "./env.js";
import pkg from "pg";
const { Pool } = pkg;

const isVercel = process.env.VERCEL === "1";

/**
 * Normalize Neon/Vercel DB URLs: strip psql wrappers, extract postgres://, drop
 * channel_binding=require (often breaks node-pg; sslmode=require is enough).
 * parsePostgresHost() still rejects Prisma Accelerate and broken hosts.
 */
function normalizePostgresUrl(raw) {
  let s = String(raw || "")
    .trim()
    .replace(/\r/g, "");
  const cli = s.match(/^\s*psql\s+['"](.+?)['"]\s*$/is);
  if (cli) s = cli[1].trim();
  if (!/^postgres(ql)?:\/\//i.test(s)) {
    const m = s.match(/(postgres(ql)?:\/\/[^\s'"]+)/i);
    if (m) s = m[1].trim();
  }
  s = s.replace(/&channel_binding=require(?=&|$)/gi, "");
  s = s.replace(/\?channel_binding=require(?=&|$)/gi, "?");
  s = s.replace(/\?$/g, "");
  return s.trim();
}

function parsePostgresHost(connectionString) {
  const t = normalizePostgresUrl(connectionString);
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
    const normalized = normalizePostgresUrl(raw);
    if (parsePostgresHost(normalized)) return normalized;
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
