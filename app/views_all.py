from . import app, USERS

@app.route("/")
def index():
    return f"<h1>Hello, World!</h1><br>{USERS}"
# f"<h1>Hello, World!</h1><br>{USERS}<br>{[user.posts.to_dict() for user in USERS]}"