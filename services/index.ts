// Re-export all services for convenient imports
export * from "./auth.service";
export * from "./users.service";
export * from "./accounts.service";
export * from "./transactions.service";
export * from "./transfers.service";
export * from "./beneficiaries.service";
export * from "./notifications.service";
export * from "./otps.service";
export * from "./admin.service";
export * from "./currency.service";

// Export axios instance and helpers
export { default as api } from "./axiosInstance";
export {
  BASE_URL,
  authHeaders,
  setAuthData,
  clearAuthData,
  getUserRole,
  isAuthenticated,
} from "./axiosInstance";
