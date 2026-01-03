"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { loginUser, logoutUser, registerUser } from "@/services/auth.service";
import { getMyProfile } from "@/services/users.service";
import {
  isAuthenticated,
  getUserRole,
  clearAuthData,
} from "@/services/axiosInstance";
import type { User } from "@/types/user";
import type { RegisterUserRequest, Token } from "@/types/auth";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  role: string | null;
  error: string | null;
}

interface UseAuthReturn extends AuthState {
  login: (email: string, password: string) => Promise<Token>;
  logout: () => void;
  register: (data: RegisterUserRequest) => Promise<void>;
  refreshUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
    role: null,
    error: null,
  });

  // Fetch user profile
  const fetchUser = useCallback(async () => {
    if (!isAuthenticated()) {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
        error: null,
      });
      return;
    }

    try {
      const user = await getMyProfile();
      const role = getUserRole();
      setState({
        user,
        isLoading: false,
        isAuthenticated: true,
        role,
        error: null,
      });
    } catch (error) {
      clearAuthData();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
        role: null,
        error: "Failed to fetch user profile",
      });
    }
  }, []);

  // Initialize auth state on mount
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Login function
  const login = useCallback(
    async (email: string, password: string): Promise<Token> => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      try {
        const token = await loginUser(email, password);
        await fetchUser();

        // Redirect based on role
        if (token.role === "ADMIN") {
          router.push("/admin");
        } else {
          router.push("/client");
        }

        return token;
      } catch (error: unknown) {
        const errorMessage =
          error instanceof Error ? error.message : "Login failed";
        setState((prev) => ({
          ...prev,
          isLoading: false,
          error: errorMessage,
        }));
        throw error;
      }
    },
    [fetchUser, router]
  );

  // Logout function
  const logout = useCallback(() => {
    logoutUser();
    setState({
      user: null,
      isLoading: false,
      isAuthenticated: false,
      role: null,
      error: null,
    });
    router.push("/");
  }, [router]);

  // Register function
  const register = useCallback(async (data: RegisterUserRequest) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      await registerUser(data);
      setState((prev) => ({ ...prev, isLoading: false }));
    } catch (error: unknown) {
      const errorMessage =
        error instanceof Error ? error.message : "Registration failed";
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      throw error;
    }
  }, []);

  // Refresh user data
  const refreshUser = useCallback(async () => {
    await fetchUser();
  }, [fetchUser]);

  return {
    ...state,
    login,
    logout,
    register,
    refreshUser,
  };
}

export default useAuth;