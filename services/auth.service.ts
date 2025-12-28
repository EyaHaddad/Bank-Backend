import api, { setAuthData, clearAuthData } from "./axiosInstance";
import type {
  RegisterUserRequest,
  Token,
  RegisterResponse,
  VerifyEmailRequest,
  VerifyEmailResponse,
  ResendOTPRequest,
  ResendOTPResponse,
} from "@/types/auth";

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

  // Store auth data in localStorage
  setAuthData(response.data.access_token, response.data.role);
  
  // Store auth data in cookies for middleware
  setAuthCookies(response.data.access_token, response.data.role);

  return response.data;
}

/**
 * Logout user - clear local storage and cookies
 */
export function logoutUser(): void {
  clearAuthData();
  clearAuthCookies();
}