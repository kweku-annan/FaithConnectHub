#!/usr/bin/env python3
"""Handles business logic for registration and authentication"""
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models import storage

class AuthService:
    """Handles business logic for registration and authentication"""
    @staticmethod
    def register_user(data):
        """Registers a new user"""
        # Check for existing user email
        if storage.query(User).filter_by(email=data['email']).first():
            return {'error': 'User with this email already exists'}, 400

        # Check for existing username
        if storage.query(User).filter_by(username=data['username']).first():
            return {'error': 'User with this username already exists'}, 400

        # Check for missing email, password or username
        if not data['email'] or not data['password'] or not data['username']:
            return {'error': 'Missing email, password or username'}, 400

        # Create new user
        user = User(
            email=data['email'],
            username=data['username'],
            role=data.get('role', 'Member'),
        )
        user.set_password(data['password'])
        storage.save(user)

        return {'message': 'User registered successfully'}, 201

    @staticmethod
    def authenticate_user(data):
        """Authenticates a user"""
        user = storage.query(User).filter(
            or_(User.email == data['email'], User.username == data['email'])
        ).first()

        if user and user.check_password(data['password']):
            return user
        return None
