from battery.models import User, Entry

def test_create_entry(session):
    user = User.query.filter_by(name="defuser").first()
    entry = Entry(title="test title",
                  content="test content",
                  user_id=user.id)
    
    session.add(entry)
    session.commit()

    _entry = Entry.query.filter_by(id = entry.id).first()

    assert _entry is not None
    assert _entry.title == entry.title
    assert _entry.content == entry.content
    assert _entry.user_id == entry.user_id
