#!/usr/bin/python3
"""File storage model"""
import json


class FileStorage:
    """Works with making data persistent"""
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """Initializes public attributes"""
        pass

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__file_path

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
                FileStorage.__objects[key] = eval(value['__class__'])(**value)
        except FileNotFoundError:
            pass

