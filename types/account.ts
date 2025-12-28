// Account types matching backend schemas

export interface AccountCreate {
  currency?: string;
  initial_balance?: number;
}

export interface AccountUpdate {
  currency?: string;
}

export interface Account {
  id: string;
  user_id: string;
  balance: number;
  currency: string;
}

export interface DepositRequest {
  amount: number;
}

export interface WithdrawRequest {
  amount: number;
}

export interface AccountTransferRequest {
  target_account_id: string;
  amount: number;
}

export interface BalanceResponse {
  account_id: string;
  balance: number;
  currency: string;
}