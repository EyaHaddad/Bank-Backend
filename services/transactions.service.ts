import api from "./axiosInstance";
import type {
  Transaction,
  TransactionListResponse,
  CreditRequest,
  DebitRequest,
  TransactionFilters,
} from "@/types/transaction";

// ---------------- TRANSACTIONS ----------------

/**
 * Credit (deposit) money to an account
 */
export async function creditAccount(data: CreditRequest): Promise<Transaction> {
  const response = await api.post<Transaction>("/transactions/credit", data);
  return response.data;
}

/**
 * Debit (withdraw) money from an account
 */
export async function debitAccount(data: DebitRequest): Promise<Transaction> {
  const response = await api.post<Transaction>("/transactions/debit", data);
  return response.data;
}

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