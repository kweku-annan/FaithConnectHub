#!/usr/bin/env python
"""Main Flask application entry point"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from config import Config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    """Creates and configures the Flask application"""
    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    app.url_map.strict_slashes = False
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.department import department_bp
    from app.routes.group import group_bp
    from app.routes.member import members_bp
    from app.routes.event import events_bp
    from app.routes.attendance import attendance_bp
    from app.routes.finance import finance_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(department_bp, url_prefix="/resources")
    app.register_blueprint(members_bp, url_prefix="/resources")
    app.register_blueprint(group_bp, url_prefix="/resources")
    app.register_blueprint(events_bp, url_prefix="/resources")
    app.register_blueprint(attendance_bp, url_prefix="/resources")
    app.register_blueprint(finance_bp, url_prefix="/resources")



    # Handle 404 errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    # Handle other errors
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to FaithConnectHub! API"}), 200
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Ensures database tables are created
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)