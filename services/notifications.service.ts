import api from "./axiosInstance";
import type {
  Notification,
  NotificationListResponse,
  NotificationFilters,
  SendOTPNotificationRequest,
  SendTransactionNotificationRequest,
  SendBankNewsNotificationRequest,
  NotificationSentResponse,
  BulkNotificationSentResponse,
} from "@/types/notification";

// ---------------- NOTIFICATIONS ----------------

/**
 * Get all notifications for the current user
 */
export async function getMyNotifications(
  filters?: NotificationFilters
): Promise<NotificationListResponse> {
  const params = new URLSearchParams();

  if (filters?.page) params.append("page", filters.page.toString());
  if (filters?.page_size)
    params.append("page_size", filters.page_size.toString());

  const response = await api.get<NotificationListResponse>("/notifications/", {
    params,
  });
  return response.data;
}

/**
 * Get a specific notification by ID
 */
export async function getNotificationById(
  notificationId: string
): Promise<Notification> {
  const response = await api.get<Notification>(
    `/notifications/${notificationId}`
  );
  return response.data;
}

/**
 * Delete a notification
 */
export async function deleteNotification(
  notificationId: string
): Promise<{ message: string }> {
  const response = await api.delete<{ message: string }>(
    `/notifications/${notificationId}`
  );
  return response.data;
}

// ==================== Admin Endpoints ====================

/**
 * Send an OTP notification (Admin only)
 */
export async function sendOTPNotification(
  data: SendOTPNotificationRequest
): Promise<NotificationSentResponse> {
  const response = await api.post<NotificationSentResponse>(
    "/notifications/send/otp",
    data
  );
  return response.data;
}

/**
 * Send a transaction notification (Admin only)
 */
export async function sendTransactionNotification(
  data: SendTransactionNotificationRequest
): Promise<NotificationSentResponse> {
  const response = await api.post<NotificationSentResponse>(
    "/notifications/send/transaction",
    data
  );
  return response.data;
}

/**
 * Send a bank news notification (Admin only)
 */
export async function sendBankNewsNotification(
  data: SendBankNewsNotificationRequest
): Promise<BulkNotificationSentResponse> {
  const response = await api.post<BulkNotificationSentResponse>(
    "/notifications/send/news",
    data
  );
  return response.data;
}