#!/usr/bin/python3
"""Test delete feature"""
from app.engine.file_storage import FileStorage
from app.models.user import User

fs = FileStorage()

# All Users
all_users = fs.all(User)
print("All Users: {}".format(len(all_users.keys())))
for user_key in all_users.keys():
    print(all_users[user_key])

# Create a new User
new_user = User()
new_user.first_name = "Emmanuel"
new_user.last_name = "Saah"
new_user.email = "aduemma07@gmail.com"
fs.new(new_user)
fs.save()
print("New User: {}".format(new_user))

# All Users
all_users = fs.all(User)
print("All Users: {}".format(len(all_users.keys())))
for user_key in all_users.keys():
    print(all_users[user_key])

# Create another user
another_user = User()
another_user.first_name = "Caleb"
another_user.last_name = "Konado"
another_user.email = "candour@gmail.com"
fs.new(another_user)
fs.save()
print("Another State: {}".format(another_user))

# All Users
all_users = fs.all(User)
print("All Users: {}".format(len(all_users.keys())))
for user_key in all_users.keys():
    print(all_users[user_key])

# Delete the new User
fs.delete(new_user)

# All Users
all_users = fs.all(User)
print("All Users: {}".format(len(all_users.keys())))
for user_key in all_users.keys():
    print(all_users[user_key])