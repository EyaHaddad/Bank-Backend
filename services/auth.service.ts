
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