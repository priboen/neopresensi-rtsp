from flask import Blueprint, Response, request, render_template, jsonify
from .services.yolo_service import process_rtsp, generate_frames
from .services.face_processing import process_face_image
from .config.config import Config
import threading
import logging
import jwt

logger = logging.getLogger(__name__)
bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html', config=Config)

@bp.route('/stream/<path:rtsp_url>')
def stream(rtsp_url):
    username = request.args.get('username')
    password = request.args.get('password')
    
    logger.info(f"Streaming RTSP URL: {rtsp_url}")
    threading.Thread(target=process_rtsp, args=(rtsp_url, username, password), daemon=True).start()
    
    return Response(generate_frames(rtsp_url, username, password), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/api/register-face', methods=['POST'])
def register_face():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"status": "error", "message": "Authorization token required"}), 401

    token = auth_header.split(" ", 1)[1]
    try:
        decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        user_id = decoded.get('uuid')
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid or expired token: {e}")
        return jsonify({"status": "error", "message": "Invalid or expired token"}), 401

    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image provided"}), 400

    image_file = request.files['image']
    result = process_face_image(image_file, user_id=user_id, token=token)

    # Jika terjadi error di DeepFace/YOLO
    if result["status"] == "error":
        return jsonify({"status": "error", "message": result["message"]}), 400

    # Jika sukses, butuh proxy pesan dari NestJS
    nest = result.get("nest_response", {})
    message = nest.get("message", "Face embedding updated successfully")
    faces   = result.get("faces", [])
    data    = nest.get("data", None)


    return jsonify({
        "status": "success",
        "message": message,
        "faces": faces,
        "data": data
    }), 200
    