#!usr/bin/python3
"""Defines the schema for member input data validation"""
from marshmallow import Schema, fields, validates, ValidationError, pre_load
from datetime import datetime
from app.models.member import Member
from app.models import storage


class MemberSchema(Schema):
    """Schema to validate member input data"""

    # Personal information fields with validation rules and custom error messages
    first_name = fields.String(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={
            "required": "First name is required.",
            "validator_failed": "First name cannot be empty."
        }
    )
    last_name = fields.String(
        required=True,
        validate=lambda x: len(x) > 0,
        error_messages={
            "required": "Last name is required.",
            "validator_failed": "Last name cannot be empty."
        }
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "A valid email is required.",
            "invalid": "Invalid email format. Please provide a valid email address (e.g., johndoe@example.com)."
        }
    )
    phone_number = fields.String(
        required=True,
        error_messages={
            "required": "Phone number is required.",
            "invalid": "Phone number must contain only digits and be at least 10 characters long (e.g., 1234567890)."
        }
    )
    address = fields.String(
        required=True,
        error_messages={
            "required": "Address is required.",
            "validator_failed": "Address cannot be empty."
        }
    )
    date_of_birth = fields.Date(
        required=True,
        error_messages={
            "required": "Date of birth is required.",
            "invalid": "Invalid date format. Please use the format YYYY-MM-DD (e.g., 1990-01-01)."
        }
    )
    gender = fields.String(
        required=True,
        validate=lambda x: x in ['male', 'female'],
        error_messages={
            "required": "Gender is required.",
            "validator_failed": "Invalid gender value. Allowed values are 'male' or 'female'."
        }
    )
    marital_status = fields.String(
        required=True,
        validate=lambda x: x in ['single', 'married', 'divorced', 'widowed'],
        error_messages={
            "required": "Marital status is required.",
            "validator_failed": "Invalid marital status value. Allowed values are 'single', 'married', 'divorced', or 'widowed'."
        }
    )

    # Church-related fields with default values and custom error messages
    status = fields.String(
        missing='active',
        validate=lambda x: x in ['active', 'inactive', 'suspended'],
        error_messages={
            "validator_failed": "Invalid status value. Allowed values are 'active', 'inactive', or 'suspended'."
        }
    )
    role = fields.String(
        missing='Member',
        validate=lambda x: x in ['Member', 'ADMIN', 'PASTOR'],
        error_messages={
            "validator_failed": "Invalid role value. Allowed values are 'Member', 'ADMIN', or 'PASTOR'."
        }
    )
    date_joined = fields.Date(
        missing=lambda: datetime.now().date(),
        error_messages={
            "invalid": "Invalid date format. Please use the format YYYY-MM-DD (e.g., 2023-10-01)."
        }
    )
    department_id = fields.String(required=False, allow_none=True)
    group_id = fields.String(required=False, allow_none=True)

    @pre_load
    def normalize_inputs(self, data, **kwargs):
        """Normalize specific string inputs that require selection from a list"""
        selective_fields = ['gender', 'marital_status', 'status', 'role']
        for field in selective_fields:
            if field in data and isinstance(data[field], str):
                # Normalize the input to lowercase
                normalized_value = data[field].lower()

                # Get the allowed values for the field
                allowed_values = self.get_allowed_values(field)

                # Check if the normalized value is in the allowed values
                if normalized_value in [value.lower() for value in allowed_values]:
                    data[field] = allowed_values[[value.lower() for value in allowed_values].index(normalized_value)]
                else:
                    raise ValidationError(f"Invalid value for {field}. Allowed values are {', '.join(allowed_values)}.")

        return data

    def get_allowed_values(self, field):
        """Get allowed values for a specific field"""
        allowed_values = {
            'gender': ['male', 'female'],
            'marital_status': ['single', 'married', 'divorced', 'widowed'],
            'status': ['active', 'inactive', 'suspended'],
            'role': ['MEMBER', 'ADMIN', 'PASTOR']
        }
        return allowed_values.get(field, [])


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


'''
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
'''