from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
import cv2
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Directories
VIDEO_DIR = "uploaded_videos"
FRAME_DIR = "frames"
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

# Qdrant Setup for Cloud
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
COLLECTION_NAME = "video_frames"

qdrant_client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=64, distance=Distance.COSINE)
)

# Util: Extract frames at 1-second interval
def extract_frames(video_path, interval_sec=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    frame_count = 0
    extracted = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            filename = f"frame_{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(FRAME_DIR, filename)
            cv2.imwrite(filepath, frame)
            extracted.append(filepath)
        frame_count += 1

    cap.release()
    return extracted

# Util: Feature vector (simple color histogram)
def compute_feature_vector(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (64, 64))
    hist = cv2.calcHist([img], [0, 1, 2], None, [4, 4, 4], [0, 256]*3)
    return cv2.normalize(hist, hist).flatten().astype(np.float32).tolist()

@app.post("/upload-video/")
def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 files are supported.")

    video_path = os.path.join(VIDEO_DIR, file.filename)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frames = extract_frames(video_path)
    points = []
    for frame_path in frames:
        vec = compute_feature_vector(frame_path)
        points.append(PointStruct(id=uuid.uuid4().int >> 64, vector=vec, payload={"path": frame_path}))

    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
    return {"frames_extracted": len(frames)}

@app.post("/query-vector/")
def query_similar_frames(file: UploadFile = File(...)):
    try:
        temp_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Image saved to {temp_path}")

        vec = compute_feature_vector(temp_path)
        print(f"Computed vector (length: {len(vec)})")

        results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vec,
            limit=5
        )

        os.remove(temp_path)

        matches = [
            {"score": float(hit.score), "image": hit.payload["path"]} for hit in results
        ]
        print("Search successful")
        return {"matches": matches}
    
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-frame/")
def get_frame(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Image not found")
