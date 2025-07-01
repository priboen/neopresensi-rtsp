# Neopresensi RTSP

A Flask-based application for real-time RTSP streaming with face detection using YOLOv11 and face registration with embedding extraction using DeepFace (FaceNet512). Integrates with a React Native frontend for face registration.

## Features

- Real-time RTSP streaming with face detection via `/stream/<path:rtsp_url>`.
- Face registration via `/api/register_face` with YOLOv11 for detection and FaceNet512 for embedding extraction.
- JWT authentication for secure API endpoints.
- SQLite database for storing face embeddings.

## Requirements

- Python 3.10 or 3.11
- FFMPEG installed for RTSP streaming
- A YOLOv11 model file (`yolov11n.pt`)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd neopresensi-rtsp
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the `.env` file:

   ```plaintext
   YOLO_MODEL_PATH=/path/to/yolov11n.pt
   RTSP_URL=rtsp://your_camera_url
   RTSP_USERNAME=admin
   RTSP_PASSWORD=password
   DEEPFACE_MODEL=Facenet512
   JWT_SECRET=your-secret-key
   ```

5. Run the Flask server:
   ```bash
   python run.py
   ```

## Usage

- Access the RTSP stream at `http://localhost:5000/` (uses default RTSP_URL from .env).
- Access a specific RTSP stream at `http://localhost:5000/stream/<rtsp_url>?username=<username>&password=<password>`.
- Use the `/api/register_face` endpoint to register faces from a React Native app (send a POST request with a `multipart/form-data` image and optional JWT token).

## Testing

- Test the streaming endpoint with a browser or curl:
  ```bash
  curl http://localhost:5000/stream/rtsp://your_camera_url?username=admin&password=password
  ```
- Test the face registration endpoint with curl:
  ```bash
  curl -X POST -F "image=@/path/to/face.jpg" -H "Authorization: Bearer your-jwt-token" http://localhost:5000/api/register_face
  ```

## Notes

- Ensure FFMPEG is installed for RTSP streaming.
- Replace `your-flask-server-ip` in the React Native app with the actual server IP.
- For GPU support, install `tensorflow-gpu` and configure CUDA/cuDNN.
