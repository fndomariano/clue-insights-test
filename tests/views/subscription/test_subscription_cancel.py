from src import db
from src.models.plan import Plan
from src.models.subscription import Subscription


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

def test_cancel_subscription_not_found(client, auth_token):
    # when
    response = client.post(
        "/subscriptions/cancel",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # then
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert "The subscription was not found." in data["error"]