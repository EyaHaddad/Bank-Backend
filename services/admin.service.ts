import api from "./axiosInstance";

// ---------------- ADMIN ----------------

export interface PromoteUserResponse {
  message: string;
  user_id: string;
  new_role: string;
}

/**
 * Promote a user to admin role (Admin only)
 */
export async function promoteUserToAdmin(
  userId: string
): Promise<PromoteUserResponse> {
  const response = await api.post<PromoteUserResponse>(
    `/admin/promote/${userId}`
  );
  return response.data;
}

/**
 * Demote an admin to regular user (Admin only)
 */
export async function demoteAdminToUser(
  userId: string
): Promise<PromoteUserResponse> {
  const response = await api.post<PromoteUserResponse>(
    `/admin/demote/${userId}`
  );
  return response.data;
}