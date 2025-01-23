#!/usr/bin/python3
"""Creates a Unique FileStorage instance for the application"""
from app.engine.file_storage import FileStorage

storage = FileStorage()

# Then import models after storage is created
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.membership import Membership
from app.models.department import Department
from app.models.event import Event
from app.models.attendance import Attendance
from app.models.finance import Expense, Income
from app.models.group import Group

storage.reload()
