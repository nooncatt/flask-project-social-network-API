# models.py
import re


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
    # todo: Создание поста POST /posts/create
    def create_post(self):
        post_number = len(self.posts)

