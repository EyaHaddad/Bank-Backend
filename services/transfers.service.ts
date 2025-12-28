import api from "./axiosInstance";
import type {
  Transfer,
  TransferRequest,
  TransferListResponse,
  TransferSummary,
  TransferFilters,
} from "@/types/transfer";

// ---------------- TRANSFERS ----------------

/**
 * Create a new transfer to a beneficiary
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