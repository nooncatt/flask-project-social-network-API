from . import app, USERS, models
from flask import request, Response
import json
@app.route('/')
def index():
    return '<h1>hello world</h1>'

@app.post('/user/create')
def user_create():
    data = request.get_json()
    # data уже dict
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']

    # todo: check thr phone and email for validity

    user = models.User(id, first_name, last_name, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email' : user.email
        }), статус, хедеры, mimetipe = 'application/json')


