import { Router } from "express";
import { login, register, refresh } from "../controllers/auth.controller.js";
import { createRateLimiter } from "../middlewares/rateLimit.middleware.js";

const router = Router();

const registerLimiter = createRateLimiter({ keyPrefix: "rl:register", windowSeconds: 60, max: 5 });
const loginLimiter = createRateLimiter({ keyPrefix: "rl:login", windowSeconds: 60, max: 10 });

router.post("/register", registerLimiter, register);
router.post("/login", loginLimiter, login);
router.post("/refresh", refresh);

export default router;
