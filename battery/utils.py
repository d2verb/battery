from markdown import markdown
from battery.models import User

def markdown_to_html(mdtext):
    html = markdown(mdtext, extensions=["extra", "codehilite"])
    return html

def get_username(user_id):
    user = User.query.get(user_id)
    if user:
        return user.name
    else:
        return ""
