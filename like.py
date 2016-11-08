"""
Comments domain module include user like number for blog

this module to create the domain of Comments and manage the domain
"""
from google.appengine.ext import db
import hashlib


class Like(db.Model):
    id = db.IntegerProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    # 0:dislike 1:like
    islike = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)


def get_like_count():
    likes = db.GqlQuery("select * from Like")
    count = 0
    for like in likes:
        count += 1
    return count


# get the next id
def get_next_id():
    return get_like_count() + 1


# through the username and blog_id to update a like
# this must be sure the like is one through username and blog_id to find
def add_or_update_like(islike, **params):
    # get the parmas defalut null value
    username = params.get('username', '')
    # there not check the foreigner key for username in account domain if necessary in later must be add there
    if username == '' or username is None:
        return "username is not allowed be a null value"
    blog_id = params.get('blog_id', '')
    if blog_id == '' or blog_id is None:
        return "blog_id is not allowed be a null value"
    # start to update
    like = Like.all().filter("blog_id =", int(id)).filter("username =", username).get()
    if like is not None:
        # the like not exist,create one
        like = Like(id=get_next_id(), blog_id=blog_id, username=username, islike=islike)
        like.put()
    else:
        # update the value
        like.islike = islike
        like.put()
    return "success"


def get_like_count_by_blog_id(islike, blog_id):
    likes = Like.all().filter("blog_id =", blog_id).filter("islike =", islike)
    count = 0
    for like in likes:
        count = count + 1
    return count
