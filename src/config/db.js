import "./env.js";
import pkg from "pg";
const { Pool } = pkg;

const isVercel = process.env.VERCEL === "1";
const dbUrl = process.env.DB_URL || "";
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
