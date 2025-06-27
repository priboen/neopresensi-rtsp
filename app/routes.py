from flask import Blueprint, Response, request
from .services.yolo_service import process_rtsp, generate_frames
import threading
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('routes', __name__)

@bp.route('/stream/<path:rtsp_url>')
def stream(rtsp_url):
    username = request.args.get('username')
    password = request.args.get('password')
    
    logger.info(f"Streaming RTSP URL: {rtsp_url}")
    threading.Thread(target=process_rtsp, args=(rtsp_url, username, password), daemon=True).start()
    
    return Response(generate_frames(rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')