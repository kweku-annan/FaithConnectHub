#!/usr/bin/python3
"""Creates a Unique DBStorage instance for the application using SQLAlchemy with mysql+mysqldb
databse connection
"""

import os
from app.models.base_model import Base
from app.models.user import User
from app.models.member import Member
from app.models.event import Event
from app.models.attendance import Attendance
from app.models.finance import Expense, Income
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {
    'User': User, 'Member': Member, 'Event': Event,
    'Expense': Expense, 'Income': Income, 'Attendance': Attendance
}

class DBStorage:
    """Manages storage of SQLAlchemy database"""
    __engine = None
    __session = None  # Session class instance

    def __init__(self):
        """Creates the engine and session"""
        user = os.getenv("MYSQL_USER")
        pwd = os.getenv("MYSQL_PWD")
        host = os.getenv("MYSQL_HOST")
        db = os.getenv("MYSQL_DB")
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine) # Drop all tables

    def all(self, cls=None):
        """Returns a dictionary of all objects present"""
        dict_object = {}
        if not self.__session:
            self.reload()
        if type(cls) == str:
            cls = classes.get[cls, None]
        if cls:
            for obj in self.__session.query(cls):
                key = f"{type(obj).__name__}.{obj.id}"
                dict_object[key] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls):
                    key = f"{type(obj).__name__}.{obj.id}"
                    dict_object[key] = obj
        return dict_object

    def reload(self):
        """Reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """Creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delets and object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Closes the current session"""
        self.__session.remove()

    def get(self, cls, id):
        """Returns an object based on the class name and id"""
        if cls is not None and type(cls) is str and id is not None and type(id) is str and cls in classes:
            cls = classes[cls]
            obj = self.__session.query(cls).filter(cls.id == id).first()
            return obj
        else:
            return None

    def count(self, cls=None):
        """Returns the number of objects in storage"""
        total = 0
        if cls is not None and type(cls) is str and cls in classes:
            cls = classes[cls]
            total += self.__session.query(cls).count()
        else:
            for cls in classes.values():
                total += self.__session.query(cls).count()
        return total


