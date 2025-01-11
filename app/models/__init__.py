#!/usr/bin/python3
"""Creates a Unique FileStorage instance for the application"""
from app.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
