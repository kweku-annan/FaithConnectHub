#!/usr/bin/python3
"""Creates a Unique FileStorage instance for the application"""
from app.schemas.db_storage import DBStorage

storage = DBStorage()
storage.reload()
