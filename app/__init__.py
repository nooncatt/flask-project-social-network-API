from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of type User
POSTS = []  # list for objects of type Post
from . import views

# import views
from . import models
