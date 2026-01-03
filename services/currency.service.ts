import api from "./axiosInstance";

// Types for currency operations
export interface CurrencyRate {
  code: string;
  name: string;
  rate: number;
  flag: string;
}

export interface ExchangeRatesResponse {
  base_currency: string;
  base_currency_name: string;
  last_updated: string;
  rates: CurrencyRate[];
}

export interface ConversionRequest {
  amount: number;
  target_currency: string;
}

export interface ConversionResponse {
  original_amount: number;
  converted_amount: number;
  target_currency: string;
  rate: number;
  base_currency: string;
}

export interface BankContactInfo {
  bank_name: string;
  address: string;
  city: string;
  country: string;
  postal_code: string;
  phone: string;
  fax: string;
  email: string;
  website: string;
  working_hours: string;
  swift_code: string;
}

/**
 * Get current exchange rates with TND as base currency
 */
export const getExchangeRates = async (): Promise<ExchangeRatesResponse> => {
  const response = await api.get<ExchangeRatesResponse>("/currency/rates");
  return response.data;
};

/**
 * Convert amount from TND to target currency
 */
export const convertCurrency = async (
  request: ConversionRequest
): Promise<ConversionResponse> => {
  const response = await api.post<ConversionResponse>(
    "/currency/convert",
    request
  );
  return response.data;
};

/**
 * Get bank contact information
 */
export const getBankContact = async (): Promise<BankContactInfo> => {
  const response = await api.get<BankContactInfo>("/currency/contact");
  return response.data;
};
