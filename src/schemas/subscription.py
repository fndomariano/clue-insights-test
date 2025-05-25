from marshmallow import Schema, fields

class SubscriptionSchema(Schema):    
    plan_id = fields.Str(required=True)

class PlanHistorySchema(Schema):
    id = fields.Int()
    name = fields.Str()

class SubscriptionHistorySchema(Schema):
    created_at = fields.DateTime()
    canceled_at = fields.DateTime(allow_none=True)
    active = fields.Bool()
    plan = fields.Nested(PlanHistorySchema)