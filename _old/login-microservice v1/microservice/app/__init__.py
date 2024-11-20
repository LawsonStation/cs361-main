from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from app.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    JWTManager(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    return app
