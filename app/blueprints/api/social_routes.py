from os import error
from . import bp as api
from app.models import *
from flask import make_response, request, g
from app.blueprints.auth.auth import token_auth

#returns all the posts for them and the users they're following
@api.get('/posts')
# Same as if: @api.route ('posts', methods = ["GET"])
@token_auth.login_required
def get_all_posts():
    user = g.current_user
    posts = user.followed_posts()

    response_list = []
    for post in posts:
        post_dict = {
            'id':post.id,
            'body':post.body,
            'date_created':post.date_created,
            'date_updated':post.date_updated,
            'author': post.author.first_name + ' ' + post.author.last_name
        }
        response_list.append(post_dict)
    return make_response({'posts':response_list}, 200)

#returns a single post
#takes a post id
@api.get('/posts/<int:id>')
@token_auth.login_required()
def get_single_post(id):
    user = g.current_user
    post = Post.query.get(id)
    #check to make sure user has access to this post
    if not user.is_following(post.author) and not post.author.id == user.id:
        return make_response("Cannot get a post for someone the user is not following", 403)
    if not post:
        return make_response(f"Post ID: {id} does not exit", 404)
    else:
        response_dict = {
            'id':post.id,
            'body':post.body,
            'date_created':post.date_created,
            'date_updated':post.date_updated,
            'author': post.author.first_name + ' ' + post.author.last_name
        }
        return make_response(response_dict, 200) #don't need to convert to dict, because response_dict IS dict

#makes a new post
# {
#     "user_id":123,
#     "body":"the post body"
# }
@api.post('/posts')
@token_auth.login_required()
def post_post():
    posted_data = request.get_json()
    u = User.query.get(posted_data['user_id'])
    if not u:
        return make_response(f"User id: {posted_data['user_id']} does not exist", 404)
    if g.current_user.id != u.id:
        return make_response("You can only post for yourself", 403)
    post = Post(**posted_data)
    #** unpacks the dictionary as keyword arguments
    post.save()
    return make_response(f"Post id: {post.id} created", 200)

#delete a post
@api.delete('/posts')
@token_auth.login_required()
def delete_post():
    posted_data = request.get_json()
    post = Post.query.get(posted_data['id'])
    if not g.current_user.id == post.user_id:
        return make_response("You can only delete your own post", 403)
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist.", 404)
    post.delete()
    return make_response(f"Post id: {post} has been deleted", 200)

#update our post as a put request (tech a patch request)
@api.put('/posts')
@token_auth.login_required()
# {
#     'id':2
#     'body':"this is the body"
#     'user_id': 3
# } 
def put_post():
    posted_data= request.get_json()
    post = Post.query.get(posted_data['id'])
    if not post:
        return make_response(f"Post id: {posted_data['id']} does not exist.", 404)
    u = Post.query.get(posted_data['user_id'])
    if not u:
        return make_response(f"User id: {posted_data['user_id']} does not exist.", 404)
    if g.current_user.id != u.id:
        return make_response("You can only modify your own posts!", 403)
    post.user_id = posted_data['user_id']
    post.body = posted_data['body']
    post.save()
    return make_response(f"Post id: {post.id} has been changed.", 200)

