// OTP types matching backend schemas

export type OTPPurpose =
  | "LOGIN"
  | "TRANSACTION"
  | "PASSWORD_RESET"
  | "EMAIL_VERIFICATION"
  | "PHONE_VERIFICATION"
  | "ACCOUNT_ACTIVATION";

export interface OTPGenerateRequest {
  purpose: OTPPurpose;
}

export interface OTPVerifyRequest {
  code: string;
  purpose: OTPPurpose;
}

export interface OTP {
  id: string;
  purpose: OTPPurpose;
  expires_at: string;
  is_used: boolean;
  attempts: number;
  max_attempts: number;
  created_at: string;
}

export interface OTPVerifyResponse {
  success: boolean;
  message: string;
}

export interface OTPGenerateResponse {
  message: string;
  expires_at: string;
  purpose: OTPPurpose;
}