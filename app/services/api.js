const BASE_URL = "http://localhost:8000/api";

// Store/Get JWT Token
function authHeaders() {
  const token = localStorage.getItem("access_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// ---------------- AUTH ----------------

export async function registerUser(data) {
  const res = await fetch(`${BASE_URL}/auth/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Registration failed");

  return res.json();
}

export async function loginUser(data) {
  const res = await fetch(`${BASE_URL}/auth/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Login failed");

  const token = await res.json();
  localStorage.setItem("access_token", token.access_token);

  return token;
}

// ---------------- USERS ----------------

export async function getMyProfile() {
  const res = await fetch(`${BASE_URL}/users/me`, {
    headers: { ...authHeaders() },
  });

  if (!res.ok) throw new Error("Unauthorized");

  return res.json();
}

export async function listUsers() {
  const res = await fetch(`${BASE_URL}/users`, {
    headers: { ...authHeaders() },
  });

  return res.json();
}

export async function createUser(data) {
  const res = await fetch(`${BASE_URL}/users`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function updateUser(id, data) {
  const res = await fetch(`${BASE_URL}/users/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function deleteUser(id) {
  const res = await fetch(`${BASE_URL}/users/${id}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  });

  return res.ok;
}

// ---------------- ACCOUNTS ----------------

export async function getMyAccount() {
  const res = await fetch(`${BASE_URL}/accounts/me`, {
    headers: { ...authHeaders() },
  });
  return res.json();
}

// ---------------- TRANSACTIONS ----------------

export async function makeTransfer(data) {
  const res = await fetch(`${BASE_URL}/transactions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error("Transfer failed");

  return res.json();
}
