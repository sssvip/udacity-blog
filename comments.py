"""
Comments domain module include user like number for blog

this module to create the domain of Comments and manage the domain
"""
from google.appengine.ext import db
import hashlib


class Comments(db.Model):
    id = db.IntegerProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    # 0:default 1:like 2:dislike
    like = db.IntegerProperty()
    content = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)


def get_comment_count():
    comments = db.GqlQuery("select * from Comments")
    count = 0
    for comment in comments:
        count += 1
    return count


# get the next id
def get_next_id():
    return get_comment_count() + 1


def add_comment(**params):
    # get the parmas defalut null value
    username = params.get('username', '')
    # there not check the foreigner key for username in account domain if necessary in later must be add there
    if username == '' or username is None:
        return "username is not allowed be a null value"
    blog_id = params.get('blog_id', '')
    like = params.get('like', 0)
    if blog_id == '' or blog_id is None:
        return "blog_id is not allowed be a null value"
    content = params.get('content', '')
    if content == '' or content is None:
        return "content is not allowed be a null value"
    comment = Comments(id=get_next_id(), blog_id=blog_id, like=like, username=username, content=content)
    comment.put()
    return "success"


def get_comments_by_blog_id(blog_id):
    return Comments.all().filter("blog_id =", blog_id)


def get_all_comments():
    comments = Comments.all().order('-created')
    return comments
