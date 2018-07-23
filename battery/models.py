from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash

# initialize db later in create_app
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="", nullable=False)
    _password = db.Column("password", db.String(100), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym("_password", descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, name, password):
        user = query(cls).filter(cls.name == name).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return "<User id={id} name={name}>".format(id=self.id, name=self.name)


class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id",
                                                  onupdate="CASCADE",
                                                  ondelete="SET NULL"))
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(db.Date, default=datetime.now().date())
    updated_at = db.Column(db.Date, default=datetime.now().date())

    def __repr__(self):
        return "<Entry id={id} t={title!r} c={created_at} u={updated_at}>".format(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
            updated_at=self.updated_at)


class Comment(db.Model):
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id",
                                                onupdate="CASCADE",
                                                ondelete="CASCADE"))
    author = db.Column(db.String(50), default="Anonymous")
    created_at = db.Column(db.Date, default=datetime.now().date())
    content = db.Column(db.Text)

    def __repr__(self):
        return "<Comment id={id} entry_id={entry_id} author={author}>".format(
            id=self.id,
            entry_id=self.entry_id,
            author=self.author)
