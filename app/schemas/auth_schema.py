#!/usr/bin/env python3
"""Defines request validation schemas for clean input handling using Marshmallow."""
from marshmallow import Schema, fields, validate, pre_load


class RegisterSchema(Schema):
    """Defines the schema for user registration"""
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(required=False, validate=validate.OneOf(['ADMIN', 'PASTOR', 'MEMBER']))

    @pre_load
    def preprocess_data(self, data, **kwargs):
        if 'role' in data and data['role']:
            data['role'] = data['role'].upper()
        return data


class LoginSchema(Schema):
    """Defines the schema for user login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)



