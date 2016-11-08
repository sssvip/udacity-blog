"""
blog domain module
"""
from google.appengine.ext import db
import hashlib


class Blog(db.Model):
    id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


def get_blogs_count():
    blogs = db.GqlQuery("select * from Blog")
    count = 0
    for blog in blogs:
        count += 1
    return count


# get the next id
def get_next_id():
    return get_blogs_count() + 1


def add_blog(**params):
    # get the parmas defalut null value
    username = params.get('username', '')
    # there not check the foreigner key for username in account domain if necessary in later must be add there
    if username == '' or username is None:
        return "username is not allowed be a null value"
    title = params.get('title', '')
    if title == '' or title is None:
        return "title is not allowed be a null value"
    content = params.get('content', '')
    if content == '' or content is None:
        return "content is not allowed be a null value"
    blog = Blog(id=get_next_id(), username=username, title=title, content=content)
    blog.put()
    return "success"


def get_blogs():
    blogs = Blog.all().order('-created')
    return blogs


def get_blog_by_username(username):
    return Blog.all().filter("username =", username).get()
