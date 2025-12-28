// Beneficiary types matching backend schemas

export interface BeneficiaryCreate {
  name: string;
  bank_name: string;
  iban: string;
  email?: string;
}

export interface BeneficiaryUpdate {
  name?: string;
  bank_name?: string;
  email?: string;
}

export interface Beneficiary {
  id: string;
  user_id: string;
  name: string;
  bank_name: string;
  iban: string;
  email?: string;
  is_verified: boolean;
  created_at: string;
  updated_at?: string;
}

export interface BeneficiaryListResponse {
  beneficiaries: Beneficiary[];
  total: number;
}