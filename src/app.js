import express from "express";
import cors from "cors";
import { fileURLToPath } from "url";
import path from "path";

import authRoutes from "./routes/auth.routes.js";
import sessionRoutes from "./routes/session.routes.js";
import attendanceRoutes from "./routes/attendance.routes.js";

const app = express();

const __dirname = path.dirname(fileURLToPath(import.meta.url));

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "..", "public")));

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