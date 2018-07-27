from battery.models import db, User, Entry, Comment
from flask import render_template, request, session, flash, redirect, url_for
from flask import g, jsonify, abort, Blueprint
from functools import wraps
from sqlalchemy.exc import IntegrityError

# There is no merit to use blueprint now
# I just don't want views.py depend on specific app object
bp = Blueprint("app", __name__)

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            flash("You must log in first")
            return redirect(url_for("app.login", next=request.path))
        return fn(*args, **kwargs)
    return decorated_view

@bp.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session["user_id"])

@bp.route("/")
def index():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("index.html", entries=entries)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    user, authenticated = User.authenticate(db.session.query,
                                            request.form["username"],
                                            request.form["password"])
    if authenticated:
        session["user_id"] = user.id
        flash("You were logged in")
        return redirect(url_for("app.index"))
    else:
        flash("Invalid username or password")

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You were logged out")
    return redirect(url_for("app.index"))

@bp.route("/entry/new/", methods=["GET", "POST"])
@login_required
def post_entry():
    if request.method == "GET":
        return render_template("editor.html", destination=url_for("app.post_entry"))

    entry = Entry(title=request.form["title"],
                  content=request.form["content"],
                  user_id=session["user_id"])
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("app.show_entry", entry_id=entry.id))

@bp.route("/entry/<int:entry_id>/edit/", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.get(entry_id)

    if request.method == "GET":
        return render_template("editor.html",
                               destination=url_for("app.edit_entry", entry_id=entry_id),
                               title=entry.title,
                               content=entry.content)

    entry.title = request.form["title"];
    entry.content = request.form["content"];
    db.session.commit()

    return redirect(url_for("app.show_entry", entry_id=entry.id))

@bp.route("/entry/<int:entry_id>/")
def show_entry(entry_id):
    entry = Entry.query.get(entry_id)
    comments = Comment.query.filter_by(entry_id=entry_id)
    return render_template("entry.html", entry=entry, comments=comments)

@bp.route("/entry/<int:entry_id>/delete/")
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("app.index"))

@bp.route("/entry/<int:entry_id>/comment/", methods=["POST"])
def post_comment(entry_id):
    author = request.form["author"]

    if not author:
        author = None

    comment = Comment(author=author,
                      content=request.form["content"],
                      entry_id=entry_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("app.show_entry", entry_id=entry_id))

@bp.route("/entry/<int:entry_id>/comment/<int:comment_id>/")
@login_required
def delete_comment(entry_id, comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("app.show_entry", entry_id=entry_id))

@bp.route("/entry/search/")
def search_entries():
    q = request.args["q"]
    entries = Entry.query.filter(Entry.content.contains(q))
    return render_template("index.html", entries=entries)

@bp.route("/entry/preview/", methods=["POST"])
@login_required
def show_preview():
    title = request.form["title"]
    content = request.form["content"]
    return render_template("preview.html", title=title, content=content)
