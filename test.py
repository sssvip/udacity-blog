"""
test module for all module to test
"""

import webapp2
import json
import account
import cookie
import templateUtils
import re
import strUtils
import blog
import comments
from datetime import datetime


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/welcome")


# welcome   cookie test (include templates test)
class Welcome(webapp2.RequestHandler):
    def get(self):
        if (self.request.cookies.get('user') is None):
            # not login redirect to the signup.html to login
            self.redirect("/signup")
        self.response.out.write(templateUtils.reder_str("welcome.html", username=cookie.get_username(self)))


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(templateUtils.reder_str("signup.html"))

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        # this is order to hold the value of username and email to the front
        params = dict(username=username, email=email)
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True
        else:  # through the first step check,and should to check in db whether existed
            result = account.check_username(username)
            if result != 'success':
                params['error_username'] = result
                have_error = True
        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True
        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True
        if have_error:
            self.response.out.write(templateUtils.reder_str("signup.html", **params))
        else:
            # signup success set the cookie to this brower
            account.add_user(username=username, password=password, email=email)
            cookie.set_cookie(self, username)
            self.redirect('/welcome')


# login to the blog system
class Login(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(templateUtils.reder_str("login.html"))

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        params = dict(username=username)
        # is not necessary to check username,because next step check it
        # check_result = account.check_username(username)
        # if check_result == 'success':
        #     params['error_username'] = "username not existed"
        #     have_error = True
        login_result = account.login(username=username, password=password)
        # if return type is str indicate login error
        if strUtils.is_str(login_result):
            params['error_password'] = login_result
            have_error = True
        if have_error:
            self.response.out.write(templateUtils.reder_str("login.html", **params))
        else:
            # signup success set the cookie to this brower
            cookie.set_cookie(self, login_result.username)
            self.redirect('/welcome')


# this is to logout this blog system
class Logout(webapp2.RequestHandler):
    def get(self):
        cookie.clear_cookie(self)
        self.redirect('/signup')


# this is to test to list all users in the db
class AllUsers(webapp2.RequestHandler):
    def get(self):
        userss = account.get_users()
        usernames = ""
        for user in userss:
            usernames += str(user.username) + "--" + str(user.password) + "--" + str(user.email) + "--" + str(
                user.created) + "<br>"
        self.response.write(usernames)


# this is to add blog
class Addblog(webapp2.RequestHandler):
    def get(self):
        # check user login
        cookie.check_login(self)
        self.response.write(templateUtils.reder_str("addblog.html"))

    def post(self):
        # check user login
        cookie.check_login(self)
        title = self.request.get('title', '')
        content = self.request.get('content', '')
        params = dict(title=title, content=content)
        if title == '' or content == '':
            params['error'] = "title or content is not allowed null value"
        # through the check and add the blog to db
        params['username'] = cookie.get_username(self)
        result = blog.add_blog(**params)
        if result == 'success':
            self.redirect('/blog')
        else:
            params['error'] = result
            self.response.write(templateUtils.reder_str("addblog.html", **params))


# this is to list all blogs in the db
class AllBlogs(webapp2.RequestHandler):
    def get(self):
        blogs_with_comments = list()
        blogs = blog.get_blogs()
        for temp_blog in blogs:
            temp_blog.comments = list()
            all_comments = comments.get_comments_by_blog_id(temp_blog.id)
            # all_comments = comments.get_all_comments()
            if all_comments is not None:
                for comment in all_comments:
                    temp_blog.comments.append(comment)
                    # add this blog all comments to this blog
                    # temp_blog.comments.append(all_comments)
            blogs_with_comments.append(temp_blog)
        params = dict(blogs=blogs_with_comments)
        self.response.write(templateUtils.reder_str("blog.html", **params))


# this is interface to the ajax deliver data
class Comment(webapp2.RequestHandler):
    def get(self):
        pass

    # through post method to add a comment
    def post(self):
        content = self.request.get("content", '')
        if content == '':
            self.response.write("content value is not allowed null value");
            return
        blog_id = self.request.get("blog_id", '')
        if blog_id == '':
            self.response.write("blog_id value is not allowed null value");
            return
        # check username
        username = cookie.get_username(self)
        if username is False:
            self.response.write("please login...");
            return
        result = comments.add_comment(blog_id=int(blog_id), username=username, content=content)
        self.response.write(result);

    # through put method to update comment
    def put(self):
        self.response.write("put method success");


# this is to test to list all comment in the db
class AllComments(webapp2.RequestHandler):
    def get(self):
        commentss = comments.get_all_comments()
        temp_str = ""
        for comment in commentss:
            temp_str += str(comment.id) + "--" + str(comment.blog_id) + "--" + str(comment.username) + "--" + str(
                comment.content) + "--" + str(comment.created) + "<br>"
        self.response.write(temp_str)


app = webapp2.WSGIApplication(
    [('/', MainPage), ('/welcome', Welcome), ('/signup', Signup), ('/login', Login), ('/logout', Logout),
     ('/allusers', AllUsers), ('/addblog', Addblog), ('/blog', AllBlogs), ('/comment', Comment),
     ('/allcomments', AllComments)],
    debug=True)
