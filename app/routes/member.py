#!/usr/bin/python3
"""Defines RBAC for Members table based on users roles"""
from flask import jsonify, request, Blueprint
from app.models.member import Member
from app.models import storage
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_helper import role_required
from marshmallow import ValidationError
from app.schemas.member_schema import MemberSchema

members_bp = Blueprint('members', __name__)

# Admin & Pastor: Get all members
@members_bp.route('/members', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_all_members():
    """Retrieves all members"""
    members = storage.all(Member)
    return jsonify([member.to_dict() for member in members]), 200

# Admin & Pastor: Create a new member
@members_bp.route('/members', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def create_member():
    """Creates a new member"""
    data = request.get_json()
    schema = MemberSchema()

    try:
        # Validate request data using schema
        member = schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    member = Member(**data)
    member.save()
    return jsonify(member.to_dict()), 201


# Member: View or update their own  profile
@members_bp.route('/members/<int:member_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
@role_required(['MEMBER', 'ADMIN', 'PASTOR'])
def manage_member(member_id):
        """Manages a member's profile"""
        current_user = get_jwt_identity()

        # Ensure member can only manage their own profile
        if current_user['role'] == 'MEMBER' and current_user['id'] != member_id:
            return jsonify({"error": "Access forbidden: you can only manage your own profile"}), 403

        # Handle profile view logic here
        if request.method == 'GET':
            member = storage.get(Member, member_id)
            if not member:
                return jsonify({"error": "Member not found"}), 404
            return jsonify(member.to_dict()), 200

        if request.method == 'PUT':
            # Handle profile update logic here
            data = request.get_json()
            schema = MemberSchema(partial=True)  # Allow partial updates
            try:
                # Validate request data using schema
                member = schema.load(data)
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400

            # Update member details
            for key, value in member.items():
                setattr(member, key, value)
            member.save()
            return jsonify(member.to_dict()), 200

        if request.method == 'DELETE':
            # Handle profile deletion logic here
            member = storage.get(Member, member_id)
            if not member:
                return jsonify({"error": "Member not found"}), 404
            storage.delete(member)
            storage.save()
            return jsonify({"message": "Member deleted successfully"}), 200

