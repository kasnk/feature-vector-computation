# Video Frame Search with FastAPI & Qdrant

A smart video frame retrieval system that allows you to:
- Upload videos
- Extract frames at fixed intervals
- Compute feature vectors using color histograms
- Store vectors in **Qdrant (Cloud Vector DB)**
- Search for similar frames using an image query

---

## Folder Structure

├── main.py
├── .env 
├── requirements.txt 
├── uploaded_videos/ 
├── frames/
├── temp/ 
---

## Features

- Upload a video and extract 1 frame per second using OpenCV
- Compute a 64-dimensional color histogram vector for each frame
- Store vectors in Qdrant Cloud
- Query with any image to find similar frames via cosine similarity
- Test all endpoints in FastAPI Swagger UI

---

## Setup Instructions

1.Clone the repository

git clone https://github.com/yourusername/video-frame-search.git
cd video-frame-search

2.Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  

or
source venv/bin/activate  # macOS/Linux

3.Install dependencies
pip install -r requirements.txt

4.Create .env file
QDRANT_URL=https://your-qdrant-url.qdrant.xyz
QDRANT_API_KEY=your_qdrant_api_key

5.Run the FastAPI server
uvicorn main:app --reload


Go to http://127.0.0.1:8000/docs to test the API.

API Endpoints
Method	Endpoint	Description
POST	/upload-video/	Uploads .mp4 file, extracts & stores vectors
POST	/query-vector/	Uploads image to find similar frames
GET	/get-frame/?path=	Serves a specific frame image

Sample Query Output

{
  "matches": [
    {
      "score": 0.02,
      "image": "frames/frame_bdf12a.jpg"
    },
    {
      "score": 0.03,
      "image": "frames/frame_47ae01.jpg"
    }
  ]
}

You can fetch these images by calling:

GET /get-frame/?path=frames/frame_47ae01.jpg


Tech Stack

FastAPI
Qdrant Cloud
OpenCV
NumPy
Uvicorn
python-dotenv


Author
Shekhar Nipane
Final-year engineering student | Backend & AI Enthusiast
