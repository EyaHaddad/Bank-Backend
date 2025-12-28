import api from "./axiosInstance";
import type {
  OTP,
  OTPGenerateRequest,
  OTPVerifyRequest,
  OTPGenerateResponse,
  OTPVerifyResponse,
  OTPPurpose,
} from "@/types/otp";

// ---------------- OTP ----------------

/**
 * Generate a new OTP
 */
export async function generateOTP(
  data: OTPGenerateRequest
): Promise<OTPGenerateResponse> {
  const response = await api.post<OTPGenerateResponse>("/otp/generate", data);
  return response.data;
}

/**
 * Verify an OTP
 */
export async function verifyOTP(
  data: OTPVerifyRequest
): Promise<OTPVerifyResponse> {
  const response = await api.post<OTPVerifyResponse>("/otp/verify", data);
  return response.data;
}

/**
 * Get OTP history for the current user
 */
export async function getOTPHistory(limit: number = 10): Promise<OTP[]> {
  const params = new URLSearchParams();
  params.append("limit", limit.toString());

  const response = await api.get<OTP[]>("/otp/history", { params });
  return response.data;
}

/**
 * Get active OTP for a specific purpose
 */
export async function getActiveOTP(purpose: OTPPurpose): Promise<OTP> {
  const response = await api.get<OTP>(`/otp/active/${purpose}`);
  return response.data;
}