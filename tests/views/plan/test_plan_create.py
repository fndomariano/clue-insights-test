from src.models.plan import Plan

def test_add(client):
    # given
    payload = {
        'name': 'Premium',
        'price': 49.99
    }
    
    # when
    response = client.post('/plan/', json=payload)
    
    # then
    plan = Plan.query.filter_by(name=payload['name']).first()
    assert 201 == response.status_code
    assert plan is not None
    assert plan.price == payload['price']
    

def test_required_validation(client):
        
    # when
    response = client.post('/plan/', json={})
    
    # then       
    assert 422 == response.status_code
    
    data = response.get_json()
    assert "errors" in data
    assert "name" in data["errors"]
    assert "price" in data["errors"]