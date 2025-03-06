#!/usr/bin/python3
"""Defines database schema for user input validation"""
from marshmallow import Schema, fields, validate, pre_load, ValidationError
from app.models.user import User
from app.models import storage


class UserSchema(Schema):
    """Schema to validate user input data"""

    # User fields with validation rules and custom error messages
    username = fields.String(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={
            "required": "Username is required.",
            "validator_failed": "Username cannot be empty."
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "A valid email is required.",
            "invalid": "Invalid email format. Please provide a valid email address (e.g., johndoe@example.com)."
        }
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8),
        error_messages={
            "required": "Password is required.",
            "validator_failed": "Password must be at least 8 characters long."
        }
    )