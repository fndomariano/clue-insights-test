from src import db
from src.models.plan import Plan
from src.models.subscription import Subscription

def test_subscription(client, auth_token):
    # given 
    plan_free = Plan(name="Free", price=0)
    db.session.add(plan_free)
    db.session.commit()

    # when
    response = client.post(
        "/subscriptions/subscribe",
        json={"plan_id": str(plan_free.id)},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # then    
    print(response.get_json())
    assert response.status_code == 200

    subscription = db.session.query(Subscription).filter_by(user_id=1, plan_id=1).first()
    assert subscription is not None
    assert subscription.plan_id == 1
    assert subscription.user_id == 1
    assert subscription.created_at is not None
    assert subscription.canceled_at is None
    assert subscription.active is True


def test_upgrade_subscription(client, auth_token):
    
    # given
    plan_free = Plan(name="Free", price=0)
    plan_basic = Plan(name="Basic", price=10)
    db.session.add_all([plan_free, plan_basic])
    db.session.commit()

    subscription = Subscription(plan_id=plan_free.id, user_id=1)
    db.session.add(subscription)
    db.session.commit()
    
    # when
    response = client.post(
        "/subscriptions/subscribe",
        json={"plan_id": str(plan_basic.id)},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # then
    assert response.status_code == 200

    subscription_free = db.session.query(Subscription).filter_by(user_id=1, plan_id=plan_free.id).first()
    assert subscription_free is not None
    assert subscription_free.canceled_at is not None
    assert subscription_free.active is False

    subscription_basic = db.session.query(Subscription).filter_by(user_id=1, plan_id=plan_basic.id).first()
    assert subscription_basic is not None        
    assert subscription_basic.canceled_at is None
    assert subscription_basic.active is True


def test_cancel_subscription(client, auth_token):
    # given
    plan_free = Plan(name="Free", price=0)
    db.session.add(plan_free)
    db.session.commit()

    subscription = Subscription(plan_id=plan_free.id, user_id=1)
    db.session.add(subscription)
    db.session.commit()

    # when
    response = client.post(
        "/subscriptions/cancel",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # then
    assert response.status_code == 200

    subscription = db.session.query(Subscription).filter_by(user_id=1, plan_id=plan_free.id).first()
    assert subscription is not None
    assert subscription.canceled_at is not None
    assert subscription.active is False