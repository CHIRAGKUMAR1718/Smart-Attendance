/**
 * Vercel serverless entry — all HTTP traffic is rewritten here (see vercel.json).
 * Local dev: use `npm run start` (src/server.js) instead.
 */
import "../src/config/env.js";
import app from "../src/app.js";

export default app;
