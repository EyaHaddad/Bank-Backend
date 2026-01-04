"use client";

import { useEffect, useCallback } from "react";
import { clearAuthData } from "@/services/axiosInstance";

// Clé pour stocker le timestamp de la dernière activité
const LAST_ACTIVITY_KEY = "last_activity_timestamp";
const SESSION_MARKER_KEY = "session_active_marker";

// Durée maximale d'inactivité (30 minutes en millisecondes)
const MAX_INACTIVITY_MS = 30 * 60 * 1000;

/**
 * Clear all auth cookies
 */
function clearAuthCookies(): void {
  if (typeof document !== "undefined") {
    document.cookie = "access_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    document.cookie = "user_role=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}

/**
 * Complete cleanup of all auth data
 */
function clearAllAuthData(): void {
  clearAuthData();
  clearAuthCookies();
  sessionStorage.removeItem(LAST_ACTIVITY_KEY);
  sessionStorage.removeItem(SESSION_MARKER_KEY);
}

/**
 * Update the last activity timestamp
 */
function updateActivityTimestamp(): void {
  if (typeof sessionStorage !== "undefined") {
    sessionStorage.setItem(LAST_ACTIVITY_KEY, Date.now().toString());
  }
}

/**
 * Check if the session has expired due to inactivity
 */
function isSessionExpired(): boolean {
  if (typeof sessionStorage === "undefined") return true;
  
  const lastActivity = sessionStorage.getItem(LAST_ACTIVITY_KEY);
  if (!lastActivity) return true;
  
  const lastActivityTime = parseInt(lastActivity, 10);
  const now = Date.now();
  
  return now - lastActivityTime > MAX_INACTIVITY_MS;
}

/**
 * Check if this is a fresh page load vs a refresh within the same session
 */
function checkSessionMarker(): boolean {
  if (typeof sessionStorage === "undefined") return false;
  
  const marker = sessionStorage.getItem(SESSION_MARKER_KEY);
  return marker === "active";
}

/**
 * Set session marker to indicate active session
 */
function setSessionMarker(): void {
  if (typeof sessionStorage !== "undefined") {
    sessionStorage.setItem(SESSION_MARKER_KEY, "active");
  }
}

/**
 * SecurityGuard Component
 * 
 * Ce composant gère la sécurité des tokens d'authentification:
 * - Efface les tokens lors de la fermeture du navigateur/onglet
 * - Vérifie l'inactivité et invalide les sessions expirées
 * - Met à jour le timestamp d'activité lors des interactions utilisateur
 */
export function SecurityGuard({ children }: { children: React.ReactNode }) {
  // Fonction de nettoyage complète
  const handleCleanup = useCallback(() => {
    clearAllAuthData();
  }, []);

  // Vérification de sécurité au chargement
  useEffect(() => {
    // Vérifie si la session est expirée par inactivité
    if (isSessionExpired()) {
      clearAllAuthData();
      return;
    }

    // Initialise le marqueur de session et le timestamp
    setSessionMarker();
    updateActivityTimestamp();
  }, []);

  // Gestion des événements de fermeture et de visibilité
  useEffect(() => {
    // Événement beforeunload - déclenché avant la fermeture de l'onglet/navigateur
    const handleBeforeUnload = (event: BeforeUnloadEvent) => {
      // Efface les données d'authentification pour prévenir les fuites
      clearAllAuthData();
    };

    // Événement pagehide - plus fiable que beforeunload sur mobile
    const handlePageHide = (event: PageTransitionEvent) => {
      // persisted = true signifie que la page est mise en cache (bfcache)
      // Dans ce cas, on ne nettoie pas pour permettre la navigation avant/arrière
      if (!event.persisted) {
        clearAllAuthData();
      }
    };

    // Événement visibilitychange - gère la mise en arrière-plan de l'onglet
    const handleVisibilityChange = () => {
      if (document.visibilityState === "hidden") {
        // Met à jour le timestamp quand l'onglet est caché
        updateActivityTimestamp();
      } else if (document.visibilityState === "visible") {
        // Vérifie l'expiration quand l'onglet redevient visible
        if (isSessionExpired()) {
          clearAllAuthData();
          // Redirige vers la page de connexion
          if (typeof window !== "undefined" && window.location.pathname !== "/") {
            window.location.href = "/";
          }
        } else {
          updateActivityTimestamp();
        }
      }
    };

    // Détection d'activité utilisateur pour mettre à jour le timestamp
    const handleUserActivity = () => {
      updateActivityTimestamp();
    };

    // Enregistre les écouteurs d'événements
    window.addEventListener("beforeunload", handleBeforeUnload);
    window.addEventListener("pagehide", handlePageHide);
    document.addEventListener("visibilitychange", handleVisibilityChange);
    
    // Événements d'activité utilisateur
    document.addEventListener("mousedown", handleUserActivity);
    document.addEventListener("keydown", handleUserActivity);
    document.addEventListener("touchstart", handleUserActivity);
    document.addEventListener("scroll", handleUserActivity, { passive: true });

    // Vérification périodique de l'expiration (toutes les minutes)
    const intervalId = setInterval(() => {
      if (isSessionExpired()) {
        clearAllAuthData();
        if (typeof window !== "undefined" && window.location.pathname !== "/") {
          window.location.href = "/";
        }
      }
    }, 60000);

    // Nettoyage lors du démontage du composant
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
      window.removeEventListener("pagehide", handlePageHide);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      document.removeEventListener("mousedown", handleUserActivity);
      document.removeEventListener("keydown", handleUserActivity);
      document.removeEventListener("touchstart", handleUserActivity);
      document.removeEventListener("scroll", handleUserActivity);
      clearInterval(intervalId);
    };
  }, [handleCleanup]);

  return <>{children}</>;
}

export default SecurityGuard;
