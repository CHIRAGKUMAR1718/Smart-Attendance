import { loginUser, registerUser, refreshAccessToken } from "../services/auth.service.js";

export const register = async (req, res, next) => {
  try {
    const { email, password, role } = req.body;
    const data = await registerUser({ email, password, role });
    res.status(201).json(data);
  } catch (e) {
    next(e);
  }
};

export const login = async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const data = await loginUser({ email, password });
    res.json(data);
  } catch (e) {
    next(e);
  }
};

export const refresh = async (req, res, next) => {
  try {
    const { refreshToken } = req.body;
    const data = await refreshAccessToken(refreshToken);
    res.json(data);
  } catch (e) {
    next(e);
  }
};
