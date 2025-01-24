from app.models import storage
from app.models.member import Member

member = Member(
    first_name="John",
    last_name="Doe",
    email="john.doe1@example.com",
    role="Leader",
    phone_number="+233554957158",
    address="1234 Main Street, Accra, Ghana",
    date_of_birth="1990-01-01",
    gender="Male",
    marital_status="Single",
    date_joined="2021-01-01"
)
member.save()
print(member.id)
print(storage.query(Member).all())

"""
 first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(120), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(String(10), nullable=False)
    marital_status = Column(String(20), nullable=False)

    # Church Information
    status = Column(String(20), nullable=False, default='active')  # active, inactive, suspended
    role = Column(String(20), nullable=False, default='Member')  # member, leader, admin, pastor
    date_joined = Column(DateTime, nullable=False)
    department_id = Column(String(60), ForeignKey('departments.id'), nullable=True)
    group_id = Column(String(60), ForeignKey('groups.id'), nullable=True)
"""
