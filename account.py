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
    # users = db.GqlQuery("select * from User order by created desc")
    users = User.all().order('-created')
    return users


def delete_all():
    # users = db.GqlQuery("select * from User")
    users = User.all()
    for user in users:
        user.delete()


# add a user into database
# return the result status string: success or faild infomation
def add_user(**params):
    # get the parmas defalut none value
    username = params.get('username', 'none')
    # check username
    if check_username(username) != 'success':
        return check_username(username)
    password = params.get('password', 'none')
    # check password
    if password == 'none' or password == '' or password is None:
        return "password is none is not allowed"
    email = params.get('email', '')
    u = User(username=username, password=password, email=email)
    u.put()
    # print username
    return "success"


# check the username
def check_username(username):
    # check None
    if username == '' or username == 'none' or username is None:
        return "username is none is not allowed "
    # check existed
    user = User.all().filter('username =', username).get()
    if user is not None:
        return "username existed"
    else:
        return "success"


# encrypt_password
def encrypt_password(password):
    pass


def prepare_insert_sql(**params):
    pass


# log in blog
# if log in success return the user
# log in faile return the faild information
def login(**params):
    username = params.get('username', 'none')
    if check_username(username) != "username existed":
        return "username not existed"
    else:
        password = params.get('password', 'none')
        # check password none
        if password is None or password == 'none':
            return "password is none"
        # log in check
        u = User.all().filter("password =", password).filter("username =", username).get()
        if u is not None:
            # log in success
            return u
        else:
            return "username or password incorrect"
