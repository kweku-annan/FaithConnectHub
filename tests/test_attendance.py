from app.models import storage
from app.models.attendance import Attendance

attendance = Attendance(
    event_id="event-uuid",
    member_id="member-uuid",
    status="present",
    notes="Attended the service on time."
)
attendance.save()
print(storage.query(Attendance).all())
