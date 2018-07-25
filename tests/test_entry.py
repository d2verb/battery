from battery.models import User, Entry
from utils import prepare_user, prepare_entry

def test_create_entry(session):
    user = prepare_user(session, username="test", password="test")
    entry = prepare_entry(session, title="test title", content="test content",
                          user_id=user.id)

    _entry = Entry.query.filter_by(id = entry.id).first()

    assert _entry is not None
    assert _entry.title == entry.title
    assert _entry.content == entry.content
    assert _entry.user_id == entry.user_id
