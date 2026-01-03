import api from "./axiosInstance";
import type {
  Transaction,
  TransactionListResponse,
  TransactionFilters,
} from "@/types/transaction";

// ---------------- TRANSACTIONS ----------------
// NOTE: Credit and Debit endpoints have been removed.
// Clients cannot directly credit/debit their accounts.
// Money can only be:
// 1. Transferred between the client's own accounts
// 2. Sent to beneficiaries via the transfers service

/**
 * Get a specific transaction by ID
 */
export async function getTransactionById(
  transactionId: string
): Promise<Transaction> {
  const response = await api.get<Transaction>(
    `/transactions/${transactionId}`
  );
  return response.data;
}

/**
 * List transactions for a specific account
 */
export async function listAccountTransactions(
  accountId: string,
  filters?: TransactionFilters
): Promise<TransactionListResponse> {
  const params = new URLSearchParams();

  if (filters?.page) params.append("page", filters.page.toString());
  if (filters?.page_size)
    params.append("page_size", filters.page_size.toString());
  if (filters?.transaction_type)
    params.append("transaction_type", filters.transaction_type);
  if (filters?.transaction_status)
    params.append("transaction_status", filters.transaction_status);

  const response = await api.get<TransactionListResponse>(
    `/transactions/account/${accountId}`,
    { params }
  );
  return response.data;
}

/**
 * List all transactions for the current user
 */
export async function listMyTransactions(
  filters?: TransactionFilters
): Promise<TransactionListResponse> {
  const params = new URLSearchParams();

  if (filters?.page) params.append("page", filters.page.toString());
  if (filters?.page_size)
    params.append("page_size", filters.page_size.toString());
  if (filters?.transaction_type)
    params.append("transaction_type", filters.transaction_type);
  if (filters?.transaction_status)
    params.append("transaction_status", filters.transaction_status);

  const response = await api.get<TransactionListResponse>("/transactions/", {
    params,
  });
  return response.data;
}