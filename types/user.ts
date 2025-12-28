// User types matching backend schemas

export interface UserBase {
  firstname: string;
  lastname: string;
  email: string;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserUpdate {
  firstname?: string;
  lastname?: string;
  password?: string;
}

export interface User extends UserBase {
  id: string;
}

export interface PasswordChange {
  current_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface PasswordChangeResponse {
  message: string;
}