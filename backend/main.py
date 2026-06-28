from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_image
from database import init_db, save_analysis, get_history

app = FastAPI(title="WardroAI Offline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/health")
def health():
    return {
        "status": "offline-ready",
        "runtime": "cpu",
        "database": "sqlite",
        "cloud_apis": "disabled"
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_image(file)
    save_analysis(result)
    return result

@app.get("/history")
def history():
    return get_history()