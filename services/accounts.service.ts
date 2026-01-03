import api from "./axiosInstance";
import type {
  Account,
  AccountCreate,
  AccountUpdate,
  AccountTransferRequest,
  BalanceResponse,
} from "@/types/account";

// ---------------- ACCOUNTS ----------------

/**
 * Get all accounts for the current user
 */
export async function getMyAccounts(): Promise<Account[]> {
  const response = await api.get<Account[]>("/accounts/");
  return response.data;
}

/**
 * Create a new account for the current user (always TND currency)
 */
export async function createAccount(data: AccountCreate): Promise<Account> {
  const response = await api.post<Account>("/accounts/", data);
  return response.data;
}

/**
 * Get a specific account by ID
 */
export async function getAccountById(accountId: string): Promise<Account> {
  const response = await api.get<Account>(`/accounts/${accountId}`);
  return response.data;
}

/**
 * Update an account
 */
export async function updateAccount(
  accountId: string,
  data: AccountUpdate
): Promise<Account> {
  const response = await api.put<Account>(`/accounts/${accountId}`, data);
  return response.data;
}

/**
 * Delete an account
 */
export async function deleteAccount(accountId: string): Promise<void> {
  await api.delete(`/accounts/${accountId}`);
}

// NOTE: Deposit and Withdraw functions have been removed.
// Clients cannot directly deposit/withdraw money.
// Money can only be:
// 1. Transferred between the client's own accounts (below function)
// 2. Sent to beneficiaries via the transfers service

/**
 * Transfer money between the client's own accounts
 */
export async function transferBetweenAccounts(
  accountId: string,
  data: AccountTransferRequest
): Promise<Account> {
  const response = await api.post<Account>(
    `/accounts/${accountId}/transfer`,
    data
  );
  return response.data;
}

/**
 * Get the balance of an account
 */
export async function getBalance(accountId: string): Promise<BalanceResponse> {
  const response = await api.get<BalanceResponse>(
    `/accounts/${accountId}/balance`
  );
  return response.data;
}