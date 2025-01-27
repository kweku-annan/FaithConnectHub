#!/usr/bin/python3
"""Configuration for the FaithConnect Hub Project.

This file typically contains configuration variables and settings required 
for the project. Examples include:

1. Database connection details (e.g., host, port, username, and password).
2. API keys for third-party services.
3. Application-specific settings, such as debug flags or feature toggles.
4. Constants and metadata used across the project.

Customize the placeholders below as needed:
- Add database connection settings.
- Include credentials and secrets as environment variables for security.
- Define any other settings specific to the FaithConnect Hub Project.

"""
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Database Configuration
    user = os.getenv("FaithConnectHub_USER")
    pwd = os.getenv("FaithConnectHub_PWD")
    host = os.getenv("FaithConnectHub_HOST")
    db = os.getenv("FaithConnectHub_DB")

    # Database connection string
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-specific settings
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 28800  # 8 hour
    DEBUG = True
