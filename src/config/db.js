import "./env.js";
import pkg from "pg";
const { Pool } = pkg;

const isVercel = process.env.VERCEL === "1";

/**
 * Vercel + Neon integration often injects POSTGRES_URL / DATABASE_URL.
 * Manual deploys use DB_URL — we accept all common names.
 */
const dbUrl =
  process.env.DB_URL ||
  process.env.POSTGRES_URL ||
  process.env.DATABASE_URL ||
  process.env.POSTGRES_PRISMA_URL ||
  "";
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
