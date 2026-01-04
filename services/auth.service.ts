import api, { setAuthData, clearAuthData } from "./axiosInstance";
import type {
  RegisterUserRequest,
  Token,
  RegisterResponse,
  VerifyEmailRequest,
  VerifyEmailResponse,
  ResendOTPRequest,
  ResendOTPResponse,
  ForgotPasswordRequest,
  ForgotPasswordResponse,
  ResetPasswordRequest,
  ResetPasswordResponse,
} from "@/types/auth";

// Clés pour la gestion de session sécurisée
const LAST_ACTIVITY_KEY = "last_activity_timestamp";
const SESSION_MARKER_KEY = "session_active_marker";

// ---------------- AUTH ----------------

/**
 * Set auth cookies for middleware access (session cookies - cleared when browser closes)
 */
function setAuthCookies(token: string, role: string): void {
  // Session cookies (no max-age) - cleared when browser closes
  document.cookie = `access_token=${token}; path=/; SameSite=Lax`;
  document.cookie = `user_role=${role}; path=/; SameSite=Lax`;
}

/**
 * Clear auth cookies
 */
function clearAuthCookies(): void {
  document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  document.cookie = "user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}

/**
 * Initialize session security markers
 */
function initializeSessionSecurity(): void {
  if (typeof sessionStorage !== "undefined") {
    sessionStorage.setItem(LAST_ACTIVITY_KEY, Date.now().toString());
    sessionStorage.setItem(SESSION_MARKER_KEY, "active");
  }
}

/**
 * Clear session security markers
 */
function clearSessionSecurity(): void {
  if (typeof sessionStorage !== "undefined") {
    sessionStorage.removeItem(LAST_ACTIVITY_KEY);
    sessionStorage.removeItem(SESSION_MARKER_KEY);
  }
}

/**
 * Register a new user
 */
export async function registerUser(
  data: RegisterUserRequest
): Promise<RegisterResponse> {
  const response = await api.post<RegisterResponse>("/auth/", data);
  return response.data;
}

/**
 * Verify email with OTP code
 */
export async function verifyEmail(
  data: VerifyEmailRequest
): Promise<VerifyEmailResponse> {
  const response = await api.post<VerifyEmailResponse>("/auth/verify-email", data);
  return response.data;
}

/**
 * Resend OTP verification code
 */
export async function resendOTP(
  data: ResendOTPRequest
): Promise<ResendOTPResponse> {
  const response = await api.post<ResendOTPResponse>("/auth/resend-otp", data);
  return response.data;
}

/**
 * Login user and get access token
 * Note: Backend uses OAuth2PasswordRequestForm which expects form data
 */
export async function loginUser(
  email: string,
  password: string
): Promise<Token> {
  // OAuth2PasswordRequestForm requires form-urlencoded data
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await api.post<Token>("/auth/token", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  // Store auth data in sessionStorage
  setAuthData(response.data.access_token, response.data.role);
  
  // Store auth data in cookies for middleware
  setAuthCookies(response.data.access_token, response.data.role);

  // Initialize session security markers
  initializeSessionSecurity();

  return response.data;
}

/**
 * Logout user - clear local storage, cookies, and session security
 */
export function logoutUser(): void {
  clearAuthData();
  clearAuthCookies();
  clearSessionSecurity();
}

/**
 * Request password reset - sends OTP to email
 */
export async function forgotPassword(
  data: ForgotPasswordRequest
): Promise<ForgotPasswordResponse> {
  const response = await api.post<ForgotPasswordResponse>("/auth/forgot-password", data);
  return response.data;
}

/**
 * Reset password using OTP verification
 */
export async function resetPassword(
  data: ResetPasswordRequest
): Promise<ResetPasswordResponse> {
  const response = await api.post<ResetPasswordResponse>("/auth/reset-password", data);
  return response.data;
}