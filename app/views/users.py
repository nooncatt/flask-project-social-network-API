from flask import request, Response
from .. import app, USERS
from .. import models
import json
from http import HTTPStatus



@app.post("/users/create")
def user_create():
    data = request.get_json()

    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user_id = len(USERS)  # id for new user
    user = models.User(user_id, first_name, last_name, email)
    USERS.append(user)

    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    posts_as_dict = [
        post.post_to_dict(post) for post in user.posts
    ]  # Преобразуем каждый пост в словарь

    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": posts_as_dict,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


