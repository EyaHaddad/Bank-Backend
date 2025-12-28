
// ---------------- ACCOUNTS ----------------

export async function getMyAccount() {
  const res = await fetch(`${BASE_URL}/accounts/me`, {
    headers: { ...authHeaders() },
  });
  return res.json();
}