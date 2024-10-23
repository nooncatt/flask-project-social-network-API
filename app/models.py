# models.py
import re
from . import POSTS, USERS


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions # todo: не количество оставленных реакций, а кол-во полученных общее
        self.posts = []

    @staticmethod
    def is_valid_email(email):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return True
        else:
            return False

    def create_post(self, post):
        new_post = Post.post_to_dict(post)
        self.posts.append(new_post)

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True

    def raise_total_reactions(self):
        self.total_reactions += 1


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
        if text is None or len(text) < 5:
            return False
        return True

    @staticmethod
    def is_valid_id(post_id):
        if post_id < 0 or post_id >= len(POSTS):
            return False
        return True

    @staticmethod
    def post_to_dict(post):
        return {
            "post_id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "time": post.time,
            "reactions": post.reactions,
            "total_reactions": post.total_reactions,
        }

    # todo: reactions for the post (смайлики библиотека ?)

    def add_reaction(self, post_reaction):
        # Убедитесь, что post_reaction — это экземпляр Reaction
        if isinstance(post_reaction, Reaction):
            self.reactions.append(Reaction.react_to_dict(post_reaction))

            author = USERS[self.author_id]  # Получаем автора поста
            author.total_reactions += 1  # Увеличиваем общее количество полученных реакций
        else:
            raise TypeError("Expected a Reaction object.")

    def raise_total_reactions(self):
        self.total_reactions += 1


class Reaction:
    # Список допустимых реакций
    ALLOWED_REACTIONS = [
        "like",
        "heart",
        "haha",
        "wow",
        "sad",
        "angry",
        "dislike",
        "boom",
    ]

    def __init__(self, user_id, reaction):
        self.user_id = user_id
        self.reaction = reaction

    @staticmethod
    def is_valid_reaction(reaction):
        if reaction is not None and reaction in Reaction.ALLOWED_REACTIONS:
            return True
        return False

    @staticmethod
    def react_to_dict(react):
        # Преобразуем объект Reaction в словарь
        return {
            "user_id": react.user_id,
            "reaction": react.reaction
        }