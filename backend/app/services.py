import os
import cv2
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier


# Pretrained mock model (trained on dummy data for demonstration)
# In production, replace with actual trained model
_mock_model = None


def _get_pretrained_model():
    global _mock_model
    if _mock_model is None:
        # Create dummy training data
        np.random.seed(42)
        n_samples = 1000
        n_features = 26  # 13 mean + 13 std MFCC
        X = np.random.randn(n_samples, n_features)
        y = np.random.choice([0, 1], n_samples)  # 0: Human, 1: AI
        
        _mock_model = RandomForestClassifier(n_estimators=100, random_state=42)
        _mock_model.fit(X, y)
    return _mock_model


def _extract_mfcc_features(file_path: str) -> np.ndarray:
    """Extract MFCC features from audio file."""
    try:
        y, sr = librosa.load(file_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        # Compute statistics: mean and std for each coefficient
        features = np.concatenate([np.mean(mfcc, axis=1), np.std(mfcc, axis=1)])
        return features
    except Exception as e:
        raise ValueError(f"Error processing audio file: {e}")


def _simple_classifier(features: np.ndarray) -> tuple:
    """Use pretrained model for classification."""
    model = _get_pretrained_model()
    probas = model.predict_proba([features])[0]
    prediction_idx = np.argmax(probas)
    confidence = float(probas[prediction_idx])
    prediction = "AI-generated" if prediction_idx == 1 else "Human"
    return prediction, confidence


def analyze_audio(file_path: str) -> dict:
    """Analyze uploaded audio using MFCC features and pretrained classifier."""
    try:
        features = _extract_mfcc_features(file_path)
        prediction, confidence = _simple_classifier(features)
        return {
            "prediction": prediction,
            "confidence": round(float(confidence), 2),
            "notes": "Analysis based on MFCC features extraction using librosa and RandomForest classifier.",
            "type": "audio",
            "file_path": file_path,
        }
    except ValueError as e:
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "notes": str(e),
            "type": "audio",
            "file_path": file_path,
        }


def _extract_frames(video_path: str, frame_interval: int = 30) -> list:
    """Extract frames from video at specified intervals."""
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frames.append(frame)
        frame_count += 1
    cap.release()
    return frames


def _detect_faces(frame: np.ndarray) -> list:
    """Detect faces in a frame using OpenCV Haar cascades."""
    # Load the pre-trained Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces  # list of (x, y, w, h)


def _deepfake_detection_placeholder(face_roi: np.ndarray) -> float:
    """Placeholder deepfake detection model - simple heuristic based on face brightness."""
    # Simple heuristic: calculate average brightness of the face region
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_face)
    # Normalize to 0-1, higher brightness might indicate 'AI' (arbitrary)
    score = min(avg_brightness / 255.0, 1.0)
    return score


def _aggregate_results(face_scores: list) -> tuple:
    """Aggregate detection results across all faces in the video."""
    if not face_scores:
        return "No faces detected", 0.0
    
    avg_score = np.mean(face_scores)
    prediction = "AI-generated" if avg_score > 0.5 else "Human"
    confidence = max(avg_score, 1 - avg_score)
    return prediction, confidence


def analyze_video(file_path: str) -> dict:
    """Analyze uploaded video for deepfake detection."""
    try:
        # Step 1: Extract frames from the video
        frames = _extract_frames(file_path, frame_interval=30)  # Extract every 30th frame
        
        face_scores = []
        for frame in frames:
            # Step 2: Detect faces in the frame
            faces = _detect_faces(frame)
            
            for (x, y, w, h) in faces:
                # Extract face region of interest (ROI)
                face_roi = frame[y:y+h, x:x+w]
                
                # Step 3: Run placeholder deepfake detection on the face
                score = _deepfake_detection_placeholder(face_roi)
                face_scores.append(score)
        
        # Step 4: Aggregate results across frames
        prediction, confidence = _aggregate_results(face_scores)
        
        # Step 5: Return final prediction with confidence
        return {
            "prediction": prediction,
            "confidence": round(float(confidence), 2),
            "notes": f"Analyzed {len(frames)} frames, detected {len(face_scores)} faces.",
            "type": "video",
            "file_path": file_path,
        }
    except Exception as e:
        return {
            "prediction": "Error",
            "confidence": 0.0,
            "notes": str(e),
            "type": "video",
            "file_path": file_path,
        }
