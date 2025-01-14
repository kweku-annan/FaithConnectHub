#!/usr/bin/python3
"""Manages User Role and Authentications
TODO 1: User Authentication
        Verifies the identity of a user.
        Involves processes like login, logout, and secure session management.

TODO 2: Role Management
        Assigns roles to users (e.g., Admin, Pastor, Member).
        Controls access to specific features or resources based on the
        user’s role.

TODO 3: Authorization
        Ensures that users can only perform actions or access
        resources permitted for their role.
"""
from email.policy import default
from enum import unique

from sqlalchemy import Column, String, Boolean, DATETIME

from app.models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Model to manage user Authentication and Role"""
    __tablename__ = "users"
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(125), nullable=False)
    username = Column(String(50), unique=True, nullable=True)
    role = Column(String(50), nullable=False, default="Member")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(20), nullable=False)
    last_login = Column(DATETIME, nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DATETIME, nullable=True)
