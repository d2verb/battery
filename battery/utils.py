from markdown import markdown
from battery.models import User

def markdown_to_html(mdtext):
    html = markdown(mdtext,
                    extensions=["extra", "codehilite"],
                    extension_configs = {
                        "codehilite": {
                            "linenums": True,
                            "pygments_style": "colorful",
                            "noclasses": True,
                        }
                    })
    return html

def get_username(user_id):
    user = User.query.get(user_id)
    if user:
        return user.name
    else:
        return ""

def regist_user(name, password, app=None):
    from battery.models import db

    if app is None:
        from battery import create_app
        app = create_app()
    
    with app.app_context():
        user = User(name=name, password=password)
        db.session.add(user)
        db.session.commit()
