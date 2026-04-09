import jwt from "jsonwebtoken";

function requireSecret() {
  const s = process.env.JWT_SECRET;
  if (!s || !String(s).trim()) {
    const err = new Error("JWT_SECRET is not configured");
    err.status = 500;
    throw err;
  }
  return String(s).trim();
}

const SECRET = () => requireSecret();
const REFRESH_SECRET = () =>
  process.env.JWT_REFRESH_SECRET?.trim() || `${requireSecret()}_refresh`;

export const signToken = (payload) =>
  jwt.sign(payload, SECRET(), { expiresIn: "2h" });

export const verifyToken = (token) =>
  jwt.verify(token, SECRET());

export const signRefreshToken = (payload) =>
  jwt.sign(payload, REFRESH_SECRET(), { expiresIn: "7d" });

export const verifyRefreshToken = (token) =>
  jwt.verify(token, REFRESH_SECRET());
