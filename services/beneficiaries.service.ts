import api from "./axiosInstance";
import type {
  Beneficiary,
  BeneficiaryCreate,
  BeneficiaryUpdate,
  BeneficiaryListResponse,
} from "@/types/beneficiary";

// ---------------- BENEFICIARIES ----------------

/**
 * Create a new beneficiary
 */
export async function createBeneficiary(
  data: BeneficiaryCreate
): Promise<Beneficiary> {
  const response = await api.post<Beneficiary>("/beneficiaries/", data);
  return response.data;
}

/**
 * List all beneficiaries for the current user
 */
export async function listBeneficiaries(
  verifiedOnly: boolean = false
): Promise<BeneficiaryListResponse> {
  const params = new URLSearchParams();
  params.append("verified_only", verifiedOnly.toString());

  const response = await api.get<BeneficiaryListResponse>("/beneficiaries/", {
    params,
  });
  return response.data;
}

/**
 * Get a specific beneficiary by ID
 */
export async function getBeneficiaryById(
  beneficiaryId: string
): Promise<Beneficiary> {
  const response = await api.get<Beneficiary>(
    `/beneficiaries/${beneficiaryId}`
  );
  return response.data;
}

/**
 * Update a beneficiary
 */
export async function updateBeneficiary(
  beneficiaryId: string,
  data: BeneficiaryUpdate
): Promise<Beneficiary> {
  const response = await api.put<Beneficiary>(
    `/beneficiaries/${beneficiaryId}`,
    data
  );
  return response.data;
}

/**
 * Delete a beneficiary
 */
export async function deleteBeneficiary(beneficiaryId: string): Promise<void> {
  await api.delete(`/beneficiaries/${beneficiaryId}`);
}

/**
 * Verify a beneficiary
 */
export async function verifyBeneficiary(
  beneficiaryId: string
): Promise<Beneficiary> {
  const response = await api.post<Beneficiary>(
    `/beneficiaries/${beneficiaryId}/verify`
  );
  return response.data;
}

/**
 * Unverify a beneficiary
 */
export async function unverifyBeneficiary(
  beneficiaryId: string
): Promise<Beneficiary> {
  const response = await api.post<Beneficiary>(
    `/beneficiaries/${beneficiaryId}/unverify`
  );
  return response.data;
}