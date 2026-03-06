import "./env.js";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL, {
	lazyConnect: true,
	retryStrategy: (times) => Math.min(times * 1000, 30000),
});

let lastErrorLogMs = 0;

redis.on("error", (err) => {
	// Keep the process alive even if Redis is down.
	const now = Date.now();
	if (now - lastErrorLogMs > 5000) {
		lastErrorLogMs = now;
		console.error("Redis error:", err?.message || err);
	}
});

redis.connect().catch((err) => {
	console.error("Redis connect failed:", err?.message || err);
});

export default redis;
