#!/usr/bin/python3
"""Manages User Role and Authentications
TODO 1: User Authentication
        Verifies the identity of a user.
        Involves processes like login, logout, and secure session management.

TODO 2: Role Management
        Assigns roles to users (e.g., Admin, Pastor, Member).
        Controls access to specific features or resources based on the
        user’s role.

TODO 3: Authorization
        Ensures that users can only perform actions or access
        resources permitted for their role.
"""
from datetime import datetime, timedelta

from dns.dnssecalgs import algorithms
from flask import current_app
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app.models.base_model import BaseModel, Base
from enum import Enum as PyEnum

# Association table for user roles
user_roles = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', String(50), ForeignKey('users.id')),
    Column('role_id', String(50), ForeignKey('roles.id'))
)

# Association table for role permissions
role_permissions = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', String(50), ForeignKey('roles.id')),
    Column('permission_id', String(50), ForeignKey('permissions.id'))
)


class UserStatus(PyEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    PENDING = 'pending'


class User(BaseModel, Base):
    """Defines user authentications and roles"""
    __tablename__ = 'users'

    # Basic Information
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)

    # Account Details
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    must_change_password = Column(Boolean, default=True)

    # Profile Association
    member_id = Column(String(50), ForeignKey('membership.id'), unique=True)

    # Relationships
    member = relationship("Membership", back_populates="user")
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    sessions = relationship('UserSession', back_populates='user')

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        """Generate JWT token for user authentication"""
        return jwt.encode(
            {
                'user.id': self.id,
                'exp': datetime.utcnow() + timedelta(seconds=expires_in)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_with_token(token):
        """Verify JWT token and return user"""
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return User.query.get(data['user_id'])
        except:
            return None

    def has_permission(self, permission_name):
        """Check if user has specific permission"""
        return any(
            permission.name == permission_name
            for role in self.roles
            for permission in role.permissions
        )

    def has_role(self, role_name):
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)


class Role(BaseModel, Base):
    """Define user roles"""
    __tablename__ = 'roles'

    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    is_system_role = Column(Boolean, default=False)  # For built-in roles

    # Relationships
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')

    @classmethod
    def create_default_roles(cls):
        """Creates default system roles"""
        default_roles = [
            ('super_admin', 'Full system access'),
            ('admin', 'Administrative access'),
            ('pastor', 'Pastoral access'),
            ('staff', 'Staff member access'),
            ('member', 'Regular member access'),
            ('guest', 'Limited guest access')
        ]
        return [
            cls(name=name, description=desc, is_system_role=True)
            for name, desc in default_roles
        ]


class Permission(BaseModel, Base):
    """Handles permissions of users"""
    __tablename__ = 'permissions'

    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    resource = Column(String(50))  # The resource this permission applies to
    action = Column(String(50)) # The action allowed (create, read, update, delete)

    # Relationships
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')

    @classmethod
    def create_default_permissions(cls):
        """Create default system permissions"""
        resources = ['members', 'departments', 'finances', 'events', 'attendance', 'groups']
        actions = ['create', 'read', 'update', 'delete']

        permissions = []
        for resource in resources:
            for action in actions:
                name = f"{resource}:{action}"
                description = f"Can {action} {resource}"
                permissions.append(cls(
                    name=name,
                    description=description,
                    resource=resource,
                    action=action
                ))
        return permissions


class UserSession(BaseModel, Base):
    """Handles user sessions"""
    __tablename__ = 'user_sessions'

    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    token = Column(String(500), nullable=False)
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="sessions")


    def is_valid(self):
        """Check if session is valid"""
        return (
            self.is_active and self.expires_at > datetime.utcnow
        )