import type React from "react";
import { useEffect, useState } from "react";
import { Upload, Cpu, WifiOff, Database } from "lucide-react";
import { analyzeOutfit, getHistory, getAnalysisById, getHealth } from "./api";

export default function App() {
  const [page, setPage] = useState<"analyze" | "results" | "history" | "settings">("analyze");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    if (page === "history") loadHistory();
    if (page === "settings") loadHealth();
  }, [page]);

  async function loadHistory() {
    try {
      const data = await getHistory();
      setHistory(data || []);
    } catch {
      setHistory([]);
    }
  }

  async function loadHealth() {
    try {
      const data = await getHealth();
      setHealth(data);
    } catch {
      setHealth(null);
    }
  }

  function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
  }

  async function handleAnalyze() {
    if (!file) return alert("Upload an outfit image first");

    setLoading(true);
    try {
      const data = await analyzeOutfit(file);
      setResult(data);
      setPage("results");
    } catch {
      alert("Failed to analyze image. Check backend is running.");
    }
    setLoading(false);
  }

  async function openHistoryItem(id: string) {
    try {
      const data = await getAnalysisById(id);
      setResult(data);
      setPage("results");
    } catch {
      alert("Failed to load analysis");
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>WardroAI</h1>
        <p>Offline AI Outfit Breakdown</p>

        <nav>
          <button
            type="button"
            className={page === "analyze" ? "active" : ""}
            onClick={() => setPage("analyze")}
          >
            Analyze Outfit
          </button>
          <button
            type="button"
            className={page === "results" ? "active" : ""}
            onClick={() => setPage("results")}
          >
            Results
          </button>
          <button
            type="button"
            className={page === "history" ? "active" : ""}
            onClick={() => setPage("history")}
          >
            History
          </button>
          <button
            type="button"
            className={page === "settings" ? "active" : ""}
            onClick={() => setPage("settings")}
          >
            Settings
          </button>
        </nav>

        <div className="status">
          <span>
            <WifiOff size={16} /> Offline Mode
          </span>
          <span>
            <Cpu size={16} /> CPU Inference
          </span>
          <span>
            <Database size={16} /> Local Database
          </span>
        </div>
      </aside>

      <main className="main">
        {page === "analyze" && (
          <>
            <section className="hero">
              <h2>Upload an outfit image</h2>
              <p>
                WardroAI turns outfit images into clean fashion details using offline CPU
                processing.
              </p>
            </section>

            <section className="grid">
              <div className="card">
                <h3>Outfit Image</h3>

                <label className="upload">
                  <Upload size={28} />
                  <span>Choose image</span>
                  <input type="file" accept="image/*" onChange={handleFile} />
                </label>

                {preview && <img className="preview" src={preview} alt="Uploaded outfit preview" />}

                <button type="button" className="primary" onClick={handleAnalyze}>
                  {loading ? "Analyzing..." : "Analyze Outfit"}
                </button>
              </div>

              <InfoCard />
            </section>
          </>
        )}

        {page === "results" && (
          <>
            <section className="hero">
              <h2>Outfit Results</h2>
              <p>Clear breakdown of the latest uploaded outfit.</p>
            </section>

            {!result ? (
              <div className="card">No result yet. Upload and analyze an outfit first.</div>
            ) : (
              <>
                <section className="grid">
                  <div className="card">
                    <h3>Outfit Breakdown</h3>
                    <OutfitItem title="Topwear" item={result.outfit_breakdown.topwear} />
                    <OutfitItem title="Bottomwear" item={result.outfit_breakdown.bottomwear} />
                    <OutfitItem title="Footwear" item={result.outfit_breakdown.footwear} />

                    <div className="metadata">
                      <DetailRow label="Style" value={result.fashion_metadata.style} />
                      <DetailRow label="Occasion" value={result.fashion_metadata.occasion} />
                      <DetailRow label="Season" value={result.fashion_metadata.season} />
                      <DetailRow
                        label="Color Harmony"
                        value={result.fashion_metadata.color_harmony}
                      />
                      <DetailRow label="Confidence" value={`${result.confidence_score}%`} />
                      <DetailRow label="Outfit Score" value={`${result.outfit_score}%`} />
                    </div>
                  </div>

                  <div className="card">
                    <h3>Fashion Summary</h3>
                    <DetailRow label="Image" value={result.image_name} />
                    <DetailRow label="Mode" value={result.runtime?.mode} />
                    <DetailRow label="Device" value={result.runtime?.device} />
                    <DetailRow label="Inference" value={result.runtime?.inference} />

                    <div className="recommendation">
                      <h4>Recommendation</h4>
                      <p>{result.fashion_metadata.recommendation}</p>
                    </div>
                  </div>
                </section>

                <section className="card">
                  <h3>Analysis Notes</h3>
                  <div className="notes">
                    {result.fashion_metadata.notes?.map((note: string, i: number) => (
                      <p key={i}>{note}</p>
                    ))}
                  </div>
                </section>

                <section className="card">
                  <h3>Shopping Matches</h3>
                  <div className="matches">
                    {result.shopping_matches?.map((m: any, i: number) => (
                      <div className="match" key={i}>
                        <h4>{m.matched_product_name}</h4>
                        <p>
                          <b>Detected:</b> {m.detected_item}
                        </p>
                        <p>
                          <b>Category:</b> {m.category}
                        </p>
                        <p>
                          <b>Source:</b> {m.source}
                        </p>
                        <p>
                          <b>Price:</b> {m.estimated_price}
                        </p>
                        <p>
                          <b>Search Query:</b> {m.search_query}
                        </p>
                        <span>{m.match_score}% match</span>
                      </div>
                    ))}
                  </div>
                </section>

                <section className="card">
                  <div className="json-header">
                    <h3>Structured Output</h3>
                  </div>
                  <pre>{JSON.stringify(result, null, 2)}</pre>
                </section>
              </>
            )}
          </>
        )}

        {page === "history" && (
          <>
            <section className="hero">
              <h2>Analysis History</h2>
              <p>Previous outfit analyses saved locally in SQLite.</p>
            </section>

            <section className="card">
              <h3>Previous Analyses</h3>

              {history.length === 0 && <p>No history yet.</p>}

              {history.map((h) => (
                <button
                  type="button"
                  className="history-item"
                  key={h.id}
                  onClick={() => openHistoryItem(h.id)}
                >
                  <h4>{h.image_name}</h4>
                  <p>
                    {h.style} · {h.occasion} · {h.confidence}% confidence
                  </p>
                  <small>{h.created_at}</small>
                </button>
              ))}
            </section>
          </>
        )}

        {page === "settings" && (
          <>
            <section className="hero">
              <h2>Settings</h2>
              <p>Offline runtime and system information.</p>
            </section>

            <section className="grid">
              <div className="card">
                <h3>Runtime Settings</h3>
                <p>
                  <b>Offline Mode:</b> Enabled
                </p>
                <p>
                  <b>Inference:</b> CPU only
                </p>
                <p>
                  <b>Database:</b> SQLite local database
                </p>
                <p>
                  <b>Cloud APIs:</b> Disabled
                </p>
              </div>

              <div className="card">
                <h3>Backend Health</h3>
                {health ? (
                  <>
                    <p>
                      <b>Status:</b> {health.status}
                    </p>
                    <p>
                      <b>Runtime:</b> {health.runtime}
                    </p>
                    <p>
                      <b>Database:</b> {health.database}
                    </p>
                    <p>
                      <b>Cloud APIs:</b> {health.cloud_apis}
                    </p>
                  </>
                ) : (
                  <p>Backend health unavailable. Make sure FastAPI is running.</p>
                )}
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

function OutfitItem({ title, item }: any) {
  if (!item) return null;

  return (
    <div className="outfit-item">
      <div>
        <h4>{title}</h4>
        <p>{item.item_name}</p>
        <small>{item.detected_item}</small>
      </div>
      <div className="outfit-meta">
        <span>
          <i style={{ background: item.hex_color }} />
          {item.dominant_color || item.color}
        </span>
        <small>{item.confidence}%</small>
      </div>
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value?: string | number }) {
  return (
    <p className="detail-row">
      <b>{label}</b>
      <span>{value || "Not available"}</span>
    </p>
  );
}

function InfoCard() {
  return (
    <div className="card">
      <h3>How it works</h3>
      <p>1. Upload an outfit image.</p>
      <p>2. WardroAI analyzes clothing colors and categories offline.</p>
      <p>3. Results are shown as readable fashion cards.</p>
      <p>4. History is saved locally using SQLite.</p>
    </div>
  );
}
