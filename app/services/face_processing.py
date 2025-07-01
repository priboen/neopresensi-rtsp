import cv2
import numpy as np
from ultralytics import YOLO
from deepface import DeepFace  # type: ignore
import logging
import requests
from datetime import datetime
from ..config.config import Config
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.makedirs(Config.CROPS_OUTPUT_DIR, exist_ok=True)


# Validate YOLO model path
logger.info(f"Loading YOLO model from: {Config.YOLO_MODEL_PATH}")
if not os.path.exists(Config.YOLO_MODEL_PATH):
    logger.error(f"YOLO model file not found at: {Config.YOLO_MODEL_PATH}")
    raise FileNotFoundError(f"YOLO model file not found at: {Config.YOLO_MODEL_PATH}")

yolo_model = YOLO(Config.YOLO_MODEL_PATH)

# Valid DeepFace model names
VALID_DEEPFACE_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'SFace']

def process_face_image(image_file, user_id=None, token=None):
    try:
        # Validate DeepFace model
        if Config.DEEPFACE_MODEL not in VALID_DEEPFACE_MODELS:
            logger.error(f"Invalid DeepFace model name: {Config.DEEPFACE_MODEL}. Valid options: {VALID_DEEPFACE_MODELS}")
            return {"status": "error", "message": f"Invalid DeepFace model name: {Config.DEEPFACE_MODEL}"}

        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("Failed to decode image")
            return {"status": "error", "message": "Failed to decode image"}

        # Detect faces with YOLO
        results = yolo_model(image, conf=0.5)
        faces = []
        for result in results:
            for box in result.boxes:
                if box.cls == 0:  # Assuming class 0 is face
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    # Ensure bounding box is within image dimensions
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)
                    face_crop = image[y1:y2, x1:x2]
                    if face_crop.size == 0:
                        logger.warning("Empty face crop detected")
                        continue
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = f"crop_{user_id or 'anon'}_{ts}.jpg"
                    out_path = os.path.join(Config.CROPS_OUTPUT_DIR, fname)
                    cv2.imwrite(out_path, face_crop)
                    logger.info(f"Cropped face saved to: {out_path}")
                    faces.append({"bbox": [x1, y1, x2, y2]})
                    break  # Process only the first face
            if faces:  # Stop after finding the first face
                break

        if not faces:
            return {"status": "error", "message": "No faces detected"}

        # Process only the first face
        first_face = faces[0]
        face_crop = image[first_face["bbox"][1]:first_face["bbox"][3], first_face["bbox"][0]:first_face["bbox"][2]]
        try:
            face_crop_bgr = image[y1:y2, x1:x2]
            face_crop = cv2.cvtColor(face_crop_bgr, cv2.COLOR_BGR2RGB)
            rep = DeepFace.represent(
                face_crop,
                model_name=Config.DEEPFACE_MODEL,
                detector_backend='skip',      # SKIP agar tak deteksi lagi
                enforce_detection=False
            )
            if not rep:
                logger.error("❌ DeepFace.represent tidak mengembalikan embedding")
                return {"status":"error","message":"Failed to extract embedding"}
            embedding = rep[0]["embedding"]
            logger.info(f"Sample embedding: {embedding[:5]}…")
            first_face["embedding"] = embedding
        except Exception as e:
            logger.error(f"Failed to extract embedding with DeepFace: {e}")
            return {"status": "error", "message": f"Failed to extract face embedding: {str(e)}"}
        # Send embedding to NestJS if user_id and token are provided
        if user_id and token:
            try:
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                # Convert embedding array to comma-separated string
                payload = {"face_embedding": embedding}
                response = requests.patch(
                    "http://192.168.1.5:4000/api/face-embedding",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                nest_json = response.json()
                logger.info(f"Successfully sent embedding to NestJS: {nest_json}")
                # Kembalikan juga jawaban dari NestJS
                return {
                    "status": "success",
                    "faces": [first_face],
                    "nest_response": nest_json
                }
            except requests.RequestException as e:
                logger.error(f"Failed to send embedding to NestJS: {e}")
                return {"status": "error", "message": f"Failed to send embedding to NestJS: {str(e)}"}

        return {"status": "success", "faces": [first_face], "message": "Detected 1 face"}
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return {"status": "error", "message": str(e)}