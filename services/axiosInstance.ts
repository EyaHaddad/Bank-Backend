import axios, {
  AxiosError,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";

// Base URL for API - use environment variable or default
export const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = sessionStorage.getItem("access_token");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Clear token and cookies
      sessionStorage.removeItem("access_token");
      sessionStorage.removeItem("user_role");
      
      // Clear cookies
      if (typeof document !== "undefined") {
        document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        document.cookie = "user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      }
      
      // Redirect to login only if not already there (prevent infinite loop)
      if (typeof window !== "undefined" && window.location.pathname !== "/") {
        window.location.href = "/";
      }
    }
    return Promise.reject(error);
  }
);

// Helper function to get auth headers (for backward compatibility)
export function authHeaders() {
  const token = sessionStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Helper to store auth data (uses sessionStorage - cleared when browser closes)
export function setAuthData(accessToken: string, role: string) {
  sessionStorage.setItem("access_token", accessToken);
  sessionStorage.setItem("user_role", role);
}

// Helper to clear auth data
export function clearAuthData() {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("user_role");
}

// Helper to get current role
export function getUserRole(): string | null {
  return sessionStorage.getItem("user_role");
}

// Helper to check if user is authenticated
export function isAuthenticated(): boolean {
  return !!sessionStorage.getItem("access_token");
}

export default api;