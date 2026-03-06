import jwt from "jsonwebtoken";

const SECRET = () => process.env.JWT_SECRET;
const REFRESH_SECRET = () => process.env.JWT_REFRESH_SECRET || process.env.JWT_SECRET + "_refresh";

export const signToken = (payload) =>
  jwt.sign(payload, SECRET(), { expiresIn: "2h" });

export const verifyToken = (token) =>
  jwt.verify(token, SECRET());

export const signRefreshToken = (payload) =>
  jwt.sign(payload, REFRESH_SECRET(), { expiresIn: "7d" });

export const verifyRefreshToken = (token) =>
  jwt.verify(token, REFRESH_SECRET());
