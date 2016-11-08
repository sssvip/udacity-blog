import webapp2
import json
import account
import cookie
class MainPage(webapp2.RequestHandler):
	def get(self):
		cookie.set_cookie(self,"test_user")

		temp_str=""
		for user in account.get_users():
			temp_str+=user.username+"----</br>"
		self.response.out.write("hello david"+temp_str+"cookie check result:"+self.request.cookies.get('user'))


app = webapp2.WSGIApplication([('/', MainPage),],
			debug=True)
