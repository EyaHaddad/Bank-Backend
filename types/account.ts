// Account types matching backend schemas

export type AccountType = "COURANT" | "EPARGNE";

export interface AccountCreate {
  initial_balance?: number;
  account_type?: AccountType;
}

export interface AccountUpdate {
  // No updateable fields - currency is always TND
}

export interface Account {
  id: string;
  user_id: string;
  balance: number;
  currency: string; // Always "TND"
  account_type: AccountType;
  status: string;
}

// NOTE: DepositRequest and WithdrawRequest have been removed.
// Clients cannot directly deposit/withdraw money.

export interface AccountTransferRequest {
  target_account_id: string;
  amount: number;
}

export interface BalanceResponse {
  account_id: string;
  balance: number;
  currency: string;
}