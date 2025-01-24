from app.models import storage
from app.models.member import Member
from app.models.user import User

member = Member(
    first_name="John",
    last_name="Doe",
    email="john.doe3@example.com",
    role="Leader",
    phone_number="+233554957158",
    address="1234 Main Street, Accra, Ghana",
    date_of_birth="1990-01-01",
    gender="Male",
    marital_status="Single",
    date_joined="2021-01-01"
)
member.save()

user = User(username="admin0", email="admin0@example.com", role="Admin0", member_id=member.id)
user.set_password("adminPassword0")
user.save()

print(storage.query(User).all())