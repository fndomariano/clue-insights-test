from src.models.plan import Plan

def test_update(client):
    # given
    payload = {
        'name': 'Premium',
        'price': 49.99
    }
    
    # when
    response = client.put('/plan/1', json=payload)
    
    # then
    plan = Plan.query.filter_by(name=payload['name']).first()
    assert 204 == response.status_code
    assert plan is not None
    assert plan.price == payload['price']
    

def test_required_validation(client):
    # when
    response = client.put('/plan/1', json={})
    
    # then       
    assert 422 == response.status_code
    
    data = response.get_json()
    assert "errors" in data
    assert "name" in data["errors"]
    assert "price" in data["errors"]


def test_not_found(client):
    # given
    payload = {
        'name': 'Premium',
        'price': 49.99
    }

    # when
    response = client.put('/plan/0', json=payload)
    
    # then       
    assert 404 == response.status_code
    
    data = response.get_json()
    assert "error" in data
    assert "The Plan was not found." in data["error"]