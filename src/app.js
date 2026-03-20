import express from "express";
import cors from "cors";
import fs from "fs";
import { fileURLToPath } from "url";
import path from "path";

import authRoutes from "./routes/auth.routes.js";
import sessionRoutes from "./routes/session.routes.js";
import attendanceRoutes from "./routes/attendance.routes.js";

const app = express();

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Behind Vercel / proxies (needed for secure cookies / IP if you add them later) */
if (process.env.VERCEL) {
  app.set("trust proxy", 1);
}

app.use(cors());
app.use(express.json());

function resolvePublicDir() {
  const candidates = [
    path.join(__dirname, "..", "public"),
    path.join(process.cwd(), "public"),
  ];
  for (const dir of candidates) {
    try {
      if (fs.existsSync(dir)) return dir;
    } catch {
      /* ignore */
    }
  }
  return path.join(process.cwd(), "public");
}

app.use(express.static(resolvePublicDir()));

app.use("/auth", authRoutes);
app.use("/sessions", sessionRoutes);
app.use("/attendance", attendanceRoutes);

app.use((_req, res) => {
  res.status(404).json({ message: "Route not found" });
});

app.use((err, _req, res, _next) => {
  const status = err.status || 500;
  res.status(status).json({
    message: err.message || "Internal server error",
    ...(process.env.NODE_ENV === "development" && { stack: err.stack }),
  });
});

export default app;