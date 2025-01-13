#!/usr/bin/python3
"""Manages membership of the church
TODO 1: Member Information Tracking:
     -- Maintain basic and detailed records for each member.
     -- Associate members with specific departments/ministries.

TODO 2: Role and Status Management:
     -- Categorize members by roles (e.g., Pastor, Member, Leader).
     -- Track membership status (active, inactive, new, transferred).

TODO 3: Engagement Tracking:
     -- Record participation in events, programs, or groups.

TODO 4: Reporting and Insights:
     -- Generate lists or statistics (e.g., number of active members, distribution by department).
"""
from app.models.base_model import BaseModel


class Membership(BaseModel):
    first_name = ""
    last_name = ""
    other_names = ""
    email = ""
    phone_number = ""
    address = ""
    date_of_birth = None
    membership_id = ""
    date_joined = None
    role_in_church = ""
    department_id = ""
    group_id = ""
    last_attendance_date = None
    is_active = True


