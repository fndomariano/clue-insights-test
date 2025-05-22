from src import db, bcrypt
from src.models.user import User

def test_login_success(client):

    # given
    email = 'test@example.com'
    password = 'keypass'

    user = User(
        name='Test', 
        email=email, 
        password_hash=bcrypt.generate_password_hash(password).decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    # when
    response = client.post("/auth/login", json={"email": email, "password": password})
    
    # then
    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data

def test_invalid_password(client):
    # given
    email = 'test@example.com'
    
    user = User(
        name='Test', 
        email=email, 
        password_hash=bcrypt.generate_password_hash("keypass").decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    # when
    response = client.post("/auth/login", json={"email": email, "password": "123"})
    
    # then
    data = response.get_json()
    assert response.status_code == 401
    assert "error" in data

def test_user_not_found(client):
    # when
    response = client.post("/auth/login", json={"email": "test@example.com", "password": "123"})
    
    # then
    data = response.get_json()
    assert response.status_code == 401
    assert "error" in data