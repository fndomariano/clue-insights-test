from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime, UTC
from src import app, db
from src.models.plan import Plan
from src.models.subscription import Subscription
from src.schemas.subscription import SubscriptionSchema

@app.route('/subscriptions/subscribe', methods=['POST'])
@jwt_required()
def subscribe():        
    user_id = get_jwt_identity()   
    schema = SubscriptionSchema()
    
    try:        
        data = schema.load(request.get_json())
    except ValidationError as err:        
        return jsonify(errors=err.messages), 422

    plan = db.session.get(Plan, data['plan_id'])

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
    
    Subscription.query.filter_by(user_id=user_id, active=True).update({'active': False, 'canceled_at': datetime.now(UTC)})

    sub = Subscription(user_id=user_id, plan_id=plan.id)
    db.session.add(sub)
    db.session.commit()

    return jsonify(message='The subscription has been completed.'), 200

@app.route('/subscriptions/cancel', methods=['POST'])
@jwt_required()
def cancel():
    user_id = get_jwt_identity()
    
    subscription = db.session.query(Subscription).filter_by(user_id=user_id, active=True).first()

    if not subscription:
        return jsonify(error='The subscription was not found.'), 404
    
    subscription.active = False
    subscription.canceled_at = datetime.now(UTC)
    db.session.commit()

    return jsonify(message='The subscription has been canceled.'), 200