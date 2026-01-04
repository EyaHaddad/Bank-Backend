// User types matching backend schemas

export type UserRole = "admin" | "user";

export interface UserBase {
  firstname: string;
  lastname: string;
  email: string;
}

export interface UserCreate extends UserBase {
  password: string;
  phone?: string;
  address?: string;
}

export interface UserUpdate {
  firstname?: string;
  lastname?: string;
  phone?: string;
  password?: string;
}

export interface User extends UserBase {
  id: string;
  phone?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
}

export interface PasswordChangeResponse {
  message: string;
}