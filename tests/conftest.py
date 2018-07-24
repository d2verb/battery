import os
import tempfile
import pytest

from battery import create_app
from battery.models import db as _db

TEST_DB_PATH = tempfile.mkstemp()[1]
TEST_DB_URI = "sqlite:///" + TEST_DB_PATH

@pytest.fixture(scope="session")
def app(request):
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DB_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": True
    }
    app = create_app(test_config)

    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app

@pytest.fixture(scope="session")
def db(app, request):
    if os.path.exists(TEST_DB_PATH):
        os.unlink(TEST_DB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TEST_DB_PATH)

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope="function")
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
