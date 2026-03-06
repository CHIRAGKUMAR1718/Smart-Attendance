import { Router } from "express";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";
import { createRateLimiter } from "../middlewares/rateLimit.middleware.js";
import {
	getAttendance,
	getAttendanceForSession,
	getByClass,
	getMyAttendance,
	markAttendance,
} from "../controllers/attendance.controller.js";

const markLimiter = createRateLimiter({ keyPrefix: "rl:mark", windowSeconds: 60, max: 10 });

const router = Router();

router.post("/mark", authMiddleware, requireRole("student"), markLimiter, markAttendance);
router.get("/me", authMiddleware, requireRole("student"), getMyAttendance);
router.get("/list", authMiddleware, getAttendance);
router.get("/class/:classId", authMiddleware, requireRole("teacher"), getByClass);
router.get("/session/:sessionId", authMiddleware, requireRole("teacher"), getAttendanceForSession);

export default router;
