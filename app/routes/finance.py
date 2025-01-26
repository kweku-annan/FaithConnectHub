#!/usr/bin/python3
"""Defines routes for managing finance and BRAC for finance based on user roles"""
from flask import jsonify, request, Blueprint
from app.models.finance import FinancialRecord
from app.models import storage
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_helper import role_required

finance_bp = Blueprint('finance', __name__)

# Admin & Pastor: Create a financial record
@finance_bp.route('/finance', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def create_financial_record():
    data = request.get_json()
    record = FinancialRecord(**data)
    record.save()
    return jsonify(record.to_dict()), 201

# Admin & Pastor: View all financial records
@finance_bp.route('/finance', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_all_financial_records():
    records = storage.all(FinancialRecord)
    return jsonify([record.to_dict() for record in records]), 200

# Admin & Pastor: View a single financial record
@finance_bp.route('/finance/<int:record_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def get_financial_record(record_id):
    record = storage.get(FinancialRecord, record_id)
    if not record:
        return jsonify({"error": "Financial record not found"}), 404
    return jsonify(record.to_dict()), 200

# Admin & Pastor: Update a financial record
@finance_bp.route('/finance/<int:record_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def update_financial_record(record_id):
    record = storage.get(FinancialRecord, record_id)
    if not record:
        return jsonify({"error": "Financial record not found "}), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(record, key, value)

    record.save()
    return jsonify(record.to_dict()), 200

# Admin & Pastor: Delete a financial record
@finance_bp.route('/finance/<int:record_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def delete_financial_record(record_id):
    record = storage.get(FinancialRecord, record_id)
    if not record:
        return jsonify({"error": "Financial record not found"}), 404
    record.delete()
    return jsonify({"message": "Financial record deleted successfully"}), 200

