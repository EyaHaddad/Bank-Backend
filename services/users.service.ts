
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