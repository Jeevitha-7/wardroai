import React, { useState } from "react";
import { Upload, Cpu, WifiOff, Database, Copy, Download } from "lucide-react";
import { analyzeOutfit } from "./api";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

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
    } catch (err) {
      alert("Failed to analyze image. Check backend is running.");
    }
    setLoading(false);
  }

  function copyJSON() {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    alert("JSON copied");
  }

  function downloadJSON() {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "wardroai-analysis.json";
    a.click();
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>WardroAI</h1>
        <p>Offline AI Outfit Breakdown</p>

        <nav>
          <button className="active">Analyze Outfit</button>
          <button>Results</button>
          <button>History</button>
          <button>Settings</button>
        </nav>

        <div className="status">
          <span><WifiOff size={16}/> Offline Mode</span>
          <span><Cpu size={16}/> CPU Inference</span>
          <span><Database size={16}/> Local Database</span>
        </div>
      </aside>

      <main className="main">
        <section className="hero">
          <h2>Upload an outfit image</h2>
          <p>WardroAI breaks it into structured fashion data using offline CPU processing.</p>
        </section>

        <section className="grid">
          <div className="card">
            <h3>Outfit Image</h3>

            <label className="upload">
              <Upload size={28}/>
              <span>Choose image</span>
              <input type="file" accept="image/*" onChange={handleFile}/>
            </label>

            {preview && <img className="preview" src={preview} />}

            <button className="primary" onClick={handleAnalyze}>
              {loading ? "Analyzing..." : "Analyze Outfit"}
            </button>
          </div>

          {result && (
            <div className="card">
              <h3>Outfit Breakdown</h3>

              <OutfitItem title="Topwear" item={result.outfit_breakdown.topwear}/>
              <OutfitItem title="Bottomwear" item={result.outfit_breakdown.bottomwear}/>
              <OutfitItem title="Footwear" item={result.outfit_breakdown.footwear}/>

              <div className="metadata">
                <p><b>Style:</b> {result.fashion_metadata.style}</p>
                <p><b>Occasion:</b> {result.fashion_metadata.occasion}</p>
                <p><b>Season:</b> {result.fashion_metadata.season}</p>
                <p><b>Confidence:</b> {result.confidence_score}%</p>
              </div>
            </div>
          )}
        </section>

        {result && (
          <>
            <section className="card">
              <h3>Shopping Matches</h3>
              <div className="matches">
                {result.shopping_matches.map((m: any, i: number) => (
                  <div className="match" key={i}>
                    <h4>{m.matched_product_name}</h4>
                    <p><b>Detected:</b> {m.detected_item}</p>
                    <p><b>Source:</b> {m.source}</p>
                    <p><b>Price:</b> {m.estimated_price}</p>
                    <p><b>Search:</b> {m.search_query}</p>
                    <span>{m.match_score}% match</span>
                  </div>
                ))}
              </div>
            </section>

            <section className="card">
              <div className="json-header">
                <h3>Structured Output</h3>
                <div>
                  <button onClick={copyJSON}><Copy size={16}/> Copy JSON</button>
                  <button onClick={downloadJSON}><Download size={16}/> Export JSON</button>
                </div>
              </div>

              <pre>{JSON.stringify(result, null, 2)}</pre>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

function OutfitItem({ title, item }: any) {
  return (
    <div className="outfit-item">
      <div>
        <h4>{title}</h4>
        <p>{item.item_name}</p>
      </div>
      <div>
        <span>{item.dominant_color}</span>
        <small>{item.confidence}%</small>
      </div>
    </div>
  );
}