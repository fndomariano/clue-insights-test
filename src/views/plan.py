from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from src import app, db
from src.models.plan import Plan
from src.models.subscription import Subscription
from src.schemas.plan import PlanSchema
from datetime import datetime


@app.route('/plan', methods=['GET'])
def list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name_filter = request.args.get('name', '', type=str)

    query = Plan.query

    if name_filter:
        query = query.filter(Plan.name.ilike(f"%{name_filter}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    schema = PlanSchema(many=True)
    plans = schema.dump(pagination.items)

    return jsonify({
        "data": plans,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages
        }
    })

@app.route('/plan/<id>', methods=['GET'])
def get(id):
        
    plan = Plan.query.get(id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    return jsonify(data={'id': plan.id, 'name': plan.name, 'price': plan.price, 'active': plan.active }), 200



@app.route('/plan', methods=['POST'])
def create():
    schema = PlanSchema()
    
    try:        
        data = schema.load(request.get_json())        
    except ValidationError as err:        
        return jsonify(err.messages), 422
    
            
    plan = Plan(name=data['name'], price=data['price'])
    db.session.add(plan)
    db.session.commit()

    return jsonify(message='The Plan was registered.'), 201



@app.route('/plan/<id>', methods=['PUT'])
def update(id):
    
    schema = PlanSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 422
    
    plan = Plan.query.get(id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404

    if 'name' in data:
        plan.name = data['name']

    if 'price' in data:
        plan.price = data['price']
        
    db.session.commit()

    return jsonify(message='The Plan has been updated.'), 204


@app.route('/plan/<id>', methods=['DELETE'])
def delete(id):
        
    plan = Plan.query.get(id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    db.session.delete(plan)
    db.session.commit()

    return jsonify(message='The Plan has been deleted.'), 204


@app.route('/plan/<id>/changeStatus', methods=['POST'])
def changeStatus(id):
        
    plan = Plan.query.get(id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    
    plan.active = not plan.active

    db.session.commit()

    return jsonify(message='The Plan has been deleted.'), 204


@app.route('/plan/<id>/subscribe', methods=['POST'])
@jwt_required()
def subscribe(id):    
    user_id = get_jwt_identity()    
    plan = Plan.query.get(id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
    
    Subscription.query.filter_by(user_id=user_id, active=True).update({'active': False, 'canceled_at': datetime.utcnow()})

    sub = Subscription(user_id=user_id, plan_id=plan.id)
    db.session.add(sub)
    db.session.commit()

    return jsonify(message='The subscription has been completed.'), 200