from app.models import storage
from app.models.user import User

user = User(username="admin5", email="admin5@example.com", role="Admin5")
user.set_password("adminPassword5")
user.save()

print(storage.query(User).all())