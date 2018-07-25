from battery.models import User, Entry, Comment

def prepare_user(session, username, password, commit=True):
    user = User(username=username, password=password)
    session.add(user)

    if commit:
        session.commit()

    return user

def prepare_entry(session, title, content, user_id, commit=True):
    entry = Entry(title=title, content=content, user_id=user_id)
    session.add(entry)

    if commit:
        session.commit()

    return entry

def prepare_comment(session, author, content, entry_id, commit=True):
    comment = Comment(author=author, content=content, entry_id=entry_id)
    session.add(comment)

    if commit:
        session.commit()

    return comment
