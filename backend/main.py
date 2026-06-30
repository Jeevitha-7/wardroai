from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

try:
    from .analyzer import analyze_image
    from .database import get_analysis_by_id, get_history, init_db, save_analysis
except ImportError:  # pragma: no cover - supports `cd backend && uvicorn main:app`
    from analyzer import analyze_image
    from database import get_analysis_by_id, get_history, init_db, save_analysis

app = FastAPI(title="WardroAI Offline API")
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"

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
    try:
        result = await analyze_image(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    save_analysis(result)
    return result

@app.get("/history")
def history():
    return get_history()


@app.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str):
    return get_analysis_by_id(analysis_id)


if (FRONTEND_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


@app.get("/{full_path:path}")
def serve_frontend(full_path: str):
    index_file = FRONTEND_DIST / "index.html"
    requested_file = FRONTEND_DIST / full_path

    if requested_file.is_file():
        return FileResponse(requested_file)
    if index_file.exists():
        return FileResponse(index_file)

    raise HTTPException(
        status_code=404,
        detail="Frontend build not found. Run `npm run build` before `npm start`.",
    )
