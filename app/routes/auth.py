#!/usr/bin/env python
"""
Handles all user registration and login operations
Contains the registration and authentication endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.services.auth_service import AuthService
from app.utils.role_helper import role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user
    """
    data = request.get_json()

    # Validate input
    schema = RegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Call service to handle registration
    user = AuthService.register_user(data)
    if not user:
        return jsonify({"message": "User with this email or username already exists"}), 400

    user_dict = user[0].to_dict()
    username, email, role = user_dict['username'], user_dict['email'], user_dict['role']

    return jsonify({"Message": "Registered Successfully! Here are your details:", "username": username,
                    "email": email, "role": role}), 201


# User Login Endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    """Logins in user"""
    data = request.get_json()

    # Validate input
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Authenticate user
    token = AuthService.authenticate_user(data)
    if not token:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"access_token": token}), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
@role_required(["ADMIN", "PASTOR", "MEMBER"])
def protected():
    """Protected route that requires authentication"""
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user['role']}! This is a restricted resource.'}), 200

