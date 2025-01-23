from app.models.user import User

user = User(username="admin3", email="admin3@example.com", role="Admin3")
user.set_password("adminPassword3")
user.save()

print(User.query.all())