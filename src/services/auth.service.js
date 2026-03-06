import bcrypt from "bcrypt";
import { db } from "../config/db.js";
import { signToken, signRefreshToken, verifyRefreshToken } from "../utils/jwt.js";

export const registerUser = async ({ email, password, role = "student" }) => {
  const normalizedEmail = String(email || "").trim().toLowerCase();
  if (!normalizedEmail || !password) {
    const err = new Error("Email and password are required");
    err.status = 400;
    throw err;
  }

  const passwordHash = await bcrypt.hash(password, 12);

  try {
    const result = await db.query(
      `INSERT INTO users (email, password_hash, role)
       VALUES ($1, $2, $3)
       RETURNING id, email, role, created_at`,
      [normalizedEmail, passwordHash, role]
    );

    const user = result.rows[0];
    const accessToken = signToken({ userId: user.id, role: user.role });
    const refreshToken = signRefreshToken({ userId: user.id, role: user.role });

    return { user, accessToken, refreshToken };
  } catch (e) {
    // Postgres unique violation
    if (e && e.code === "23505") {
      const err = new Error("Email already registered");
      err.status = 409;
      throw err;
    }
    throw e;
  }
};

export const loginUser = async ({ email, password }) => {
  const normalizedEmail = String(email || "").trim().toLowerCase();
  if (!normalizedEmail || !password) {
    const err = new Error("Email and password are required");
    err.status = 400;
    throw err;
  }

  const result = await db.query(
    `SELECT id, email, role, password_hash
     FROM users
     WHERE email = $1`,
    [normalizedEmail]
  );

  const user = result.rows[0];
  if (!user) {
    const err = new Error("Invalid credentials");
    err.status = 401;
    throw err;
  }

  const ok = await bcrypt.compare(password, user.password_hash);
  if (!ok) {
    const err = new Error("Invalid credentials");
    err.status = 401;
    throw err;
  }

  const accessToken = signToken({ userId: user.id, role: user.role });
  const refreshToken = signRefreshToken({ userId: user.id, role: user.role });
  return {
    user: { id: user.id, email: user.email, role: user.role },
    accessToken,
    refreshToken,
  };
};

export const refreshAccessToken = async (token) => {
  if (!token) {
    const err = new Error("Refresh token is required");
    err.status = 400;
    throw err;
  }

  let payload;
  try {
    payload = verifyRefreshToken(token);
  } catch {
    const err = new Error("Invalid or expired refresh token");
    err.status = 401;
    throw err;
  }

  const result = await db.query("SELECT id, email, role FROM users WHERE id = $1", [payload.userId]);
  const user = result.rows[0];
  if (!user) {
    const err = new Error("User not found");
    err.status = 401;
    throw err;
  }

  const accessToken = signToken({ userId: user.id, role: user.role });
  return { accessToken, user };
};
