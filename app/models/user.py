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
from app.models.base_model import BaseModel


class User(BaseModel):
    """Model to manage user Authentication and Role"""
    email = ""
    password_hash = ""
    username = ""
    role = ""
    is_active = True
    is_verified = False
    first_name = ""
    last_name = ""
    phone_number = ""