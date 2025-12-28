// Auth types matching backend schemas

export interface RegisterUserRequest {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  password: string;
  confirm_password: string;
}

export interface LoginUserRequest {
  username: string; // OAuth2PasswordRequestForm uses 'username' field (email)
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  role: string;
}

export interface TokenData {
  user_id: string | null;
  role: string | null;
}

export interface RegisterResponse {
  message: string;
}

export interface VerifyEmailRequest {
  email: string;
  code: string;
}

export interface VerifyEmailResponse {
  success: boolean;
  message: string;
}

export interface ResendOTPRequest {
  email: string;
}

export interface ResendOTPResponse {
  message: string;
}

export interface AuthError {
  detail: string;
}