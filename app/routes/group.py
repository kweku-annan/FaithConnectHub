#!/usr/bin/python3
"""Defines RBAC for Groups table"""
from flask import jsonify, request, Blueprint
from app.models.group import Group
from app.models import storage
from flask_jwt_extended import jwt_required

from app.models.member import Member
from app.utils.role_helper import role_required

group_bp = Blueprint('group', __name__)

# Admin & Pastor: Get all groups
@group_bp.route('/groups', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_all_groups():
    """Retrieves all groups"""
    groups = storage.all(Group)
    return jsonify([group.to_dict() for group in groups]), 200

# Admin: Create a new group
@group_bp.route('/groups', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_group():
    """Creates a new group"""
    data = request.get_json()
    group = Group(**data)
    group.save()
    return jsonify(group.to_dict()), 201

# Admin & Pastor: View a single group
@group_bp.route('/groups/<string:group_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_group(group_id):
    """Retrieves a single group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    return jsonify(group.to_dict()), 200

# Admin & Pastor: Update a group
@group_bp.route('/groups/<string:group_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_group(group_id):
    """Updates a group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(group, key, value)
    group.save()
    return jsonify(group.to_dict()), 200

# Admin: Delete a group
@group_bp.route('/groups/<string:group_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def delete_group(group_id):
    """Deletes a group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    storage.delete(group)
    storage.save()

    return jsonify({group.to_dict}), 200

# Admin & Pastor: Add a member to a group
@group_bp.route('/groups/<string:group_id>/users/<string:member_id>', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def add_member_to_group(group_id, member_id):
    """Adds a member to a group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    user = storage.get(Member, member_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    group.members.append(user)
    group.save()
    return jsonify(group.to_dict()), 200

# Admin & Pastor: Remove a member from a group
@group_bp.route('/groups/<string:group_id>/users/<string:member_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def remove_member_from_group(group_id, member_id):
    """Removes a member from a group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    user = storage.get(Member, member_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    group.members.remove(user)
    group.save()
    return jsonify({}), 200

# Admin & Pastor: Get all members in a group
@group_bp.route('/groups/<string:group_id>/users', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_group_members(group_id):
    """Retrieves all members in a group"""
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    return jsonify([member.to_dict() for member in group.members]), 200

