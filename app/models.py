import re
import datetime
from . import USERS, POST_COUNTER  # Глобальная переменная доступна из __init__.py


class User:
    def __init__(self, id, first_name, last_name, email, total_reactions=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.total_reactions = total_reactions  # todo: sum of reactions for all user's posts пока что сколько оставил сам
        self.posts = []  # Храним посты внутри пользователя

    @staticmethod
    def is_valid_email(email):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            return True
        else:
            return False

    def create_post(self, text):
        global POST_COUNTER  # todo: delete text global
        post_id = POST_COUNTER  # Используем глобальный счетчик для уникальных id
        POST_COUNTER += 1  # Увеличиваем глобальный счетчик для следующего поста

        time = str(datetime.datetime.now())
        new_post = Post(post_id, self.id, text, time)
        self.posts.append(new_post)
        # Обновляем общее количество реакций после создания нового поста
        self.update_total_reactions()

        return new_post

    def get_post(self, post_id):
        for post in self.posts:
            if post.id == post_id:
                return post
        return None

    def update_total_reactions(self):
        total_reactions = sum(post.total_reactions for post in self.posts)
        # for post in self.posts:
        #     total_reactions += post.total_reactions  # суммируем реакции для всех постов
        self.total_reactions = total_reactions  # обновляем общее количество реакций

    @staticmethod
    def is_valid_id(user_id):
        if user_id < 0 or user_id >= len(USERS):
            return False
        return True


class Post:
    def __init__(self, id, author_id, text, time, total_reactions=0):
        self.id = id  # Уникальный id для всех постов
        self.author_id = author_id
        self.text = text
        self.time = time
        self.reactions = []
        self.total_reactions = total_reactions  # total react for this post

    @staticmethod
    def is_valid_text(text):
        if text is None or len(text) < 5:
            return False
        return True

    def add_reaction(self, reaction):
        if isinstance(reaction, Reaction):
            self.reactions.append(reaction)  # (reaction.react_to_dict())

    def raise_total_reactions(self):
        self.total_reactions += 1

    @staticmethod
    def post_to_dict(post):
        return {
            "id": post.id,
            "author_id": post.author_id,
            "text": post.text,
            "time": post.time,
            "reactions": [
                reaction.react_to_dict() for reaction in post.reactions
            ],  # Преобразуем в словари
            "total_reactions": post.total_reactions,
        }


class Reaction:
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

    def react_to_dict(self):
        return {"user_id": self.user_id, "reaction": self.reaction}
