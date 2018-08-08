from battery.models import db, User, Entry, Comment
from flask import render_template, request, session, flash, redirect, url_for
from flask import g, jsonify, abort, Blueprint, current_app, send_file
from functools import wraps
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from datetime import datetime
from imghdr import test_png, test_jpeg, test_bmp, test_gif
from calendar import monthrange
from collections import defaultdict
import os

# There is no merit to use blueprint now
# I just don't want views.py depend on specific app object
bp = Blueprint("app", __name__)

def login_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            flash("You must log in first", "error")
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
    entries = Entry.query.order_by(Entry.created_at.desc()).all()
    return render_template("index.html", entries=entries)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]
    
    if not username or not password:
        flash("Username or password is empty", "error")
        return render_template("login.html")

    user, authenticated = User.authenticate(db.session.query,
                                            request.form["username"],
                                            request.form["password"])
    if authenticated:
        session["user_id"] = user.id
        flash("You were logged in", "info")
        return redirect(url_for("app.index"))
    else:
        flash("Invalid username or password", "error")
        return render_template("login.html")

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You were logged out", "info")
    return redirect(url_for("app.index"))

@bp.route("/entry/new/", methods=["GET", "POST"])
@login_required
def post_entry():
    if request.method == "GET":
        return render_template("editor.html", destination=url_for("app.post_entry"))

    title = request.form["title"]
    content = request.form["content"]
    save_as_draft = request.form.get("save-as-draft", False)

    if not title:
        flash("Title is empty", "error")
        return render_template("editor.html",
                               content=content,
                               destination=url_for("app.post_entry"))

    entry = Entry(title=request.form["title"],
                  content=request.form["content"],
                  user_id=session["user_id"],
                  is_public=not save_as_draft)

    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("app.show_entry", entry_id=entry.id))

@bp.route("/entry/<int:entry_id>/edit/", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get(entry_id)

    if entry is None:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))
    
    if g.user.id != entry.user_id:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    if request.method == "GET":
        return render_template("editor.html",
                               destination=url_for("app.edit_entry", entry_id=entry_id),
                               title=entry.title,
                               content=entry.content)

    title = request.form["title"]
    content = request.form["content"]
    save_as_draft = request.form.get("save-as-draft", False)

    if not title:
        flash("Title is empty", "error")
        return render_template("editor.html",
                               content=content,
                               destination=url_for("app.edit_entry", entry_id=entry_id))

    entry.title = request.form["title"]
    entry.content = request.form["content"]
    entry.is_public = not save_as_draft
    db.session.commit()

    return redirect(url_for("app.show_entry", entry_id=entry.id))

@bp.route("/entry/<int:entry_id>/")
def show_entry(entry_id):
    entry = Entry.query.get(entry_id)

    if entry is None:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    if not entry.is_public and (g.user is None or g.user.id != entry.user_id):
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    comments = Comment.query.filter_by(entry_id=entry_id)
    return render_template("entry.html", entry=entry, comments=comments)

@bp.route("/entry/<int:entry_id>/delete/")
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)

    if entry is None:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    if g.user.id != entry.user_id:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

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

@bp.route("/entry/<int:entry_id>/comment/<int:comment_id>/delete/")
@login_required
def delete_comment(entry_id, comment_id):
    entry = Entry.query.get(entry_id)

    if entry is None:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    if g.user.id != entry.user_id:
        flash("Entry not found", "error")
        return redirect(url_for("app.index"))

    comment = Comment.query.get(comment_id)

    if comment is None:
        flash("Comment not found", "error")
    else:
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


@bp.route("/data/<string:file_name>/", methods=["GET"])
def dowload_img(file_name):
    upload_dir = current_app.config["UPLOAD_DIR"]
    file_path = os.path.join(upload_dir, secure_filename(file_name))
    return send_file(file_path)

@bp.route("/data/upload/", methods=["GET", "POST"])
def upload_img():
    upload_dir = current_app.config["UPLOAD_DIR"]

    if request.method == "GET":
        files = os.listdir(upload_dir)
        return render_template("upload.html", files=files)

    file = request.files["file"]
    head = file.read(20)

    valid_type = False
    for test in (test_png, test_jpeg, test_bmp, test_gif):
        # I don't know whether the 2nd arg is valid or not.
        # these test function is defined at:
        #   https://hg.python.org/cpython/file/3.6/Lib/imghdr.py
        valid_type = valid_type or test(head, None)

    if not valid_type:
        flash("Invalid file type", "error")
    else:
        file_name = datetime.now().strftime("%Y%m%d_%H%M%S_") + secure_filename(file.filename)
        file.seek(0) # really need this?
        file.save(os.path.join(upload_dir, file_name))

    return redirect(url_for("app.upload_img"))

@bp.route("/data/delete/<string:file_name>/", methods=["GET"])
def delete_img(file_name):
    upload_dir = current_app.config["UPLOAD_DIR"]
    file_path = os.path.join(upload_dir, file_name)
    os.remove(file_path)
    return redirect(url_for("app.upload_img"))

@bp.route("/about/", methods=["GET"])
def about():
    return render_template("about.html")

def calc_archive_range(year, month=None, day=None):
    # set month range
    start_month = end_month = month
    if month is None:
        start_month = 1
        end_month = 12

    # set day range
    start_day = end_day = day
    if day is None:
        start_day = 1
        end_day = 31 if month is None else monthrange(year, month)[1]

    return (start_month, start_day, end_month, end_day)

@bp.route("/archive/", methods=["GET"])
def archive():
    entries = Entry.query.filter(Entry.is_public).order_by(Entry.created_at).all()

    if not entries:
      return render_template("archive.html", n_entries={})

    oldest_datetime = entries[0].created_at
    newest_datetime = entries[-1].created_at

    n_entries = defaultdict(lambda: [])
    for year in range(newest_datetime.year, oldest_datetime.year-1, -1):
        for month in range(12, 0, -1):
            start_day = 1
            _,end_day = monthrange(year, month)

            start_datetime = datetime(year, month, start_day, 0, 0, 0, 0)
            end_datetime = datetime(year, month, end_day, 23, 59, 59, 999)

            n = Entry.query.filter(start_datetime <= Entry.created_at,
                                   Entry.created_at <= end_datetime).count()

            if n == 0:
                continue

            n_entries[year].append((month, n))
    return render_template("archive.html", n_entries=n_entries)

@bp.route("/archive/<int:year>/<int:month>/<int:day>", methods=["GET"])
@bp.route("/archive/<int:year>/<int:month>", methods=["GET"])
@bp.route("/archive/<int:year>/", methods=["GET"])
def archive_with_datetime(year, month=None, day=None):
    start_month, start_day, end_month, end_day = calc_archive_range(year, month, day)

    # create datetime object
    start_datetime = datetime(year, start_month, start_day, 0, 0, 0, 0)
    end_datetime = datetime(year, end_month, end_day, 23, 59, 59, 999)

    # find entries
    entries = Entry.query.filter(start_datetime <= Entry.created_at,
                                 Entry.created_at <= end_datetime,
                                 Entry.is_public).all()
    return render_template("index.html", entries=entries)
