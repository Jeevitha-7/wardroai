const API_URL = "http://localhost:8000";

export async function analyzeOutfit(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Analysis failed");
  }

  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_URL}/history`);
  return res.json();
}