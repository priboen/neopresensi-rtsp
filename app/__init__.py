from flask import Flask
from flask_cors import CORS
from .config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS
    CORS(app, resources={r"/stream/*": {"origins": Config.CORS_ORIGINS}})
    
    # Register blueprints
    from .routes import bp
    app.register_blueprint(bp)

    return app