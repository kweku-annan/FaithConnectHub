#!/usr/bin/python3
from app.models.user import  User
from app.models import storage
from app.models.base_model import BaseModel
from app.models.user import User
from tests.test_save_reload_base_model import all_objs

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "FaithConnect@gmail.com"
my_user.password_hash = "root"
my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.first_name = "John"
my_user2.email = "User2@email.com"
my_user2.password_hash = "root"
my_user2.save()
print(my_user2)