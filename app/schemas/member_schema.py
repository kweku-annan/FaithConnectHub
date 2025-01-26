from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime
from app.models.member import Member
from app.models import storage


class MemberSchema(Schema):
    """Schema to validate member input data"""

    # Personal information fields with validation rules
    first_name = fields.String(required=True, validate=lambda x: len(x) > 0,
                               error_messages={"required": "First name is required."})
    last_name = fields.String(required=True, validate=lambda x: len(x) > 0,
                              error_messages={"required": "Last name is required."})
    email = fields.Email(required=True, error_messages={"required": "A valid email is required."})
    phone_number = fields.String(required=True, error_messages={"required": "Phone number is required."})
    address = fields.String(required=True, error_messages={"required": "Address is required."})
    date_of_birth = fields.Date(required=True, error_messages={"required": "Date of birth is required."})
    gender = fields.String(required=True, validate=lambda x: x in ['male', 'female'],
                           error_messages={"required": "Gender is required.", "invalid": "Invalid gender value."})
    marital_status = fields.String(required=True, validate=lambda x: x in ['single', 'married', 'divorced', 'widowed'],
                                   error_messages={"required": "Marital status is required.",
                                                   "invalid": "Invalid marital status value."})

    # Church-related fields with default values
    status = fields.String(missing='active', validate=lambda x: x in ['active', 'inactive', 'suspended'],
                           error_messages={"required": "Status is required.", "invalid": "Invalid status value."})
    role = fields.String(missing='Member', validate=lambda x: x in ['Member', 'ADMIN', 'PASTOR'],
                         error_messages={"required": "Role is required.", "invalid": "Invalid role value."})
    date_joined = fields.Date(missing=lambda: datetime.now().date())
    department_id = fields.String(required=False, allow_none=True)
    group_id = fields.String(required=False, allow_none=True)

    @validates('email')
    def validate_unique_email(self, email):
        """Check if the email already exists in the database"""
        if Member.check_duplicate_email(email):
            raise ValidationError("Email already exists. Please use a different one.")

    @validates('date_of_birth')
    def validate_date_of_birth(self, value):
        """Ensure date of birth is not in the future"""
        if value > datetime.now().date():
            raise ValidationError("Date of birth cannot be in the future.")

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        """Ensure phone number format (basic check, add custom logic if needed)"""
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits long.")
