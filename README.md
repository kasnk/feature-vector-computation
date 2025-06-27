# Feature Vector Computation with FastAPI & Qdrant

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://example.com/build)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A smart video frame retrieval system that allows you to:

- Upload videos
- Extract frames at fixed intervals
- Compute feature vectors using color histograms
- Store vectors in **Qdrant (Cloud Vector DB)**
- Search for similar frames using an image query

## Workflow


├── main.py             
├── .env                
├── requirements.txt    
├── uploaded_videos/    
├── frames/             
├── temp/               

- Upload a video and extract 1 frame per second using OpenCV
- Compute a 64-dimensional color histogram vector for each frame
- Store vectors in Qdrant Cloud
- Query with any image to find similar frames via cosine similarity
- Test all endpoints in FastAPI Swagger UI

---

## Setup Instructions

1.  **Clone the repository**

bash
    python -m venv venv
        > If you face issues during installation, ensure your pip is up to date: `pip install --upgrade pip`

4.  **Create a `.env` file**

    Create a `.env` file in the root directory with the following content:


    QDRANT_URL=https://your-qdrant-url.qdrant.xyz
    QDRANT_API_KEY=your_qdrant_api_key
        > Replace `https://your-qdrant-url.qdrant.xyz` and `your_qdrant_api_key` with your actual Qdrant Cloud URL and API key.

5.  **Run the FastAPI server**

        Go to `http://127.0.0.1:8000/docs` to test the API in Swagger UI.

## API Endpoints

| Method | Endpoint          | Description                                          | Example Request                                                                                                                                                                                          | Example Response                                                                                                                                                                                               |
| :----- | :---------------- | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | `/upload-video/`  | Uploads `.mp4` file, extracts & stores vectors       | `curl -X POST -F "file=@/path/to/your/video.mp4" http://127.0.0.1:8000/upload-video/`                                                                                                                  | `{"message": "Video uploaded and processed successfully"}`                                                                                                                                                   |
| POST   | `/query-vector/`  | Uploads image to find similar frames                | `curl -X POST -F "file=@/path/to/your/image.jpg" http://127.0.0.1:8000/query-vector/`                                                                                                                  | `{"matches": [{"score": 0.02, "image": "frames/frame_bdf12a.jpg"}, {"score": 0.03, "image": "frames/frame_47ae01.jpg"}]}`                                                                               |
| GET    | `/get-frame/?path=` | Serves a specific frame image                      | `curl http://127.0.0.1:8000/get-frame/?path=frames/frame_47ae01.jpg`                                                                                                                                  | (Returns the image file)                                                                                                                                                                                 |

> Ensure the paths in the example requests are adjusted to match your local file paths.

### Sample Query Output

json
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
-   [FastAPI](https://fastapi.tiangolo.com/): Web framework
-   [Qdrant Cloud](https://qdrant.com/): Vector database
-   [OpenCV](https://opencv.org/): Image processing
-   [NumPy](https://numpy.org/): Numerical computing
-   [Uvicorn](https://www.uvicorn.org/): ASGI server
-   [python-dotenv](https://github.com/theskumar/python-dotenv): Environment variable management
-   [Mermaid](https://mermaid.js.org/): Diagram and flowchart generation

## Contributing

> We welcome contributions! Please follow these steps:
>
> 1.  Fork the repository.
> 2.  Create a new branch for your feature or bug fix.
> 3.  Make your changes and commit them with descriptive messages.
> 4.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
