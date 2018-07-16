from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("battery.config")

db = SQLAlchemy(app)

import battery.views
