#!/usr/bin/env python3
"""Defines request validation schemas for clean input handling using Marshmallow."""
from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    """Defines the schema for user registration"""
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(required=False, validate=validate.OneOf(['Member', 'Admin', 'Pastor', 'Stuff', 'Super_admin']))


class LoginSchema(Schema):
    """Defines the schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserSchema(Schema):
    """Defines the schema for user details"""
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    role = fields.Str(required=False, validate=validate.OneOf(['Member', 'Admin', 'Pastor', 'Stuff', 'Super_admin']))
    is_active = fields.Boolean(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


