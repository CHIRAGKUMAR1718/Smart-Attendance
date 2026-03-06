import { Router } from "express";
import { authMiddleware } from "../middlewares/auth.middleware.js";
import { requireRole } from "../middlewares/role.middleware.js";
import { startSession, activeSessions, sessionHistory, lookupByCode } from "../controllers/session.controller.js";

const router = Router();
router.post("/start", authMiddleware, requireRole("teacher"), startSession);
router.get("/active", authMiddleware, requireRole("teacher"), activeSessions);
router.get("/history", authMiddleware, requireRole("teacher"), sessionHistory);
router.get("/code/:code", authMiddleware, lookupByCode);
export default router;
