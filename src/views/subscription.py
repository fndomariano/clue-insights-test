from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql import text
from marshmallow import ValidationError
from datetime import datetime, UTC
from src import db
from src.models.plan import Plan
from src.models.subscription import Subscription
from src.schemas.subscription import SubscriptionSchema

bp = Blueprint('subscriptions', __name__, url_prefix='/subscriptions')

@bp.route('/history', methods=['GET'])
@jwt_required()
def subscription_history():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    sql = '''
        SELECT s.id, s.created_at, s.canceled_at, s.active, p.id as plan_id, p.name as plan_name
        FROM subscription s
        INNER JOIN plan p ON s.plan_id = p.id
        WHERE s.user_id = :user_id
        ORDER BY s.created_at DESC
        LIMIT :per_page OFFSET :offset
    '''
    result = db.session.execute(text(sql), {
        'user_id': user_id,
        'per_page': per_page,
        'offset': offset
    })
    items = [
        {
            'canceled_at': row.canceled_at.isoformat() if row.canceled_at else None,
            'active': True if row.active == 1 else False,
            'plan': {
                'id': row.plan_id,
                'name': row.plan_name
            }
        }
        for row in result
    ]
        
    return jsonify({'data': items}), 200

@bp.route('/subscribe', methods=['POST'])
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



@bp.route('/cancel', methods=['POST'])
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