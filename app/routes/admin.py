#!/usr/bin/python3
"""Defines RBAC for Users table"""
from flask import jsonify, request, Blueprint
from app.models.user import User
from app.models import storage
from flask_jwt_extended import jwt_required
from app.utils.role_helper import role_required

admin_bp = Blueprint('admin', __name__)

# Admin-only: Get all users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(['ADMIN'])
def get_all_users():
    """Retrieves all users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users]), 200

# Admin-only: Create a new user
@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_user():
    """Creates a new user"""
    data = request.get_json()
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

# Admin & Pastor: View a single user
@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_user(user_id):
    """Retrieves a single user"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200