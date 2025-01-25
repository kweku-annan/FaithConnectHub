from app.models import storage
from app.models.department import Department
from app.models.member import Member

# Get leader_id from members table
member = storage.query(Member).filter_by(email="john.doe3@example.com").first()
member_id = member.id

# Create a new department
department = Department(
    leader_id = member_id,
    name="Youth Ministry",
    description="Focuses on engaging and mentoring young members."
)
department.save()
print(department.to_dict())
