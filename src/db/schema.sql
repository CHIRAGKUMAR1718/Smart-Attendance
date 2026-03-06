CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'student',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
  id VARCHAR(100) PRIMARY KEY,
  class_id TEXT NOT NULL,
  code VARCHAR(6) NOT NULL,
  teacher_id VARCHAR(100) NOT NULL,
  duration INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_teacher ON sessions (teacher_id);
CREATE INDEX IF NOT EXISTS idx_sessions_class ON sessions (class_id);

CREATE TABLE IF NOT EXISTS attendance_records (
  id SERIAL PRIMARY KEY,
  session_id VARCHAR(100) NOT NULL,
  student_id VARCHAR(100) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (session_id, student_id)
);

CREATE INDEX IF NOT EXISTS idx_attendance_session ON attendance_records (session_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance_records (student_id);
