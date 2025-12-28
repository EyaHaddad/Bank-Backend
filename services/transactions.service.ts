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
