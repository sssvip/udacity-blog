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
    last_modified = db.DateTimeProperty(auto_now=True)

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


def update_blog(**params):
    # get the parmas defalut null value
    username = params.get('username', '')
    # there not check the foreigner key for username in account domain if necessary in later must be add there
    if username == '':
        return "username is not allowed be a null value"
    title = params.get('title', '')
    if title == '':
        return "title is not allowed be a null value"
    content = params.get('content', '')
    if content == '':
        return "content is not allowed be a null value"
    blog_id = params.get('blog_id', '')
    if blog_id == '':
        return "blog_id is null value"
    blog = Blog.all().filter("blog_id =", blog_id)
    if blog is None:
        return "blog is not existed"
    # check the blog whether belong current user
    if blog.username != username:
        return "you can't update other's blog"
    blog.content = content
    blog.title = title
    blog.put()
    return "success"


def get_blogs():
    blogs = Blog.all().order('-last_modified')
    return blogs


def get_blog_by_username(username):
    return Blog.all().filter("username =", username).order('-last_modified')


def get_blog_by_id(id):
    return Blog.all().filter("id =", id).get()
