import ldap, smtplib
import functools
from flask import g, session, redirect, current_app, request, url_for
from flask_login import current_user
from LDAP_app import db, app 

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

def get_ldap_connection():
	conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
	return conn

class Login(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))

	def __init__(self, username, password):
		self.username = username

	@staticmethod
	def try_login(username, password):
		conn = get_ldap_connection()
		conn.simple_bind_s(
			'uid=%s,ou=People,dc=ssc,dc=wisc,dc=edu' % username, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

class User(object):

	def __init__(self, username):
		self.conn = get_ldap_connection()
		self.username = username

	def get_affiliation(self):
		filter = "uid=" + self.username
		return self.conn.search_s('ou=People,dc=ssc,dc=wisc,dc=edu', ldap.SCOPE_SUBTREE, filter, ['ssccAffiliation'])[0][1]['ssccAffiliation']

	def get_email(self):
		filter = "uid=" + self.username
		return self.conn.search_s('ou=People,dc=ssc,dc=wisc,dc=edu', ldap.SCOPE_SUBTREE, filter, ['mail'])[0][1]['mail'][0]

class Search:

	def __init__(self, find):
		user = User(current_user.username)
		dn = 'ou=People,dc=ssc,dc=wisc,dc=edu'
		attr = ['ssccMemberStatus', 'uid', 'mail', 'ssccAffiliation', 'cn', 'ssccAccountDeleted']
		filter = find
		conn = get_ldap_connection()
	
		user_info = conn.search_s(dn, ldap.SCOPE_SUBTREE, filter, attr)
		g.user_info = sorted(user_info, key=lambda user: user[1]['cn'][0]) #Sorts by user first name
		g.affil = user.get_affiliation()

class SendMessage:

	def __init__(self, sender, affiliation, action, users):
		self.sender = sender
		self.affiliation = affiliation
		self.action = action
		self.users = users
		receivers = ['ogiramma@ssc.wisc.edu']
	
		message = ("""From: Consult <%s> """ % self.sender +
"""To: Oliver <ogiramma@ssc.wisc.edu>
Subject: Test Email

Please %s """ % self.action +
"the %s affiliation(s) on the account(s): " % ", ".join(self.affiliation) + "%s" % ', '.join(self.users))
	
		try:
			smtpObj = smtplib.SMTP('localhost')
			smtpObj.sendmail(self.sender, receivers, message)
		except:
			print ("Error: unable to send")	


# This snippet is in public domain.
# However, please retain this link in your sources:
# http://flask.pocoo.org/snippets/120/
# Danya Alexeyevsky

class Back(object):
	cfg = app.config.get
	cookie = cfg('REDIRECT_BACK_COOKIE', 'back')
	default_view = cfg('REDIRECT_BACK_DEFAULT', 'auth.home')
	
	@staticmethod
	def anchor(func, cookie=cookie):
		@functools.wraps(func)
		def result(*args, **kwargs):
			session[cookie] = request.url
			return func(*args, **kwargs)
		return result
	
	@staticmethod
	def url(default=default_view, cookie=cookie):
		return session.get(cookie, url_for(default))
	
	@staticmethod
	def redirect(default=default_view, cookie=cookie):
		return redirect(back.url(default, cookie))

back = Back()