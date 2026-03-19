import redis from "../config/redis.js";
import { db } from "../config/db.js";

const fail = (status, message) => {
  const err = new Error(message);
  err.status = status;
  throw err;
};

export const markStudentAttendance = async (sessionId, studentId) => {
  if (!sessionId) fail(400, "sessionId is required");

  const sessionKey = `chirp:session:${sessionId}`;
  const exists = await redis.exists(sessionKey);
  if (!exists) fail(404, "Session expired or invalid");

  const dedupeKey = `attendance:${sessionId}:${studentId}`;
  const duplicate = await redis.exists(dedupeKey);
  if (duplicate) fail(409, "Already marked");

  await redis.set(dedupeKey, "1", "EX", 120);

  try {
    await db.query(
      "INSERT INTO attendance_records(session_id, student_id) VALUES ($1,$2)",
      [sessionId, studentId]
    );
  } catch (e) {
    if (e && e.code === "23505") fail(409, "Already marked");
    throw e;
  }
};

export const markStudentAttendanceBySignalFrequency = async (studentId, detectedFrequency) => {
  const frequency = Number(detectedFrequency);
  if (!Number.isFinite(frequency)) fail(400, "detected frequency is required");

  const keys = await redis.keys("chirp:session:*");
  if (!keys.length) fail(404, "No active chirp session");

  let matched = null;
  let bestTtl = -1;

  for (const key of keys) {
    const raw = await redis.get(key);
    if (!raw) continue;
    const data = JSON.parse(raw);
    const minFreq = Number(data?.chirpMinFreq ?? 18000);
    const maxFreq = Number(data?.chirpMaxFreq ?? 20000);
    if (!Number.isFinite(minFreq) || !Number.isFinite(maxFreq)) continue;
    if (frequency < minFreq || frequency > maxFreq) continue;

    const ttl = await redis.ttl(key);
    if (ttl > bestTtl) {
      matched = key.replace("chirp:session:", "");
      bestTtl = ttl;
    }
  }

  if (!matched) fail(404, "No active session matches detected frequency");
  await markStudentAttendance(matched, studentId);
  return matched;
};

export const listAttendance = async ({ limit = 50, offset = 0 } = {}) => {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 200));
  const safeOffset = Math.max(0, Number(offset) || 0);

  const result = await db.query(
    `SELECT id, session_id, student_id, timestamp
     FROM attendance_records
     ORDER BY id DESC
     LIMIT $1 OFFSET $2`,
    [safeLimit, safeOffset]
  );

  return result.rows;
};

export const listAttendanceBySession = async ({ sessionId, limit = 200 } = {}) => {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 200, 500));

  const result = await db.query(
    `SELECT ar.id, ar.session_id, ar.student_id, ar.timestamp,
            u.email AS student_email
     FROM attendance_records ar
     LEFT JOIN users u ON ar.student_id = u.id::text
     WHERE ar.session_id = $1
     ORDER BY ar.timestamp ASC
     LIMIT $2`,
    [sessionId, safeLimit]
  );

  return result.rows;
};

export const listAttendanceByClass = async ({ teacherId, classId }) => {
  const result = await db.query(
    `SELECT ar.id, ar.session_id, ar.student_id, ar.timestamp,
            u.email AS student_email,
            s.class_id, s.code AS session_code, s.created_at AS session_date
     FROM attendance_records ar
     JOIN sessions s ON ar.session_id = s.id
     LEFT JOIN users u ON ar.student_id = u.id::text
     WHERE s.teacher_id = $1 AND LOWER(s.class_id) = LOWER($2)
     ORDER BY s.created_at DESC, ar.timestamp ASC`,
    [teacherId, classId]
  );
  return result.rows;
};

export const listAttendanceByStudent = async ({ studentId, limit = 50, offset = 0 } = {}) => {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 50, 200));
  const safeOffset = Math.max(0, Number(offset) || 0);

  const result = await db.query(
    `SELECT ar.id, ar.session_id, ar.student_id, ar.timestamp,
            s.class_id, s.code AS session_code
     FROM attendance_records ar
     LEFT JOIN sessions s ON ar.session_id = s.id
     WHERE ar.student_id = $1
     ORDER BY ar.id DESC
     LIMIT $2 OFFSET $3`,
    [studentId, safeLimit, safeOffset]
  );

  return result.rows;
};
