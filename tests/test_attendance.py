from app.models import storage
from app.models.attendance import Attendance
from app.models.event import Event
from app.models.member import Member

# Create a new event
event = Event(
    name="Sunday Service",
    description="Weekly Sunday service",
    start_date="2021-09-05",
    end_date="2021-09-05",
    start_time="09:00:00",
    end_time="11:00:00",
    location="Church Auditorium",
    category="Service"
)

event.save()

# Create a new member
member = Member(
    first_name="John",
    last_name="Doe",
    email="john.doe8@example.com",
    phone_number="123-456-7890",
    address="123 Main St, Anytown, USA",
    date_of_birth="1990-01-01",
    gender="Male",
    marital_status="Single",
    status="active",
    role="Member",
    date_joined="2021-09-05"
)
member.save()

attendance = Attendance(
    member_id=member.id,
    event_id=event.id,
    status="present",
    notes="Attended the service on time."
)
attendance.save()
print(storage.query(Attendance).all())
