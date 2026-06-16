const BASE_URL = "http://localhost:8000/api"

export async function chat(
  userId: string,
  feature: string,
  message: string,
): Promise<{ message: string; structured_data: Record<string, unknown> | null }> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, feature, message }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}
