#!/usr/bin/env python
"""
Handles all user registration and login operations
Contains the registration and authentication endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
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
    user.save()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Logins in user"""
    data = request.get_json()
    user = storage.query(User).filter(
        or_(User.email == data['email'], User.username == data['email'])
    ).first()

    # Validate user credentials
    if user and user.check_password(data['password']):
        access_token = create_access_token({"id": user.id, "role": user.role})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid email/username or password'}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """Protected route that requires authentication"""
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'}), 200