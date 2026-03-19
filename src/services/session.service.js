import { v4 as uuid } from "uuid";
import redis from "../config/redis.js";
import { db } from "../config/db.js";

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
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
  tableReady = true;
};

const generateCode = () => {
  const chars = "ABCDEFGHJKMNPQRSTUVWXYZ23456789";
  let code = "";
  for (let i = 0; i < 6; i++) code += chars[Math.floor(Math.random() * chars.length)];
  return code;
};

export const createSession = async ({ classId, duration, teacherId }) => {
  if (!classId || typeof classId !== "string") fail(400, "classId is required");
  const dur = Number(duration);
  if (!dur || dur < 30 || dur > 3600) fail(400, "duration must be 30–3600 seconds");

  const sessionId = uuid();
  let code, attempts = 0;
  do {
    code = generateCode();
    if (!(await redis.exists(`chirp:code:${code}`))) break;
  } while (++attempts < 10);
  if (attempts >= 10) fail(500, "Could not generate unique session code");

  await redis.set(`chirp:session:${sessionId}`, JSON.stringify({ classId, teacherId, code }), "EX", dur);
  await redis.set(`chirp:code:${code}`, sessionId, "EX", dur);

  await ensureTable();
  await db.query(
    `INSERT INTO sessions (id, class_id, code, teacher_id, duration) VALUES ($1,$2,$3,$4,$5)
     ON CONFLICT (id) DO NOTHING`,
    [sessionId, classId, code, teacherId, dur]
  );

  return { sessionId, code, expiresIn: dur };
};

export const getSessionByCode = async (code) => {
  if (!code) fail(400, "Code is required");
  const sessionId = await redis.get(`chirp:code:${String(code).toUpperCase().trim()}`);
  if (!sessionId) fail(404, "Invalid or expired code");
  const raw = await redis.get(`chirp:session:${sessionId}`);
  if (!raw) fail(404, "Session expired");
  const session = JSON.parse(raw);
  const ttl = await redis.ttl(`chirp:session:${sessionId}`);
  return { sessionId, classId: session.classId, remainingSeconds: ttl };
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
      sessions.push({ sessionId, classId: data.classId, code: data.code, remainingSeconds: ttl });
    }
  }

  return sessions;
};
