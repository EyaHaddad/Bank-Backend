// Transfer types matching backend schemas

export type TransferStatus = "PENDING" | "COMPLETED" | "FAILED";

export interface TransferRequest {
  sender_account_id: string;
  beneficiary_id: string;
  amount: number;
  reference?: string;
}

export interface Transfer {
  id: string;
  sender_account_id: string;
  beneficiary_id: string;
  amount: number;
  status: TransferStatus;
  reference?: string;
  type: string;
  created_at: string;
  updated_at?: string;
  beneficiary_name?: string;
  beneficiary_iban?: string;
  beneficiary_bank?: string;
}

export interface TransferListResponse {
  transfers: Transfer[];
  total: number;
  page: number;
  page_size: number;
}

export interface TransferSummary {
  account_id: string;
  total_sent: number;
  transfer_count: number;
  average_transfer: number;
  period_start?: string;
  period_end?: string;
}

export interface TransferFilters {
  page?: number;
  page_size?: number;
  transfer_status?: TransferStatus;
}