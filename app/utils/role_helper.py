#!/usr/bin/python3
"""Utility for role-based access control"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(allowed_roles):
    """
    Decorator to restrict access based on roles.
    :param allowed_roles: List of roles that can access the route
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
