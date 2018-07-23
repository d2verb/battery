from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("battery.config")

db = SQLAlchemy(app)

import battery.views
from battery.utils import get_username, markdown_to_html

app.jinja_env.globals.update(get_username=get_username)
app.jinja_env.globals.update(markdown_to_html=markdown_to_html)
