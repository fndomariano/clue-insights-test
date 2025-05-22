from src import bcrypt
from src.models.user import User

def test_register(client):
    # given
    payload = {
        'name': 'Test',
        'email':'test@test.com',
        'password': 'secret'
    }
    
    # when
    response = client.post('/user/register', json=payload)
    
    # then
    user = User.query.filter_by(email=payload['email']).first()
    assert 201 == response.status_code
    assert user is not None
    assert user.name == payload['name']
    assert user.email == payload['email']
    assert bcrypt.check_password_hash(user.password_hash, payload['password']) is True
    

def test_required_validation(client):
        
    # when
    response = client.post('/user/register', json={})
    
    # then       
    assert 422 == response.status_code
    
    data = response.get_json()
    assert "errors" in data
    assert "name" in data["errors"]
    assert "email" in data["errors"]
    assert "password" in data["errors"]