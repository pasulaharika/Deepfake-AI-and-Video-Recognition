# Deepfake-AI-and-Video-Recognition

## Project overview
Full-stack prototype for AI/human audio and video detection.

- backend: Python FastAPI
- frontend: Bootstrap + vanilla JS
- Storage: local upload folder
- Analysis: placeholder/smoke validation (size-based heuristic), replace with real AI models for production

## Features
- Upload audio file via `/api/upload/audio`
- Upload video file via `/api/upload/video`
- JSON response with mock `prediction` and `confidence`
- Local UI at `frontend/index.html` with file chooser
- CORS enabled for browser-based frontend

---

## Setup (Windows)

### 1) Backend

```powershell
cd d:\workspace\Deepfake-AI-and-Video-Recognition\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

FastAPI docs: http://localhost:8000/docs

### 2) Frontend

Open `d:\workspace\Deepfake-AI-and-Video-Recognition\frontend\index.html` in browser

or run a simple static server:

```powershell
cd d:\workspace\Deepfake-AI-and-Video-Recognition\frontend
python -m http.server 8080
```

then visit `http://localhost:8080`

---

## Usage
1. Select audio or video file
2. Click upload
3. View prediction in JSON results

## Notes
- This work is starter scaffolding; replace `app/services.py` with a real ML model (e.g., HuggingFace for deepfake detection) for production accuracy.
- For higher quality results, install `ffmpeg`, `opencv-python`, and deep learning packages, then implement `analyze_audio` and `analyze_video` pipelines.

## Future improvements
- Real model inference, not heuristic
- Async processing queue (Celery/RQ)
- Database for upload history
- Visual waveform / thumbnail preview
- Enhanced UI/UX (React + progress bars)

