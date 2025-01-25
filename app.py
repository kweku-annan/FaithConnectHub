#!/usr/bin/env python
"""Main Flask application entry point"""
from flask import Flask
from config import Config
from app.routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth_bp, url_prefix="/auth")


if __name__ == "__main__":
    app.run(debug=True)