from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from src.models.plan import Plan

class PlanSchema(Schema):    
    name = fields.Str(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0, error="Price must be a non-negative number"))

    @validates_schema
    def validate_unique_name(self, data, **kwargs):
        if Plan.query.filter_by(name=data.get('name')).first():
            raise ValidationError({'name': ['This plan name is already in use.']})
