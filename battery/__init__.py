from flask import Flask
import pathlib
import os

config = {
    "development": "battery.config.Development",
    "testing": "battery.config.Testing",
    "production": "battery.config.Production"
}

def configure_app(app):
    config_name = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    if app.config["INSTANCE_PATH"] is not None:
        app.instance_path = app.config["INSTANCE_PATH"]
    else:
        project_root = pathlib.Path(__file__).parent.parent
        app.instance_path = os.path.join(project_root, "instance")

    # setup db path and upload dir dynamically
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}/battery.db".format(app.instance_path)
    UPLOAD_DIR = os.path.join(app.instance_path, "upload")

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI,
        UPLOAD_DIR = UPLOAD_DIR 
    )

    # user defined configuration
    if os.path.exists(os.path.join(app.instance_path, "config.py")):
        app.config.from_pyfile("config.py", silent=True)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config["UPLOAD_DIR"])
    except OSError:
        pass


    from battery.models import db
    db.init_app(app)
    db.create_all(app=app)

    from battery.views import bp
    app.register_blueprint(bp)

    from battery.utils import get_username, markdown_to_html
    app.jinja_env.globals.update(get_username=get_username)
    app.jinja_env.globals.update(markdown_to_html=markdown_to_html)

    return app
