from app.models import storage
from app.models.member import Member

member = Member(first_name="John", last_name="Doe", email="john.doe@example.com", role="Leader")
member.save()
print(storage.query(Member).all())
