# This snippet is in public domain.
# However, please retain this link in your sources:
# http://flask.pocoo.org/snippets/120/
# Danya Alexeyevsky

from flask import session, redirect, current_app


cfg = current_app.config.get
cookie = cfg('REDIRECT_BACK_COOKIE', 'back')
default_view = cfg('REDIRECT_BACK_DEFAULT', 'index')

def anchor(func, cookie=cookie):
	@functools.wraps(func)
	def result(*args, **kwargs):
		session[cookie] = request.url
		return func(*args, **kwargs)
	return result

def url(default=default_view, cookie=cookie):
	return session.get(cookie, url_for(default))

def redirect(default=default_view, cookie=cookie):
	return redirect(back.url(default, cookie))