import { createSession, getActiveSessions, getSessionByCode, getSessionHistory } from "../services/session.service.js";

export const startSession = async (req, res, next) => {
  try {
    const { classId, duration, chirpMinFreq, chirpMaxFreq } = req.body;
    const teacherId = req.user.userId;
    const session = await createSession({ classId, duration, teacherId, chirpMinFreq, chirpMaxFreq });
    res.status(201).json(session);
  } catch (e) {
    next(e);
  }
};

export const activeSessions = async (req, res, next) => {
  try {
    const sessions = await getActiveSessions(req.user.userId);
    res.json(sessions);
  } catch (e) {
    next(e);
  }
};

export const sessionHistory = async (req, res, next) => {
  try {
    const rows = await getSessionHistory(req.user.userId);
    res.json(rows);
  } catch (e) {
    next(e);
  }
};

export const lookupByCode = async (req, res, next) => {
  try {
    const session = await getSessionByCode(req.params.code);
    res.json(session);
  } catch (e) {
    next(e);
  }
};
