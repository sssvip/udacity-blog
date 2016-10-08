"""
cookie module
"""
import hashlib

cookie_salt = 'udacity-cookie'


def encrypt_cookie(cookie_content):
    return hashlib.md5(cookie_content + cookie_salt).hexdigest()


# set cookie to the web through the 'web' that is the web handler
# cookie_content str type eg: user
def set_cookie(web, cookie_content):
    web.response.headers.add_header('Set-Cookie',
                                    'user=' + cookie_content + '|' + encrypt_cookie(cookie_content))


# check user whether log in
# return true or false for log in status
def check_cookie(web):
    userinfo = web.request.cookies.get('user')
    if userinfo is None:
        return False
    username = userinfo.split('|')[0]
    encrypted_cookie = userinfo.split('|')[1]
    return encrypt_cookie(username) == encrypted_cookie
