from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_login import LoginManager
import os
from app.extensions import db
from app.models.user import User
from app import models
from flask import Flask
from .routes import main


migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__, static_folder='../static')
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///transport.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret-key-placeholder')
    
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)

    # Import models here to avoid circular imports
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.routes.fuel_requests import fuelrequest_bp
    app.register_blueprint(fuelrequest_bp, url_prefix='/fuel')

    from app.routes.loader_routes import loader_bp
    app.register_blueprint(loader_bp, url_prefix='/loader')
    
    from app.routes.vehicle import vehicle_bp
    app.register_blueprint(vehicle_bp, url_prefix='/api/vehicle')

    
    from app.routes.approver_routes import approver_bp
    app.register_blueprint(approver_bp, url_prefix='/approver')

    app.register_blueprint(main)
    return app
