from flask import Flask

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        app.config.from_object("battery.config")
    else:
        app.config.from_mapping(config)

    from battery.models import db
    db.init_app(app)
    db.create_all(app=app)

    from battery.views import bp
    app.register_blueprint(bp)

    from battery.utils import get_username, markdown_to_html
    app.jinja_env.globals.update(get_username=get_username)
    app.jinja_env.globals.update(markdown_to_html=markdown_to_html)

    return app
