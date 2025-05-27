from marshmallow import Schema, fields

class SubscriptionSchema(Schema):    
    plan_id = fields.Int(required=True)