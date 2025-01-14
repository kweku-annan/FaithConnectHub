#!/usr/bin/python3
"""File storage model"""
import json
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.membership import Membership
from app.models.event import  Event
from app.models.attendance import Attendance
from app.models.finance import Expense, Income

class FileStorage:
    """Works with making data persistent"""
    __file_path = "../file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

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
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, mode='r',
                      encoding='utf-8') as a_file:
                a_dict = json.load(a_file)
            for key, value in a_dict.items():
                attri_value = eval(value["__class__"])(**value)
                FileStorage.__objects[key] = attri_value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
            obj_key = f'{obj.to_dict()["__class__"]}.{obj.id}'


