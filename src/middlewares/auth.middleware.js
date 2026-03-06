import { verifyToken } from "../utils/jwt.js";

export const authMiddleware = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ message: "Unauthorized" });

  let token = authHeader.trim();
  if (token.toLowerCase().startsWith("bearer ")) token = token.slice(7).trim();

  // Postman sometimes sends the token with quotes; strip them.
  if (
    (token.startsWith('"') && token.endsWith('"')) ||
    (token.startsWith("'") && token.endsWith("'"))
  ) {
    token = token.slice(1, -1).trim();
  }

  if (!token) return res.status(401).json({ message: "Unauthorized" });

  try {
    req.user = verifyToken(token);
    next();
  } catch {
    res.status(401).json({ message: "Invalid token" });
  }
};
