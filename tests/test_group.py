from app.models import storage
from app.models.group import Group
from app.models.department import Department
from app.models.member import Member

# Get department id
department = storage.query(Department).filter_by(name="Youth Ministry").first()
department_id = department.id

# Get member id
member = storage.query(Member).filter_by(email="john.doe3@example.com").first()
leader_id = member.id

# Create a new group
group = Group(
    department_id=department_id,
    name="Bible Study Group",
    description="A group focused on weekly Bible studies.",
    leader_id=leader_id
)
group.save()
print(group.to_dict())
