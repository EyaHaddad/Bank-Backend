import api from "./axiosInstance";
import type {
  User,
  UserCreate,
  UserUpdate,
  PasswordChange,
  PasswordChangeResponse,
} from "@/types/user";

// ---------------- USERS ----------------

/**
 * Get current authenticated user's profile
 */
export async function getMyProfile(): Promise<User> {
  const response = await api.get<User>("/users/me");
  return response.data;
}

/**
 * Get all users (Admin only)
 */
export async function listUsers(): Promise<User[]> {
  const response = await api.get<User[]>("/users/");
  return response.data;
}

/**
 * Create a new user (Admin only)
 */
export async function createUser(data: UserCreate): Promise<User> {
  const response = await api.post<User>("/users/", data);
  return response.data;
}

/**
 * Get a specific user by ID (Admin only)
 */
export async function getUserById(userId: string): Promise<User> {
  const response = await api.get<User>(`/users/${userId}`);
  return response.data;
}

/**
 * Update a user's profile
 */
export async function updateUser(
  userId: string,
  data: UserUpdate
): Promise<User> {
  const response = await api.put<User>(`/users/${userId}`, data);
  return response.data;
}

/**
 * Delete a user (Admin only)
 */
export async function deleteUser(userId: string): Promise<void> {
  await api.delete(`/users/${userId}`);
}

/**
 * Change user's password
 */
export async function changePassword(
  userId: string,
  data: PasswordChange
): Promise<PasswordChangeResponse> {
  const response = await api.post<PasswordChangeResponse>(
    `/users/${userId}/change-password`,
    data
  );
  return response.data;
}