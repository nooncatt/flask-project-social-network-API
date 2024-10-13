from . import app, USERS, models, POSTS
from flask import request, Response
import json
from http import HTTPStatus
import datetime


@app.route('/')
def index():
    return '<h1>hello world</h1>'


@app.post('/users/create')
def user_create():
    data = request.get_json()
    # data уже dict
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'total_reactions': user.total_reactions,
            'posts': user.posts,
        }), HTTPStatus.OK, mimetype='application/json'
    )
    return response

@app.get('/users/<int:user_id>')
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = USERS[user_id]
    response = Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'total_reactions': user.total_reactions,
            'posts': user.posts,
        }), HTTPStatus.OK, mimetype='application/json'
    )
    return response


@app.post('/posts/create')
def create_post():
    data = request.get_json()
    id = len(POSTS)
    author_id = data["author_id"]
    text = data["text"]
    time = str(datetime.datetime.now())

    if not models.Post.is_valid_text(text):
        return Response(status=HTTPStatus.BAD_REQUEST)

    if id < 0 or id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)

    post = models.Post(id, author_id, text, time, total_reactions=0)
    POSTS.append(post)

    # находим пользователя по author_id
    user = USERS[author_id]

    # добавляем пост пользователю
    user.create_post(post)

    response = Response(
        json.dumps({
            'id': post.id,
            'author_id': post.author_id,
            'text': post.text,
            'time': post.time,
            'total_reactions': post.total_reactions,
        }), HTTPStatus.OK, mimetype='application/json'
    )
    return response


@app.get('/posts/<int:post_id>')
def get_post(post_id):
    if post_id < 0 or post_id >= len(POSTS):
        return Response(status=HTTPStatus.NOT_FOUND)

    post = POSTS[post_id]
    response = Response(
        json.dumps({
            'id': post.id,
            'author_id': post.author_id,
            'text': post.text,
            'time': post.time,
            'total_reactions': post.total_reactions,
            'reactions': post.reactions,
        }), HTTPStatus.OK, mimetype='application/json'
    )
    return response

# todo: Поставить реакцию посту POST /posts/<post_id>/reaction