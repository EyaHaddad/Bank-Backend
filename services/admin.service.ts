import api from "./axiosInstance";
import type { AccountType } from "@/types/account";

// ---------------- ADMIN TYPES ----------------

export interface PromoteUserResponse {
  message: string;
  user_id: string;
  new_role: string;
}

export interface AdminAccount {
  id: string;
  user_id: string;
  user_name: string;
  user_email: string;
  balance: number;
  currency: string;
  account_type: AccountType;
  status: string;
}

export interface AdminAccountCreate {
  user_id: string;
  initial_balance?: number;
  account_type?: AccountType;
}

export interface UserStatusResponse {
  message: string;
  user_id: string;
  is_active: boolean;
}

export interface AccountStatusResponse {
  message: string;
  account_id: string;
  status: string;
}

export interface AdminUserUpdate {
  firstname?: string;
  lastname?: string;
  email?: string;
}

export interface AccountBalanceUpdate {
  new_balance: number;
}

// ---------------- USER MANAGEMENT ----------------

/**
 * Activate a user account (Admin only)
 */
export async function activateUser(userId: string): Promise<UserStatusResponse> {
  const response = await api.post<UserStatusResponse>(`/admin/users/${userId}/activate`);
  return response.data;
}

/**
 * Deactivate a user account (Admin only)
 */
export async function deactivateUser(userId: string): Promise<UserStatusResponse> {
  const response = await api.post<UserStatusResponse>(`/admin/users/${userId}/deactivate`);
  return response.data;
}

/**
 * Delete a user (Admin only)
 */
export async function adminDeleteUser(userId: string): Promise<void> {
  await api.delete(`/admin/users/${userId}`);
}

/**
 * Update a user's information (Admin only)
 */
export async function adminUpdateUser(userId: string, data: AdminUserUpdate): Promise<any> {
  const response = await api.put(`/admin/users/${userId}`, data);
  return response.data;
}

// ---------------- ACCOUNT MANAGEMENT ----------------

/**
 * Get all accounts in the system (Admin only)
 */
export async function listAllAccounts(): Promise<AdminAccount[]> {
  const response = await api.get<AdminAccount[]>("/admin/accounts");
  return response.data;
}

/**
 * Create a new account for a user (Admin only)
 */
export async function createAccountForUser(data: AdminAccountCreate): Promise<AdminAccount> {
  const response = await api.post<AdminAccount>("/admin/accounts", data);
  return response.data;
}

/**
 * Activate a blocked account (Admin only)
 */
export async function activateAccount(accountId: string): Promise<AccountStatusResponse> {
  const response = await api.post<AccountStatusResponse>(`/admin/accounts/${accountId}/activate`);
  return response.data;
}

/**
 * Block an account (Admin only)
 */
export async function blockAccount(accountId: string): Promise<AccountStatusResponse> {
  const response = await api.post<AccountStatusResponse>(`/admin/accounts/${accountId}/block`);
  return response.data;
}

/**
 * Close an account permanently (Admin only)
 */
export async function closeAccount(accountId: string): Promise<AccountStatusResponse> {
  const response = await api.post<AccountStatusResponse>(`/admin/accounts/${accountId}/close`);
  return response.data;
}

/**
 * Delete an account permanently (Admin only)
 */
export async function deleteAccount(accountId: string): Promise<void> {
  await api.delete(`/admin/accounts/${accountId}`);
}

/**
 * Update account balance - admin correction (Admin only)
 */
export async function updateAccountBalance(accountId: string, newBalance: number): Promise<AdminAccount> {
  const response = await api.put<AdminAccount>(`/admin/accounts/${accountId}/balance`, { new_balance: newBalance });
  return response.data;
}

// ---------------- ROLE MANAGEMENT ----------------

/**
 * Promote a user to admin role (Admin only)
 */
export async function promoteUserToAdmin(
  userId: string
): Promise<PromoteUserResponse> {
  const response = await api.post<PromoteUserResponse>(
    `/admin/promote/${userId}`
  );
  return response.data;
}

/**
 * Demote an admin to regular user (Admin only)
 */
export async function demoteAdminToUser(
  userId: string
): Promise<PromoteUserResponse> {
  const response = await api.post<PromoteUserResponse>(
    `/admin/demote/${userId}`
  );
  return response.data;
}