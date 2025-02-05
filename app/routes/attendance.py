#!/usr/bin/python3
"""Defines RBAC for Attendance table"""
from flask import jsonify, request, Blueprint
from app.models.attendance import Attendance
from app.models import storage
from flask_jwt_extended import jwt_required

from app.models.event import Event
from app.models.member import Member
from app.utils.role_helper import role_required

attendance_bp = Blueprint('attendance', __name__)

# Admin & Pastor: Get all attendance records
@attendance_bp.route('/attendance', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_all_attendance():
    """Retrieves all attendance records"""
    attendance_records = storage.all(Attendance)
    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Create a new attendance record
@attendance_bp.route('/attendance', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def create_attendance():
    """Creates a new attendance record"""
    data = request.get_json()

    event = storage.get(Event, data['event_id'])
    if not event:
        return jsonify({"error": "Event not found"}), 404

    member = storage.get(Member, data['member_id'])
    if not member:
        return jsonify({"error": "Member not found"}), 404

    # Validate attendance status
    if data['status'] not in ['PRESENT', 'ABSENT']:
        return jsonify({"error": "Invalid attendance status"}), 400

    # Check if attendance record already exists
    if storage.query(Attendance).filter_by(event_id=data['event_id'], member_id=data['member_id']).first():
        return jsonify({"error": "Attendance record already exists"}), 400

    # Create a new Attendance record
    attendance = Attendance(**data)
    attendance.save()
    return jsonify(attendance.to_dict()), 201

# Admin & Pastor: View a single attendance record
@attendance_bp.route('/attendance/<string:attendance_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance(attendance_id):
    """Retrieves a single attendance record"""
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    return jsonify(attendance.to_dict()), 200

# Admin & Pastor: Update an attendance record
@attendance_bp.route('/attendance/<string:attendance_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def update_attendance(attendance_id):
    """Updates an attendance record"""
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(attendance, key, value)

    attendance.save()
    return jsonify(attendance.to_dict()), 200

# Admin & Pastor: Delete an attendance record
@attendance_bp.route('/attendance/<string:attendance_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def delete_attendance(attendance_id):
    """Deletes an attendance record"""
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    attendance.delete()
    return jsonify({}), 204

# Admin & Pastor: Get all attendance records for a specific event
@attendance_bp.route('/attendance/event/<string:event_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_event(event_id):
    """Retrieves all attendance records for a specific event"""
    attendance_records = storage.query(Attendance).filter_by(event_id=event_id).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific member
@attendance_bp.route('/attendance/member/<string:member_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_member(member_id):
    """Retrieves all attendance records for a specific member"""
    attendance_records = storage.query(Attendance).filter_by(member_id=member_id).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific date range
@attendance_bp.route('/attendance/date', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_date():
    """Retrieves all attendance records for a specific date range"""
    data = request.get_json()
    attendance_records = storage.query(Attendance).filter(Attendance.date.between(data['start_date'], data['end_date'])).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific date range and event
@attendance_bp.route('/attendance/date/event', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_date_and_event():
    """Retrieves all attendance records for a specific date range and event"""
    data = request.get_json()
    attendance_records = storage.query(Attendance).filter(Attendance.date.between(data['start_date'], data['end_date']),
                                                          Attendance.event_id == data['event_id']).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific date range and member
@attendance_bp.route('/attendance/date/member', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_date_and_member():
    """Retrieves all attendance records for a specific date range and member"""
    data = request.get_json()

    attendance_records = storage.query(Attendance).filter(Attendance.date.between(data['start_date'], data['end_date']),
                                                          Attendance.member_id == data['member_id']).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404
    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific date range, event, and member
@attendance_bp.route('/attendance/date/event/member', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_date_event_and_member():
    """Retrieves all attendance records for a specific date range, event, and member"""
    data = request.get_json()

    attendance_records = storage.query(Attendance).filter(Attendance.date.between(data['start_date'], data['end_date']),
                                                          Attendance.event_id == data['event_id'],
                                                          Attendance.member_id == data['member_id']).all()
    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404
    return jsonify([record.to_dict() for record in attendance_records]), 200

# Admin & Pastor: Get all attendance records for a specific date range, event, and member with a specific status
@attendance_bp.route('/attendance/date/event/member/status', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_attendance_by_date_event_and_member_with_status():
    """Retrieve all attendance records for a specific date range, event, and member with a specific status"""
    data = request.get_json()

    attendance_records = storage.query(Attendance).filter(Attendance.date.between(data['start_date'], data['end_date']),
                                                          Attendance.event_id == data['event_id'],
                                                          Attendance.member_id == data['member_id'],
                                                          Attendance.status == data['status']).all()

    if not attendance_records:
        return jsonify({"error": "No attendance records found"}), 404

    return jsonify([record.to_dict() for record in attendance_records]), 200


