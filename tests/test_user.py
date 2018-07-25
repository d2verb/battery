from battery.models import User
from utils import prepare_user

def test_add_user(session):
    user = prepare_user(session, username="test", password="test")

    assert user.id > 0
    assert user.username == "test"
    assert User.query.filter_by(username = "test").first() is not None

def test_password_auth(session):
    user = prepare_user(session, username="test", password="test")

    assert User.authenticate(session.query, "test", "test")[1]
    assert not User.authenticate(session.query, "test", "invalid password")[1]

def test_add_same_name_user(session):
    user1 = prepare_user(session, username="test", password="test1", commit=False)
    user2 = prepare_user(session, username="test", password="test2", commit=False)

    from sqlalchemy.exc import IntegrityError

    try:
        session.commit()
    except IntegrityError as e:
        assert "UNIQUE constraint failed" in str(e)
    else:
        assert False
