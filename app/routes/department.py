#!/usr/bin/python3
"""Defines RBAC for Department table"""
from flask import jsonify, request, Blueprint
from app.models.department import Department
from app.models import storage
from flask_jwt_extended import jwt_required

from app.models.group import Group
from app.models.member import Member
from app.utils.role_helper import role_required

department_bp = Blueprint('departments', __name__)

# Admin, Pastor & Members: Get all departments
@department_bp.route('/departments', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR', 'MEMBER'])
def get_all_departments():
    """Retrieves all departments"""
    departments = storage.all(Department)
    return jsonify([department.to_dict() for department in departments]), 200

# Admin & Pastor: Create a new department
@department_bp.route('/departments', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def create_department():
    """Creates a new department"""
    data = request.get_json()
    department = Department(**data)
    department.save()
    return jsonify(department.to_dict()), 201

# Admin & Pastor: View a single department
@department_bp.route('/departments/<string:department_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR', 'MEMBER'])
def get_department(department_id):
    """Retrieves a single department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(department.to_dict()), 200

# Admin & Pastor: Update a department
@department_bp.route('/departments/<string:department_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN'])
def update_department(department_id):
    """Updates a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(department, key, value)
    department.save()
    return jsonify(department.to_dict()), 200

# Admin: Delete a department
@department_bp.route('/departments/<string:department_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def delete_department(department_id):
    """Deletes a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    storage.delete(department)
    storage.save()
    return jsonify({}), 204

# Admin & Pastor: Get all members in a department
@department_bp.route('/departments/<string:department_id>/members', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_department_members(department_id):
    """Retrieves all members in a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify([member.to_dict() for member in department.members]), 200

# Admin & Pastor: Add a member to a department
@department_bp.route('/departments/<string:department_id>/members', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def add_member_to_department(department_id):
    """Adds a member to a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    data = request.get_json()
    member = storage.get(Member, data['member_id'])
    if not member:
        return jsonify({"error": "Member not found"}), 404
    department.members.append(member)
    department.save()
    return jsonify(department.to_dict()), 201

# Admin & Pastor: Remove a member from a department
@department_bp.route('/departments/<string:department_id>/members/<string:member_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def remove_member_from_department(department_id, member_id):
    """Removes a member from a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    member = storage.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    department.members.delete(member)
    department.save()
    return jsonify({}), 204

# Admin: Register a group for a department
@department_bp.route('/departments/<string:department_id>/groups', methods=['POST'])
@jwt_required()
@role_required(['ADMIN'])
def register_group_for_department(department_id):
    """Registers a group for a department"""
    department = storage.get(Department , department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    data = request.get_json()
    group = storage.get(Group, data['group_id'])
    if not group:
        return jsonify({"error": "Group not found"}), 404
    department.group.append(group)
    department.save()
    return jsonify(department.to_dict()), 201

# Admin: Unregister a group from a department
@department_bp.route('/departments/<string:department_id>/groups/<string:group_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN'])
def unregister_group_from_department(department_id, group_id):
    """Unregisters a group from a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    department.group.delete(group)
    department.save()
    return jsonify({}), 204

# Admin & Pastor: Get all groups in a department
@department_bp.route('/departments/<string:department_id>/groups', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_department_groups(department_id):
    """Retrieves all groups in a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify([group.to_dict() for group in department.group]), 200

# Admin & Pastor: Get all members in a group in a department
@department_bp.route('/departments/<string:department_id>/groups/<string:group_id>/members', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_department_group_members(department_id, group_id):
    """Retrieves all members in a group in a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    return jsonify([member.to_dict() for member in group.members]), 200

# Admin & Pastor: Add a member to a group in a department
@department_bp.route('/departments/<string:department_id>/groups/<string:group_id>/members', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def add_member_to_group_in_department(department_id, group_id):
    """Adds a member to a group in a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    data = request.get_json()
    member = storage.get(Member, data['member_id'])
    if not member:
        return jsonify({"error": "Member not found"}), 404
    group.members.append(member)
    group.save()
    return jsonify(group.to_dict()), 201

# Admin & Pastor: Remove a member from a group in a department
@department_bp.route(
    '/departments/<string:department_id>/groups/<string:group_id>/members/<string:member_id>', methods=['DELETE']
)
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def remove_member_from_group_in_department(department_id, group_id, member_id):
    """Removes a member from a group in a department"""
    department = storage.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404

    group = storage.get(Group, group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404
    member = storage.get(Member, member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    group.members.delete(member)
    group.save()

    return jsonify({group.to_dict()}), 204




