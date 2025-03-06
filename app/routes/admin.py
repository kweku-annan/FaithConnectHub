#!/usr/bin/python3
"""Defines RBAC for Users table"""
from flask import jsonify, request, Blueprint
from marshmallow import ValidationError

from app.models.user import User
from app.models import storage
from flask_jwt_extended import jwt_required


from app.services.auth_service import AuthService
from app.utils.role_helper import role_required
from app.schemas.auth_schema import RegisterSchema

admin_bp = Blueprint('resources', __name__)

# Admin-only: Get all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['ADMIN'])
def get_all_users():
    """Retrieves all users"""
    users = storage.all(User)
    all_users = [users[user].to_dict() for user in users]
    for user in all_users:
        del user['password']
        del user['__class__']
    return jsonify(all_users), 200

# Admin-only: Create a new user
@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_user():
    """Creates a new user"""
    data = request.get_json()

    # Validate input
    schema = RegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = AuthService.register_user(data)

    if not user:
        return jsonify({"message": "User with this email or username already exists"}), 400

    user_dict = user[0].to_dict()
    username, email, role, id = user_dict['username'], user_dict['email'], user_dict['role'], user_dict['id']
    return jsonify({"Message": "Registered Successfully! Here are your details:", "username": username, "id": id,
                    "email": email, "role": role}), 201

# Admin & Pastor: View a single user
@admin_bp.route('/users/<string:user_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_user(user_id):
    """Retrieves a single user"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    del user.password
    return jsonify(user.to_dict()), 200

# Admin & Pastor: Update a user
@admin_bp.route('/users/<string:user_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_user(user_id):
    """Updates a user"""
    data = request.get_json()
    schema = RegisterSchema(partial=True) # Allow partial updates

    try:
        # Validate request data using schema
        validated_data = schema.load(data)
        user = storage.get(User, user_id)

        # Update user details
        for key, value in validated_data.items():
            setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

# Admin & Pastor: Delete a user
@admin_bp.route('/users/<string:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def delete_user(user_id):
    """Deletes a user"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.delete()
    return jsonify({}), 204

