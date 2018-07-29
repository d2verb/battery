import sys, os
sys.path.insert(0, "/home/d2verb/battery")

os.environ["FLASK_ENV"] = "production"

from battery import create_app
application = create_app()
