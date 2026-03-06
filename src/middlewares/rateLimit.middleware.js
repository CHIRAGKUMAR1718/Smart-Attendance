import redis from "../config/redis.js";

export const createRateLimiter = ({
  keyPrefix,
  windowSeconds,
  max,
  message = "Too many requests",
} = {}) => {
  if (!keyPrefix) throw new Error("rateLimit: keyPrefix is required");
  if (!windowSeconds) throw new Error("rateLimit: windowSeconds is required");
  if (!max) throw new Error("rateLimit: max is required");

  return async (req, res, next) => {
    try {
      const ip = req.ip || req.headers["x-forwarded-for"] || "unknown";
      const key = `${keyPrefix}:${ip}`;

      const count = await redis.incr(key);
      if (count === 1) {
        await redis.expire(key, windowSeconds);
      }

      if (count > max) {
        const ttl = await redis.ttl(key);
        res.setHeader("Retry-After", String(Math.max(ttl, 0)));
        return res.status(429).json({ message, retryAfterSeconds: ttl });
      }

      next();
    } catch {
      // If Redis is down, fail open (don’t block auth)
      next();
    }
  };
};
