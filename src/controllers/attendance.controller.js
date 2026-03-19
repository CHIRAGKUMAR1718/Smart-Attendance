import {
  listAttendance,
  listAttendanceBySession,
  listAttendanceByStudent,
  listAttendanceByClass,
  markStudentAttendance,
  markStudentAttendanceByFixedSignal,
} from "../services/attendance.service.js";

export const markAttendance = async (req, res, next) => {
  try {
    const { sessionId } = req.body;
    const studentId = req.user.userId;
    await markStudentAttendance(sessionId, studentId);
    res.status(201).json({ message: "Attendance marked" });
  } catch (e) {
    next(e);
  }
};

export const markAttendanceBySignal = async (req, res, next) => {
  try {
    const studentId = req.user.userId;
    const sessionId = await markStudentAttendanceByFixedSignal(studentId);
    res.status(201).json({ message: "Attendance marked", sessionId });
  } catch (e) {
    next(e);
  }
};

export const getAttendance = async (req, res, next) => {
  try {
    const { limit, offset } = req.query;
    const rows = await listAttendance({ limit, offset });
    res.json(rows);
  } catch (e) {
    next(e);
  }
};

export const getAttendanceForSession = async (req, res, next) => {
  try {
    const { sessionId } = req.params;
    const { limit } = req.query;
    const rows = await listAttendanceBySession({ sessionId, limit });
    res.json(rows);
  } catch (e) {
    next(e);
  }
};

export const getByClass = async (req, res, next) => {
  try {
    const { classId } = req.params;
    const rows = await listAttendanceByClass({
      teacherId: req.user.userId,
      classId,
    });
    res.json(rows);
  } catch (e) {
    next(e);
  }
};

export const getMyAttendance = async (req, res, next) => {
  try {
    const { limit, offset } = req.query;
    const rows = await listAttendanceByStudent({
      studentId: req.user.userId,
      limit,
      offset,
    });
    res.json(rows);
  } catch (e) {
    next(e);
  }
};
