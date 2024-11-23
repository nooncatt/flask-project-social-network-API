from flask import request, Response
from .. import app, USERS
from .. import models
from http import HTTPStatus



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
            # checking if the user has already left a reaction
            for existing_reaction in post.reactions:
                if existing_reaction.user_id == user_id:
                    # delete an existing reaction
                    post.reactions.remove(existing_reaction)
                    post.total_reactions -= 1  # reducing the total number of reactions by 1
                    break  # exit the loop to add a new reaction

            post_reaction = models.Reaction(user_id, reaction_str)
            post.add_reaction(post_reaction)

            post.raise_total_reactions()  # increasing the number of reactions for the post

            # update total_reactions only for user
            user.update_total_reactions()  # update total reactions for the user

            return Response(status=HTTPStatus.OK)

    return Response(status=HTTPStatus.NOT_FOUND)
