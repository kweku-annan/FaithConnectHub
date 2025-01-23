#!/usr/bin/python3
"""File storage model"""
import json


class FileStorage:
    """Works with making data persistent"""
    __file_path = "../file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls is None:
            return FileStorage.__objects
        temp = {}
        for key, value in self.__objects.items():
            if isinstance(value, cls):
                temp[key] = value
        return temp

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        obj_id_name = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[obj_id_name] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        a_dict = {}
        for key in FileStorage.__objects:
            a_dict[key] = FileStorage.__objects[key].to_dict()
        with open(FileStorage.__file_path, mode='w',
                  encoding='utf-8') as a_file:
            json.dump(a_dict, a_file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        from app.models.base_model import BaseModel
        from app.models.user import User
        from app.models.membership import Membership
        from app.models.event import Event
        from app.models.attendance import Attendance
        from app.models.finance import Expense, Income

        # Mapping of class names to class references
        class_map = {
            "BaseModel": BaseModel,
            "User": User,
            "Membership": Membership,
            "Event": Event,
            "Attendance": Attendance,
            "Expense": Expense,
            "Income": Income
        }

        try:
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') as a_file:
                a_dict = json.load(a_file)
            for key, value in a_dict.items():
                class_name = value.pop("__class__", None)
                cls = class_map.get(class_name)

                if cls:
                    # Filter out invalid keys that are not class attributes
                    if hasattr(cls, '__table__'):  # Make sure the class has a __table__ attribute
                        valid_keys = {col.name for col in cls.__table__.columns}
                        filtered_data = {k: v for k, v in value.items() if k in valid_keys}

                        # Initialize the object with the filtered data
                        attri_value = cls(**filtered_data)
                        FileStorage.__objects[key] = attri_value
                    else:
                        # Handle abstract or unmapped classes gracefully
                        filtered_data = {k: v for k, v in value.items() if k not in ['__table__']}
                        FileStorage.__objects[key] = cls(**filtered_data)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
            obj_key = f'{obj.to_dict()["__class__"]}.{obj.id}'
            if obj_key in self.__objects.keys():
                del self.__objects[obj_key]