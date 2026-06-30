const API_URL = import.meta.env.VITE_API_URL ?? "";

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

export async function getAnalysisById(id: string) {
  const res = await fetch(`${API_URL}/analysis/${id}`);
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_URL}/health`);
  return res.json();
}
