import api from "./axios";

export const login = (data) => {
      return api.post("/auth/login", data);
};

export const refreshToken = (data) => {
      return api.post("/auth/refresh", data);
};