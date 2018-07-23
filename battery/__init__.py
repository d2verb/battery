from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("battery.config")

    from battery.models import db
    db.init_app(app)

    from battery.views import bp
    app.register_blueprint(bp)

    from battery.utils import get_username, markdown_to_html
    app.jinja_env.globals.update(get_username=get_username)
    app.jinja_env.globals.update(markdown_to_html=markdown_to_html)

    return app
