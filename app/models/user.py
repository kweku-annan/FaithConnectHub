#/usr/bin/env python
"""User model"""
from datetime import datetime

from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Boolean, ForeignKey


class User(BaseModel, Base):
    __tablename__ = 'users'

    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default='MEMBER')
    is_active = Column(Boolean, default=True)
    member_id = Column(String(60), ForeignKey('members.id'), nullable=True)


    # Relationships
    member = relationship("Member", back_populates="user")

    def __init__(self, *args, **kwargs):
        """Initializes the User instance"""
        super().__init__(*args, **kwargs)
        self.is_active = self.is_active or True
        self.role = self.role or 'Member'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """"""
        return check_password_hash(self.password, password)

    @staticmethod
    def check_duplicate_username(username):
        """Checks duplicate usernames"""
        from app.models import storage
        return storage.query(User).filter(User.username == username).first()

    @staticmethod
    def check_duplicate_email(email):
        """Checks duplicate email"""
        from app.models import storage
        return storage.query(User).filter(User.email == email).first()

    def save(self):
        """Custom save method to ensure no duplicates, then saves the user"""
        if self.check_duplicate_username(self.username):
            raise ValueError("Username already exists")
        if self.check_duplicate_email(self.email):
            raise ValueError("Email already exists")
        super().save()

    def __repr__(self):
        return f"<User {self.username}, Role: {self.role}>"

    def __str__(self):
        return f"<User {self.username}, Role: {self.role}>"
