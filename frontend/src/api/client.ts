import axios from "axios";

const API_URL = "/api";

const client = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ====== Request interceptor: dodaje Bearer token ======
client.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ====== Response interceptor: auto-refresh przy 401 ======
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        // Brak refresh tokena — wyloguj
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const res = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const { access, refresh } = res.data;
        localStorage.setItem("access_token", access);
        if (refresh) {
          localStorage.setItem("refresh_token", refresh);
        }

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return client(originalRequest);
      } catch {
        // Refresh token wygasł — wyloguj
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

// ====== API functions ======

export const authAPI = {
  login: (username: string, password: string) =>
    client.post("/auth/token/", { username, password }),

  register: (username: string, email: string, password: string, password2: string) =>
    client.post("/auth/register/", { username, email, password, password2 }),

  me: () => client.get("/auth/me/"),
};

export const receiptsAPI = {
  list: (page = 1) => client.get(`/receipts/?page=${page}`),

  upload: (file: File) => {
    const formData = new FormData();
    formData.append("receipt_image", file);
    return client.post("/receipts/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  delete: (id: number) => client.delete(`/receipts/${id}/`),
};

export const statsAPI = {
  get: () => client.get("/stats/"),
};

export default client;
