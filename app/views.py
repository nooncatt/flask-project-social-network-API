from . import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus
import datetime


@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"


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
        mimetype="application/json"
    )
    return response


@app.get("/users/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[user_id]
    posts_as_dict = [post.post_to_dict(post) for post in user.posts]  # Преобразуем каждый пост в словарь

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
        mimetype="application/json"
    )
    return response


@app.post("/posts/create")
def create_post():
    data = request.get_json()
    author_id = data["author_id"]
    text = data["text"]

    if not models.User.is_valid_id(author_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.Post.is_valid_text(text):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = USERS[author_id]
    post = user.create_post(text)  # Создаем пост для пользователя с уникальным id

    response = Response(
        json.dumps(
            {
                "id": post.id,  # Уникальный id на уровне всей системы
                "author_id": post.author_id,
                "text": post.text,
                "time": post.time,
                "total_reactions": post.total_reactions,
                "reactions": post.reactions,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json"
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    for user in USERS:
        post = user.get_post(post_id)
        if post:
            response = Response(
                json.dumps(post.post_to_dict(post)),  # Преобразуем объект Post в словарь перед сериализацией в JSON

                # json.dumps(
                #     {
                #         "id": post.id,
                #         "author_id": post.author_id,
                #         "text": post.text,
                #         "time": post.time,
                #         "total_reactions": post.total_reactions,
                #         "reactions": post.reactions,
                #     }
                #),
                status=HTTPStatus.OK,
                mimetype="application/json"
            )
            return response
    return Response(status=HTTPStatus.NOT_FOUND)


@app.post("/posts/<int:post_id>/reaction")
def create_reaction(post_id):
    data = request.get_json()
    user_id = data["user_id"]  # expect int
    reaction_str = data["reaction"]  # expect str

    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if not models.Reaction.is_valid_reaction(reaction_str):
        return Response(status=HTTPStatus.BAD_REQUEST)


    # todo: change reaction if user send second request (firstly delete
    #  and then can send the next reaction request)

    for user in USERS:
        post = user.get_post(post_id)
        if post:
            # Проверка, оставил ли пользователь уже реакцию
            for existing_reaction in post.reactions:
                if existing_reaction.user_id == user_id:
                    # Удаляем старую реакцию
                    post.reactions.remove(existing_reaction)
                    post.total_reactions -= 1  # Уменьшаем общее количество реакций на 1
                    break  # Выходим из цикла, чтобы добавить новую реакцию

            post_reaction = models.Reaction(user_id, reaction_str)
            post.add_reaction(post_reaction)

            post.raise_total_reactions()  # Увеличиваем количество реакций для поста

            # Обновляем total_reactions только для пользователя
            user.update_total_reactions()  # Обновляем общее количество реакций для пользователя

            return Response(status=HTTPStatus.OK)

    return Response(status=HTTPStatus.NOT_FOUND)
