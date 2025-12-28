// Notification types matching backend schemas

export type NotificationType = "EMAIL";
export type NotificationCategory = "OTP" | "TRANSACTION" | "NEWS";

export interface Notification {
  id: string;
  type: NotificationType;
  user_id: string;
  title: string;
  content: string;
  sent_at: string;
}

export interface NotificationListResponse {
  notifications: Notification[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface SendOTPNotificationRequest {
  user_id: string;
  otp_code: string;
}

export interface SendTransactionNotificationRequest {
  user_id: string;
  transaction_type: string;
  amount: number;
  account_number?: string;
  reference?: string;
}

export interface SendBankNewsNotificationRequest {
  user_id?: string;
  title: string;
  content: string;
}

export interface CreateNotificationRequest {
  user_id: string;
  title: string;
  content: string;
  category?: NotificationCategory;
}

export interface NotificationSentResponse {
  success: boolean;
  message: string;
  notification_id?: string;
}

export interface BulkNotificationSentResponse {
  success: boolean;
  message: string;
  total_sent: number;
  failed: number;
}

export interface NotificationFilters {
  page?: number;
  page_size?: number;
}