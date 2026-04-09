import { v4 as uuid } from "uuid";
import redis from "../config/redis.js";
import { db } from "../config/db.js";

export const DEFAULT_CHIRP_MIN_FREQ = 18000;
export const DEFAULT_CHIRP_MAX_FREQ = 20000;
const SESSION_CODE_REGEX = /^\d{6}$/;

const fail = (status, message) => {
  const err = new Error(message);
  err.status = status;
  throw err;
};

let tableReady = false;
const ensureTable = async () => {
  if (tableReady) return;
  await db.query(`
    CREATE TABLE IF NOT EXISTS sessions (
      id VARCHAR(100) PRIMARY KEY,
      class_id TEXT NOT NULL,
      code VARCHAR(6) NOT NULL,
      teacher_id VARCHAR(100) NOT NULL,
      duration INTEGER NOT NULL,
      chirp_min_freq INTEGER NOT NULL DEFAULT ${DEFAULT_CHIRP_MIN_FREQ},
      chirp_max_freq INTEGER NOT NULL DEFAULT ${DEFAULT_CHIRP_MAX_FREQ},
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
  await db.query(`ALTER TABLE sessions ADD COLUMN IF NOT EXISTS chirp_min_freq INTEGER NOT NULL DEFAULT ${DEFAULT_CHIRP_MIN_FREQ}`);
  await db.query(`ALTER TABLE sessions ADD COLUMN IF NOT EXISTS chirp_max_freq INTEGER NOT NULL DEFAULT ${DEFAULT_CHIRP_MAX_FREQ}`);
  tableReady = true;
};

const generateCode = () => {
  let code = "";
  for (let i = 0; i < 6; i++) code += Math.floor(Math.random() * 10);
  return code;
};

export const normalizeSessionCode = (code) => {
  const normalized = String(code ?? "").trim();
  if (!SESSION_CODE_REGEX.test(normalized)) fail(400, "Code must be exactly 6 digits");
  return normalized;
};

export const createSession = async ({ classId, duration, teacherId, chirpMinFreq, chirpMaxFreq }) => {
  if (!classId || typeof classId !== "string") fail(400, "classId is required");
  const dur = Number(duration);
  if (!dur || dur < 30 || dur > 3600) fail(400, "duration must be 30–3600 seconds");
  const minFreq = Number(chirpMinFreq ?? DEFAULT_CHIRP_MIN_FREQ);
  const maxFreq = Number(chirpMaxFreq ?? DEFAULT_CHIRP_MAX_FREQ);
  if (!Number.isFinite(minFreq) || !Number.isFinite(maxFreq)) fail(400, "chirp frequencies must be numbers");
  if (minFreq < 17000 || maxFreq > 21000 || minFreq >= maxFreq) {
    fail(400, "chirp frequency range must be between 17000 and 21000 Hz and min < max");
  }

  const sessionId = uuid();
  let code, attempts = 0;
  do {
    code = generateCode();
    if (!(await redis.exists(`chirp:code:${code}`))) break;
  } while (++attempts < 10);
  if (attempts >= 10) fail(500, "Could not generate unique session code");

  await redis.set(
    `chirp:session:${sessionId}`,
    JSON.stringify({ classId, teacherId, code, chirpMinFreq: minFreq, chirpMaxFreq: maxFreq }),
    "EX",
    dur
  );
  await redis.set(`chirp:code:${code}`, sessionId, "EX", dur);

  await ensureTable();
  await db.query(
    `INSERT INTO sessions (id, class_id, code, teacher_id, duration, chirp_min_freq, chirp_max_freq)
     VALUES ($1,$2,$3,$4,$5,$6,$7)
     ON CONFLICT (id) DO NOTHING`,
    [sessionId, classId, code, teacherId, dur, minFreq, maxFreq]
  );

  return { sessionId, code, expiresIn: dur, chirpMinFreq: minFreq, chirpMaxFreq: maxFreq };
};

export const getSessionByCode = async (code) => {
  const normalizedCode = normalizeSessionCode(code);
  const sessionId = await redis.get(`chirp:code:${normalizedCode}`);
  if (!sessionId) fail(404, "Invalid or expired code");
  const raw = await redis.get(`chirp:session:${sessionId}`);
  if (!raw) fail(404, "Session expired");
  const session = JSON.parse(raw);
  const ttl = await redis.ttl(`chirp:session:${sessionId}`);
  return {
    sessionId,
    classId: session.classId,
    remainingSeconds: ttl,
    chirpMinFreq: session.chirpMinFreq ?? DEFAULT_CHIRP_MIN_FREQ,
    chirpMaxFreq: session.chirpMaxFreq ?? DEFAULT_CHIRP_MAX_FREQ,
  };
};

export const getSessionHistory = async (teacherId) => {
  await ensureTable();
  const result = await db.query(
    `SELECT s.id, s.class_id, s.code, s.duration, s.created_at,
            COUNT(ar.id)::int AS student_count
     FROM sessions s
     LEFT JOIN attendance_records ar ON s.id = ar.session_id
     WHERE s.teacher_id = $1
     GROUP BY s.id
     ORDER BY s.created_at DESC
     LIMIT 100`,
    [teacherId]
  );
  return result.rows;
};

export const getActiveSessions = async (teacherId) => {
  const keys = await redis.keys("chirp:session:*");
  const sessions = [];

  for (const key of keys) {
    const raw = await redis.get(key);
    if (!raw) continue;
    const data = JSON.parse(raw);
    if (data && data.teacherId === teacherId) {
      const ttl = await redis.ttl(key);
      const sessionId = key.replace("chirp:session:", "");
      sessions.push({
        sessionId,
        classId: data.classId,
        code: data.code,
        remainingSeconds: ttl,
        chirpMinFreq: data.chirpMinFreq ?? DEFAULT_CHIRP_MIN_FREQ,
        chirpMaxFreq: data.chirpMaxFreq ?? DEFAULT_CHIRP_MAX_FREQ,
      });
    }
  }

  return sessions;
};
