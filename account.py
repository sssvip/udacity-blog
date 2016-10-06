"""
user module
"""
from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


# init some users for test program
def init_users():
    for x in range(0, 10):
        u = User(username="user" + str(x), password="123", email="mail@qq.com")
        u.put()


def get_users_count():
    users = db.GqlQuery("select * from User")
    count = 0
    for user in users:
        count += 1
    return count


def get_users():
    users = db.GqlQuery("select * from User order by created desc")
    return users


def delete_all():
    users = db.GqlQuery("select * from User")
    for user in users:
        user.delete()
