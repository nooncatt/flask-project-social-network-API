from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of type User
POST_COUNTER = 0  # global post counter that guarantees unique IDs

from . import models
from . import views_all
from . import views