import {
  listAttendanceByClassForTeacher,
  listAttendanceForStudent,
  listAttendance,
  listAttendanceBySession,
  markStudentAttendance,
  markStudentAttendanceByCode,
} from "../services/attendance.service.js";

export const markAttendance = async (req, res, next) => {
  try {
    const { sessionId } = req.body;
    const studentId = req.user.userId;

    const result = await markStudentAttendance(sessionId, studentId);
    res.status(result.marked ? 201 : 200).json({
      message: result.marked ? "Attendance marked" : "Already marked",
      marked: result.marked,
      sessionId: result.sessionId,
    });
  } catch (e) {
    next(e);
  }
};

export const markAttendanceByCode = async (req, res, next) => {
  try {
    const { code } = req.body;
    const studentId = req.user.userId;

    const result = await markStudentAttendanceByCode(code, studentId);
    res.status(result.marked ? 201 : 200).json({
      message: result.marked ? "Attendance marked" : "Already marked",
      marked: result.marked,
      sessionId: result.sessionId,
      code: result.code,
    });
  } catch (e) {
    next(e);
  }
};

export const getAttendance = async (req, res) => {
  const { limit, offset } = req.query;
  const rows = await listAttendance({ limit, offset });
  return res.status(200).json(rows);
};

export const getAttendanceForSession = async (req, res) => {
  const { sessionId } = req.params;
  const { limit } = req.query;

  if (!sessionId) return res.status(400).json({ message: "sessionId is required" });

  const rows = await listAttendanceBySession({ sessionId, limit });
  return res.status(200).json(rows);
};

export const getMyAttendance = async (req, res, next) => {
  try {
    const { limit } = req.query;
    const rows = await listAttendanceForStudent({ studentId: req.user.userId, limit });
    return res.status(200).json(rows);
  } catch (e) {
    next(e);
  }
};

export const getAttendanceByClass = async (req, res, next) => {
  try {
    const { classId } = req.params;
    const { limit } = req.query;
    const rows = await listAttendanceByClassForTeacher({
      classId,
      teacherId: req.user.userId,
      limit,
    });
    return res.status(200).json(rows);
  } catch (e) {
    next(e);
  }
};
