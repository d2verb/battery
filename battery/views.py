from battery import app, db
from battery.models import User, Entry, Comment
from flask import render_template, request, session, flash, redirect, url_for
from flask import g, jsonify, abort
from functools import wraps

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            flash("You must log in first")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return decorated_view

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session["user_id"])

@app.route("/")
def index():
    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("index.html", entries=entries)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user, authenticated = User.authenticate(db.session.query,
                                                request.form["username"],
                                                request.form["password"])
        if authenticated:
            session["user_id"] = user.id
            flash("You were logged in")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    flash("You were logged out")
    return redirect(url_for("index"))

@app.route("/entry/new/", methods=["GET", "POST"])
@login_required
def create_entry():
    if request.method == "POST":
        entry = Entry(title=request.form["title"],
                      content=request.form["content"],
                      user_id=session["user_id"])
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("show_entry", entry_id=entry.id))

    return render_template("editor.html", destination=url_for("create_entry"))

@app.route("/entry/<int:entry_id>/edit/", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.get(entry_id)

    if request.method == "POST":
        entry.title = request.form["title"];
        entry.content = request.form["content"];
        db.session.commit()

        return redirect(url_for("show_entry", entry_id=entry.id))

    return render_template("editor.html",
                           destination=url_for("edit_entry", entry_id=entry_id),
                           title=entry.title,
                           content=entry.content)

@app.route("/entry/<int:entry_id>/")
def show_entry(entry_id):
    entry = Entry.query.get(entry_id)
    comments = Comment.query.filter_by(entry_id=entry_id)
    return render_template("entry.html", entry=entry, comments=comments)

@app.route("/entry/<int:entry_id>/delete/")
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/entry/<int:entry_id>/comment/", methods=["POST"])
def create_comment(entry_id):
    author = request.form["author"]

    if not author:
        author = None

    comment = Comment(author=author,
                      content=request.form["content"],
                      entry_id=entry_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("show_entry", entry_id=entry_id))

@app.route("/entry/<int:entry_id>/comment/<int:comment_id>/")
@login_required
def delete_comment(entry_id, comment_id):
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("show_entry", entry_id=entry_id))

@app.route("/entry/search/")
def search_entries():
    q = request.args["q"]
    entries = Entry.query.filter(Entry.content.contains(q))
    return render_template("index.html", entries=entries)

@app.route("/entry/preview/", methods=["POST"])
@login_required
def show_preview():
    title = request.form["title"]
    content = request.form["content"]
    return render_template("preview.html", title=title, content=content)
