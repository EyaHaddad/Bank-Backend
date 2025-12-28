const BASE_URL = "http://localhost:8000/api";

// Store/Get JWT Token
function authHeaders() {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}