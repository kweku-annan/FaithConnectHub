#!/usr/bin/env python
"""
Handles all user registration and login operations
Contains the registration and authentication endpoints.
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.models import storage

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user
    """
    data = request.get_json()

    # Check for existing user email
    if storage.query(User).filter_by(email=data['email']).first():
        return jsonify({'error': 'User with this email already exists'}), 400

    # Check for existing username
    if storage.query(User).filter_by(username=data['username']).first():
        return jsonify({'error': 'User with this username already exists'}), 400

    if not data['email'] or not data['password'] or not data['username']:
        return jsonify({'error': 'Missing email, password or username'}), 400

    # Create new user
    user = User(
        email=data['email'],
        username=data['username'],
        role=data.get('role', 'Member'),
    )
    user.set_password(data['password'])
    storage.save(user)

    storage.save(user)
    return jsonify({'message': 'User created successfully'}), 201