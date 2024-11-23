from flask import request, Response
from .. import app, USERS
from .. import models
import json
from http import HTTPStatus


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
        mimetype="application/json",
    )
    return response


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    for user in USERS:
        post = user.get_post(post_id)
        if post:
            response = Response(
                json.dumps(
                    post.post_to_dict(post)
                ),  # Преобразуем объект Post в словарь перед сериализацией в JSON
                # json.dumps(
                #     {
                #         "id": post.id,
                #         "author_id": post.author_id,
                #         "text": post.text,
                #         "time": post.time,
                #         "total_reactions": post.total_reactions,
                #         "reactions": post.reactions,
                #     }
                # ),
                status=HTTPStatus.OK,
                mimetype="application/json",
            )
            return response
    return Response(status=HTTPStatus.NOT_FOUND)



