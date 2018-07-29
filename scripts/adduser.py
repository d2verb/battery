import sys
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from battery import create_app
from battery.models import db, User
from sqlalchemy.exc import IntegrityError

if __name__ == "__main__":
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        app = create_app()
        with app.app_context():
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            print("Done !!")
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print("{} is already used".format(username))
    except:
        print("Something wrong")
