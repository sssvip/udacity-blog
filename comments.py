"""
Comments domain module

this module to create the domain of Comments and manage the domain
"""
from google.appengine.ext import db
import hashlib


class Comments(db.Model):
    id = db.IntegerProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
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
    if blog_id == '' or blog_id is None:
        return "blog_id is not allowed be a null value"
    content = params.get('content', '')
    if content == '' or content is None:
        return "content is not allowed be a null value"
    comment = Comments(id=get_next_id(), blog_id=blog_id, username=username, content=content)
    comment.put()
    return "success"


# through the comment's id to update a comment
def update_comment(id, **params):
    # get the parmas defalut null value
    username = params.get('username', '')
    # there not check the foreigner key for username in account domain if necessary in later must be add there
    if username == '' or username is None:
        return "username is not allowed be a null value"
    blog_id = params.get('blog_id', '')
    if blog_id == '' or blog_id is None:
        return "blog_id is not allowed be a null value"
    content = params.get('content', '')
    if content == '' or content is None:
        return "content is not allowed be a null value"
    # start to update
    comment = Comments.all().filter("id =", int(id)).get()
    if comment is not None:
        # the first the comment is must existed in the db
        return "comment not existed"
    else:
        # update the value
        comment.content = content
        comment.put()
    return "success"


def get_comments_by_blog_id(blog_id):
    return Comments.all().filter("blog_id =", blog_id).order('-last_modified')


def get_comments_by_id(id):
    return Comments.all().filter("id =", id).get()


def get_all_comments():
    comments = Comments.all().order('-created')
    return comments
