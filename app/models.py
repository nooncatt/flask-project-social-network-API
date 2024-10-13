# models.py
import re
from . import POSTS


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        else:
            return False

    def create_post(self, post):
        new_post = dict()
        new_post["id"] = post.id
        new_post["author_id"] = post.author_id
        new_post["text"] = post.text
        new_post["time"] = post.time
        new_post["total_reactions"] = post.total_reactions
        new_post["reactions"] = post.reactions

        self.posts.append(new_post) # или просто post.text

class Post:
    def __init__(self, id, author_id, text, time, total_reactions=0):
        self.author_id = author_id
        self.text = text
        self.id = id
        self.time = time
        self.reactions = []
        self.total_reactions = total_reactions
    @staticmethod
    def is_valid_text(text):
        if text is None or len(text)<5:
            return False
        return True

    # todo: reactions for the post (смайлики библиотека)


