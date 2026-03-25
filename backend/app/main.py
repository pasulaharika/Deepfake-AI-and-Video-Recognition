from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
import shutil

from app.services import analyze_audio, analyze_video

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "uploads"
STORAGE_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Audio/Video Human vs AI Recognition",
    version="0.1.0",
    description="Simple backend skeleton for audio/video human vs AI detection",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _save_upload(upload_file: UploadFile, dest_dir: Path) -> str:
    file_ext = Path(upload_file.filename).suffix or ""
    safe_name = f"{uuid.uuid4().hex}{file_ext}"
    dest_path = dest_dir / safe_name

    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    upload_file.file.close()
    return str(dest_path)


@app.post("/api/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    dest_path = _save_upload(file, STORAGE_DIR)
    result = analyze_audio(dest_path)
    return JSONResponse(content={"success": True, "file": file.filename, "result": result})


@app.post("/api/upload/video")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    dest_path = _save_upload(file, STORAGE_DIR)
    result = analyze_video(dest_path)
    return JSONResponse(content={"success": True, "file": file.filename, "result": result})


@app.get("/api/ping")
async def ping():
    return {"success": True, "message": "pong"}
