from marshmallow import Schema, fields, validates_schema, ValidationError
from src.models.user import User

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates_schema
    def validate_unique_email(self, data, **kwargs):
        if User.query.filter_by(email=data.get('email')).first():
            raise ValidationError({'email': ['This email is already in use.']})