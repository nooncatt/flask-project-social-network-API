from . import app, USERS, models, POSTS
from flask import request, Response
import json
from http import HTTPStatus
import datetime


@app.route("/")
def index():
    return "<h1>hello world</h1>"


@app.post("/users/create")
def user_create():
    data = request.get_json()
    # data уже dict
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, last_name, email)
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
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
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
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    post_id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    time = str(datetime.datetime.now())

    if not models.Post.is_valid_text(text):  # то есть is_valid не True
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.User.is_valid_id(author_id):  # means we do not have such user
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = models.Post(post_id, author_id, text, time, total_reactions=0)
    POSTS.append(post)

    # находим пользователя по author_id
    user = USERS[author_id]

    # добавляем пользователю ссылку на пост
    user.create_post(post)

    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "time": post.time,
                "reactions": post.reactions,
                "total_reactions": post.total_reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    if not models.Post.is_valid_id(post_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    post = POSTS[post_id]
    response = Response(
        json.dumps(
            {
                "id": post.id,
                "author_id": post.author_id,
                "text": post.text,
                "time": post.time,
                "reactions": post.reactions,
                "total_reactions": post.total_reactions,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.post("/posts/<int:post_id>/reaction")
def create_reaction(post_id):
    data = request.get_json()
    user_id = data["user_id"]  # expect int
    reaction_str = data["reaction"]  # expect str


    if not models.Post.is_valid_id(post_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.Reaction.is_valid_reaction(reaction_str):
        return Response(status=HTTPStatus.BAD_REQUEST)


    post = POSTS[post_id]

    # check if one user can have only one reaction
    for existing_reaction in post.reactions:
        if existing_reaction["user_id"] == user_id:
            return Response(
                status=HTTPStatus.CONFLICT,
                response=json.dumps({"error": "User has already reacted to this post"}),
                mimetype='application/json')


    user = USERS[user_id]

    post_reaction = models.Reaction(user_id, reaction_str)
    post.add_reaction(post_reaction)

    post.raise_total_reactions()  # someone's post received reaction
    user.raise_total_reactions()  # sb who added reaction

    return Response(status=HTTPStatus.OK)



# todo: Получение всех постов пользователя, отсортированных по количеству реакций GET /users/<user_id>/posts
