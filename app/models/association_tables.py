#!/usr/bin/env python
"""Defines the association tables for the many-to-many relationships in the database"""
from sqlalchemy import Column, String, ForeignKey, Table
from app.models.base_model import Base

member_department = Table(
    'member_department', # Name of the 'bridge' table
    Base.metadata,
    Column('member_id', String(60), ForeignKey('members.id'), primary_key=True),
    Column('department_id', String(60), ForeignKey('departments.id'), primary_key=True)
)

member_group = Table(
    'member_group', # Name of the 'bridge' table
    Base.metadata,
    Column('member_id', String(60), ForeignKey('members.id'), primary_key=True),
    Column('group_id', String(60), ForeignKey('groups.id'), primary_key=True)
)