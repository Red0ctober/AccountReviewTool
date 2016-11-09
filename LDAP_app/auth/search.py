#Search Class
from flask_login import current_user, login_user, logout_user, login_required
from LDAP_app import login_manager, db
from LDAP_app.auth.models import User, LoginForm, SearchForm, get_ldap_connection

class Search(find):
	dn = 'ou=People,dc=ssc,dc=wisc,dc=edu'
	attr = ['ssccMemberStatus', 'uid', 'mail', 'ssccAffiliation', 'cn', 'ssccAccountDeleted']

	filter = find

	conn = get_ldap_connection()

	user_info = conn.search_s(dn, ldap.SCOPE_SUBTREE, filter, attr)
	g.user_info = sorted(user_info, key=lambda user: user[1]['cn'][0]) #Sorts by user first name

	return g.user_info