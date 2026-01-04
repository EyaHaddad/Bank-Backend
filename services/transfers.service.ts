import api from "./axiosInstance";
import type {
  Transfer,
  TransferRequest,
  TransferListResponse,
  TransferSummary,
  TransferFilters,
  TransferInitiateRequest,
  TransferInitiateResponse,
} from "@/types/transfer";

// ---------------- TRANSFERS ----------------

/**
 * Initiate a transfer with OTP verification
 * This sends an OTP to the user's email and returns a transfer token
 */
export async function initiateTransfer(
  data: TransferInitiateRequest
): Promise<TransferInitiateResponse> {
  const response = await api.post<TransferInitiateResponse>("/transfers/initiate", data);
  return response.data;
}

/**
 * Confirm a transfer with OTP code
 */
export async function confirmTransfer(
  transferToken: string,
  otpCode: string
): Promise<Transfer> {
  const params = new URLSearchParams();
  params.append("transfer_token", transferToken);
  params.append("otp_code", otpCode);

  const response = await api.post<Transfer>(`/transfers/confirm?${params.toString()}`);
  return response.data;
}

/**
 * Create a new transfer to a beneficiary (without OTP - legacy)
 */
export async function createTransfer(data: TransferRequest): Promise<Transfer> {
  const response = await api.post<Transfer>("/transfers/", data);
  return response.data;
}

/**
 * Get a specific transfer by ID
 */
export async function getTransferById(transferId: string): Promise<Transfer> {
  const response = await api.get<Transfer>(`/transfers/${transferId}`);
  return response.data;
}

/**
 * List transfers for a specific account
 */
export async function listAccountTransfers(
  accountId: string,
  filters?: TransferFilters
): Promise<TransferListResponse> {
  const params = new URLSearchParams();

  if (filters?.page) params.append("page", filters.page.toString());
  if (filters?.page_size)
    params.append("page_size", filters.page_size.toString());
  if (filters?.transfer_status)
    params.append("transfer_status", filters.transfer_status);

  const response = await api.get<TransferListResponse>(
    `/transfers/account/${accountId}`,
    { params }
  );
  return response.data;
}

/**
 * List all transfers for the current user
 */
export async function listMyTransfers(
  filters?: TransferFilters
): Promise<TransferListResponse> {
  const params = new URLSearchParams();

  if (filters?.page) params.append("page", filters.page.toString());
  if (filters?.page_size)
    params.append("page_size", filters.page_size.toString());
  if (filters?.transfer_status)
    params.append("transfer_status", filters.transfer_status);

  const response = await api.get<TransferListResponse>("/transfers/", {
    params,
  });
  return response.data;
}

/**
 * Get transfer summary for a specific account
 */
export async function getTransferSummary(
  accountId: string,
  startDate?: string,
  endDate?: string
): Promise<TransferSummary> {
  const params = new URLSearchParams();

  if (startDate) params.append("start_date", startDate);
  if (endDate) params.append("end_date", endDate);

  const response = await api.get<TransferSummary>(
    `/transfers/account/${accountId}/summary`,
    { params }
  );
  return response.data;
}