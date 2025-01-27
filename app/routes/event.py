#!/usr/bin/python3
"""Defines routes for managing events and BRAC for events based on user roles"""
from flask import jsonify, request, Blueprint
from app.models.event import Event
from app.models import storage
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role_helper import role_required

events_bp = Blueprint('events', __name__)

# Admin & Pastor: Create an event
@events_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def create_event():
    data = request.get_json()
    event = Event(**data)
    event.save()
    return jsonify(event.to_dict()), 201

# All roles: View all events
@events_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR', 'MEMBER'])
def get_all_events():
    events = storage.all(Event)
    return jsonify([event.to_dict() for event in events]), 200

# All roles: View a single event
@events_bp.route('/events/<int:event_id>', methods=['GET'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR', 'MEMBER'])
def get_event(event_id):
    event = storage.get(Event, event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify(event.to_dict()), 200

# Admin & Pastor: Update an event
@events_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def update_event(event_id):
    event = storage.get(Event, event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    event.save()
    return jsonify(event.to_dict()), 200

# Admin & Pastor: Delete an event
@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
@role_required(['ADMIN', 'PASTOR'])
def delete_event(event_id):
    event = storage.get(Event, event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    event.delete()
    return jsonify({"message": "Event deleted successfully"}), 200

# Member, Admin, & Pastor: Register for an event
@events_bp.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
@role_required(['MEMBER', 'ADMIN', 'PASTOR'])
def register_for_event(event_id):
    event = storage.get(Event, event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    user_id = get_jwt_identity()
    if user_id not in [user.id for user in event.attendance]:
        event.attendance.append(user_id)
        event.save()
        return jsonify({"message": "Registered for the event successfully"}), 200
    else:
        return jsonify({"error": "You are already registered for this event"}), 400

