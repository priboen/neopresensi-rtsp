import cv2
import numpy as np
from ultralytics import YOLO
import logging
from ..config import Config
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate model path
if not os.path.exists(Config.YOLO_MODEL_PATH):
    logger.error(f"YOLO model file not found at: {Config.YOLO_MODEL_PATH}")
    raise FileNotFoundError(f"YOLO model file not found at: {Config.YOLO_MODEL_PATH}")

# Initialize YOLO model
logger.info(f"Loading YOLO model from: {Config.YOLO_MODEL_PATH}")
model = YOLO(Config.YOLO_MODEL_PATH)

def process_rtsp(rtsp_url, username=None, password=None):
    # Construct RTSP URL with credentials
    final_rtsp_url = rtsp_url
    if username and password:
        final_rtsp_url = rtsp_url.replace("rtsp://", f"rtsp://{username}:{password}@")
    elif Config.DEFAULT_RTSP_USERNAME and Config.DEFAULT_RTSP_PASSWORD:
        logger.info("Using default RTSP credentials from .env")
        final_rtsp_url = rtsp_url.replace("rtsp://", f"rtsp://{Config.DEFAULT_RTSP_USERNAME}:{Config.DEFAULT_RTSP_PASSWORD}@")
    
    logger.info(f"Opening RTSP stream: {final_rtsp_url}")
    cap = cv2.VideoCapture(final_rtsp_url, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        logger.error(f"Failed to open RTSP stream: {final_rtsp_url}")
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "RTSP Stream Failed", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.warning(f"Failed to grab frame from {final_rtsp_url}")
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Stream Unavailable", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()

        # Process frame with YOLO
        try:
            results = model(frame, conf=0.5)
            annotated_frame = results[0].plot()
        except Exception as e:
            logger.error(f"YOLO processing error: {e}")
            annotated_frame = frame

        # Encode to JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ret:
            logger.error("Failed to encode frame to JPEG")
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
        logger.info(f"RTSP stream closed: {final_rtsp_url}")

def generate_frames(rtsp_url, username=None, password=None):
    return process_rtsp(rtsp_url, username, password)