from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src import db
from src.models.plan import Plan
from src.schemas.plan import PlanSchema

bp = Blueprint('plan', __name__, url_prefix='/plan')

@bp.route('/', methods=['GET'])
def list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name_filter = request.args.get('name', '', type=str)

    query = Plan.query

    if name_filter:
        query = query.filter(Plan.name.ilike(f"%{name_filter}%"))    

    query = query.order_by(Plan.name.asc())

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

@bp.route('/<id>', methods=['GET'])
def get(id):
        
    plan = db.session.get(Plan, id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    return jsonify(data={'id': plan.id, 'name': plan.name, 'price': plan.price, 'active': plan.active }), 200



@bp.route('/', methods=['POST'])
def create():
    schema = PlanSchema()
    
    try:        
        data = schema.load(request.get_json())        
    except ValidationError as err:        
        return jsonify(errors=err.messages), 422
    
            
    plan = Plan(name=data['name'], price=data['price'])
    db.session.add(plan)
    db.session.commit()

    return jsonify(message='The Plan was registered.'), 201



@bp.route('/<id>', methods=['PUT'])
def update(id):
    
    schema = PlanSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(errors=err.messages), 422
    
    plan = db.session.get(Plan, id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404

    if 'name' in data:
        plan.name = data['name']

    if 'price' in data:
        plan.price = data['price']
        
    db.session.commit()

    return jsonify(message='The Plan has been updated.'), 204


@bp.route('/<id>', methods=['DELETE'])
def delete(id):
        
    plan = db.session.get(Plan, id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    db.session.delete(plan)
    db.session.commit()

    return jsonify(message='The Plan has been deleted.'), 204


@bp.route('/<id>/changeStatus', methods=['POST'])
def changeStatus(id):
        
    plan = db.session.get(Plan, id)

    if not plan:
        return jsonify(error='The Plan was not found.'), 404
        
    
    plan.active = not plan.active

    db.session.commit()

    return jsonify(message='The Plan has been deleted.'), 204


