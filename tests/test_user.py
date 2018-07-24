from battery.models import User

def test_add_user(session):
    user = User(name="test", password="test")

    session.add(user)
    session.commit()

    assert user.id > 0
    assert user.name == "test"
    assert User.query.filter_by(name = "test").first() is not None

def test_password_auth(session):
    user = User(name="test", password="test")

    session.add(user)
    session.commit()

    assert User.authenticate(session.query, "test", "test")[1]
    assert not User.authenticate(session.query, "test", "invalid password")[1]

def test_add_same_name_user(session):
    user1 = User(name="test", password="test1")
    session.add(user1)

    user2 = User(name="test", password="test2")
    session.add(user2)

    from sqlalchemy.exc import IntegrityError

    try:
        session.commit()
    except IntegrityError as e:
        assert "UNIQUE constraint failed" in str(e)
    else:
        assert False
