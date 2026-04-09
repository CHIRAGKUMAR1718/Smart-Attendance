import redis from "../config/redis.js";
import { db } from "../config/db.js";
import { normalizeSessionCode } from "./session.service.js";

const fail = (status, message) => {
  const err = new Error(message);
  err.status = status;
  throw err;
};

export const markStudentAttendance = async (sessionId, studentId) => {
  const sessionKey = `chirp:session:${sessionId}`;
  const exists = await redis.exists(sessionKey);

  if (!exists) fail(404, "Session expired");

  const existing = await db.query(
    "SELECT 1 FROM attendance_records WHERE session_id = $1 AND student_id = $2 LIMIT 1",
    [sessionId, studentId]
  );
  if (existing.rows.length) return { marked: false, sessionId };

  const dedupeKey = `attendance:${sessionId}:${studentId}`;
  const duplicate = await redis.exists(dedupeKey);

  if (duplicate) return { marked: false, sessionId };

  const ttl = await redis.ttl(sessionKey);
  const dedupeTtl = ttl > 0 ? ttl : 120;

  await redis.set(dedupeKey, "1", "EX", dedupeTtl);

  await db.query(
    "INSERT INTO attendance_records(session_id, student_id) VALUES ($1,$2)",
    [sessionId, studentId]
  );

  return { marked: true, sessionId };
};

export const markStudentAttendanceByCode = async (code, studentId) => {
  const normalizedCode = normalizeSessionCode(code);
  const sessionId = await redis.get(`chirp:code:${normalizedCode}`);
  if (!sessionId) fail(404, "Invalid or expired code");

  const result = await markStudentAttendance(sessionId, studentId);
  return { ...result, code: normalizedCode };
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
    `SELECT attendance_records.id, attendance_records.session_id, attendance_records.student_id, attendance_records.timestamp,
            u.email AS student_email
     FROM attendance_records
     LEFT JOIN users u ON u.id::text = attendance_records.student_id
     WHERE attendance_records.session_id = $1
     ORDER BY attendance_records.id DESC
     LIMIT $2`,
    [sessionId, safeLimit]
  );

  return result.rows;
};

export const listAttendanceForStudent = async ({ studentId, limit = 20 } = {}) => {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 20, 100));
  const result = await db.query(
    `SELECT ar.id, ar.session_id, ar.student_id, ar.timestamp,
            s.class_id, s.code AS session_code
     FROM attendance_records ar
     LEFT JOIN sessions s ON s.id = ar.session_id
     WHERE ar.student_id = $1
     ORDER BY ar.id DESC
     LIMIT $2`,
    [studentId, safeLimit]
  );
  return result.rows;
};

export const listAttendanceByClassForTeacher = async ({ classId, teacherId, limit = 1000 } = {}) => {
  const safeLimit = Math.max(1, Math.min(Number(limit) || 1000, 3000));
  if (!classId) fail(400, "classId is required");

  const result = await db.query(
    `SELECT ar.id, ar.session_id, ar.student_id, ar.timestamp,
            s.code AS session_code, s.created_at AS session_date,
            u.email AS student_email
     FROM attendance_records ar
     JOIN sessions s ON s.id = ar.session_id
     LEFT JOIN users u ON u.id::text = ar.student_id
     WHERE s.class_id = $1 AND s.teacher_id = $2
     ORDER BY s.created_at DESC, ar.id DESC
     LIMIT $3`,
    [classId, teacherId, safeLimit]
  );

  return result.rows;
};
