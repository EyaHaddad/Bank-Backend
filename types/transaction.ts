// Transaction types matching backend schemas

export type TransactionType = "DEBIT" | "CREDIT" | "TRANSFER";
export type TransactionStatus = "PENDING" | "COMPLETED" | "FAILED";

// NOTE: CreditRequest and DebitRequest have been removed.
// Clients cannot directly credit/debit their accounts.

export interface Transaction {
  id: string;
  sender_account_id: string;
  type: TransactionType;
  amount: number;
  status: TransactionStatus;
  reference?: string;
  created_at: string;
  updated_at?: string;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  page: number;
  page_size: number;
}

export interface TransactionSummary {
  account_id: string;
  total_credits: number;
  total_debits: number;
  total_transfers_sent: number;
  transaction_count: number;
  period_start?: string;
  period_end?: string;
}

export interface TransactionFilters {
  page?: number;
  page_size?: number;
  transaction_type?: TransactionType;
  transaction_status?: TransactionStatus;
}