-- gen_random_uuid() is built into PostgreSQL 13+ (Neon). No pgcrypto extension needed.

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
  chirp_min_freq INTEGER NOT NULL DEFAULT 18000,
  chirp_max_freq INTEGER NOT NULL DEFAULT 20000,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE sessions ADD COLUMN IF NOT EXISTS chirp_min_freq INTEGER NOT NULL DEFAULT 18000;
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS chirp_max_freq INTEGER NOT NULL DEFAULT 20000;

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
