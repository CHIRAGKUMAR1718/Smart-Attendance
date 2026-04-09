import { Router } from "express";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";
import {
	getAttendanceByClass,
	getAttendance,
	getAttendanceForSession,
	getMyAttendance,
	markAttendance,
	markAttendanceByCode,
} from "../controllers/attendance.controller.js";

const router = Router();

router.post("/mark", authMiddleware, markAttendance);
router.post("/mark-by-code", authMiddleware, requireRole("student"), markAttendanceByCode);
router.get("/list", authMiddleware, getAttendance);
router.get("/me", authMiddleware, requireRole("student"), getMyAttendance);
router.get("/class/:classId", authMiddleware, requireRole("teacher"), getAttendanceByClass);
router.get("/session/:sessionId", authMiddleware, getAttendanceForSession);

export default router;
