import ldap
from flask import request, render_template, flash, redirect, url_for, Blueprint, g
from flask.json import jsonify
from flask_login import current_user, login_user, logout_user, login_required
from LDAP_app import login_manager, db
from LDAP_app.auth.models import Login, User, get_ldap_connection, Search, SendMessage, back, PublicNote, PrivateNote
from LDAP_app.auth.app_forms import LoginForm, SearchForm, AddRemoveBtn, EditPublicBtn, EditPrivateBtn, EditPublicForm, EditPrivateForm
from operator import attrgetter


auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(id):
	return Login.query.get(int(id))

@auth.before_request
def get_current_user():
	g.user = current_user
	g.result = [('', {'': ''})]

@auth.route('/')
@auth.route('/home')
@auth.route('/index')
def home():
	return render_template('home.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():

	#allowed_users = []

	if current_user.is_authenticated:
		flash('You are already logged in.')
		return redirect(url_for('auth.home'))

	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():
		username = request.form.get('username')
		password = request.form.get('password')

		#if username in allowed_users:
		#Will only allow users in the designated list to log in
		try:
			Login.try_login(username, password)
		except ldap.INVALID_CREDENTIALS:
			flash('Invalid username or password. Please try again.', 'danger')
			return render_template('login.html', form=form)

		user = Login.query.filter_by(username=username).first()

		if not user:
			user = Login(username, password)
			db.session.add(user)
			db.session.commit()

		login_user(user)
		flash('You have successfully logged in.', 'success')
		return redirect(url_for('auth.home'))

	if form.errors:
		flash(form.errors, 'danger')

	return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	db.session.rollback()
	return redirect(url_for('auth.home'))

@auth.route('/search', methods=['GET', 'POST'])
@login_required
@back.anchor
def search():
	form = SearchForm(request.form)
	return render_template('search.html', form=form)

@auth.route('/results', methods=['GET', 'POST'])
@login_required
def results():
	form = SearchForm(request.form)

	if request.method == 'POST' and form.validate():
		search = request.form.get('search')
		user_input = 'uid=' + search + '*'

		try:
			Search(user_input)
			if g.user_info == []:
				flash('No results', 'danger')
			else:
				pass
		except ldap.LDAPError, e:
			print "LDAPError"
			flash(e, 'danger')

	return render_template('results.html', form=form)

@auth.route('/editpublicnote', methods=['GET', 'POST'])
@login_required
def editpublicnote():
	form = EditPublicBtn(request.form)
	editing_user = request.form.get('edit_public_btn')
	find_user = 'uid=' + editing_user
	Search(find_user)

	return render_template('editpublicnote.html', form=form)

@auth.route('/editprivatenote', methods=['GET', 'POST'])
@login_required
def editprivatenote():
	form = EditPrivateBtn(request.form)
	editing_user = request.form.get('edit_private_btn')
	find_user = 'uid=' + editing_user
	Search(find_user)

	return render_template('editprivatenote.html', form=form)

@auth.route('/commitpubnote', methods=['GET', 'POST'])
@login_required
def commitpubnote():
	form = EditPublicForm(request.form)
	note = request.form.get('editing_public_form')
	user_to_edit = request.form.get('username')

	public_username = PublicNote.query.filter_by(username=user_to_edit).first()
	try:
		if public_username.username == user_to_edit:	
			add_note = PublicNote.query.filter_by(username=user_to_edit).update(dict(public=note))
	except (AttributeError):
		user_and_note = PublicNote(user_to_edit, note) 
		db.session.add(user_and_note)
	db.session.commit()

	flash("Your note has been saved", "success")
	return back.redirect()

@auth.route('/commitprivnote', methods=['GET', 'POST'])
@login_required
def commitprivnote():
	form = EditPrivateForm(request.form)
	note = request.form.get('editing_private_form')
	user_to_edit = request.form.get('username')
	affil_to_edit = request.form.get('priv_affiliation')

	print affil_to_edit
	print note
	user = PrivateNote.query.filter_by(username=user_to_edit, affiliation=affil_to_edit).first()
	#private_username = PrivateNote.query.filter_by(username=user_to_edit).first()
	try:
		print 'trying'
		if user.username == user_to_edit and user.affiliation == affil_to_edit:
			print 'affil check'
			add_note = PrivateNote.query.filter_by(username=user_to_edit, affiliation=affil_to_edit).update(dict(private=note))
		else:
			print "adding"
			user_and_note = PrivateNote(user_to_edit, affil_to_edit, note) 
			db.session.add(user_and_note)
	except (AttributeError):
		print 'except'
		user_and_note = PrivateNote(user_to_edit, affil_to_edit, note) 
		db.session.add(user_and_note)
	db.session.commit()

	flash("Your note has been saved", 'success')
	return back.redirect()

@auth.route('/sociology', methods=['GET', 'POST'])
@login_required
@back.anchor
def sociology(): #Finds everyone with the Soc affiliation
	soc = Search('ssccAffiliation=soc')
	flash('Alphabetical by first name', 'success')
	return render_template('sociology.html')

@auth.route('/sscc', methods=['GET', 'POST'])
@login_required
@back.anchor
def sscc():
	sscc = Search('ssccAffiliation=staff')
	flash('Alphabetical by first name', 'success')
	return render_template('sscc.html')

@auth.route('/econ', methods=['GET', 'POST'])
@login_required
@back.anchor
def econ():
	econ = Search('ssccAffiliation=econ')
	flash('Alphabetical by first name', 'success')
	return render_template('econ.html')

@auth.route('/irp', methods=['GET', 'POST'])
@login_required
@back.anchor
def irp():
	irp = Search('ssccAffiliation=irp')
	flash('Alphabetical by first name', 'success')
	return render_template('irp.html')

@auth.route('/cows', methods=['GET', 'POST'])
@login_required
@back.anchor
def cows():
	cows = Search('ssccAffiliation=cows')
	flash('Alphabetical by first name', 'success')
	return render_template('cows.html')

@auth.route('/cde', methods=['GET', 'POST'])
@login_required
@back.anchor
def cde():
	cde = Search('ssccAffiliation=cde')
	flash('Alphabetical by first name', 'success')
	return render_template('cde.html')

@auth.route('/cdha', methods=['GET', 'POST'])
@login_required
@back.anchor
def cdha():
	cdha = Search('ssccAffiliation=cdha')
	flash('Alphabetical by first name', 'success')
	return render_template('cdha.html')

@auth.route('/polisci', methods=['GET', 'POST'])
@login_required
@back.anchor
def polisci():
	polisci = Search('ssccAffiliation=polisci')
	flash('Alphabetical by first name', 'success')
	return render_template('polisci.html')

@auth.route('/psych', methods=['GET', 'POST'])
@login_required
@back.anchor
def psych():
	psych = Search('ssccAffiliation=psych')
	flash('Alphabetical by first name', 'success')
	return render_template('psych.html')

@auth.route('/sohe', methods=['GET', 'POST'])
@login_required
@back.anchor
def sohe():
	sohe = Search('ssccAffiliation=sohe')
	flash('Alphabetical by first name', 'success')
	return render_template('sohe.html')

@auth.route('/uwsc', methods=['GET', 'POST'])
@login_required
@back.anchor
def uwsc():
	uwsc = Search('ssccAffiliation=uwsc')
	flash('Alphabetical by first name', 'success')
	return render_template('uwsc.html')

@auth.route('/wsob', methods=['GET', 'POST'])
@login_required
@back.anchor
def wsob():
	wsob = Search('ssccAffiliation=wsob')
	flash('Alphabetical by first name', 'success')
	return render_template('wsob.html')

@auth.route('/age', methods=['GET', 'POST'])
@login_required
@back.anchor
def age():
	age = Search('ssccAffiliation=age')
	flash('Alphabetical by first name', 'success')
	return render_template('age.html')

@auth.route('/all_users', methods=['GET', 'POST'])
@login_required
@back.anchor
def all_users():
	all_users = Search('ssccAffiliation=*')
	flash('Alphabetical by first name', 'success')
	return render_template('all_users.html')

@auth.route('/all_locked', methods=['GET', 'POST'])
@login_required
@back.anchor
def all_locked():
	all_locked = Search('ssccAccountLocked=TRUE')
	flash('Alphabetical by first name', 'success')
	return render_template('all_locked.html')

@auth.route('/sendmail', methods=['GET', 'POST'])
@login_required
def sendmail():
	this_user = User(current_user.username)
	form = AddRemoveBtn(request.form)
	affil = request.form.getlist('affiliation')
	sender = this_user.get_email()
	sender_name = this_user.get_name()
	action = request.form.get('submit')
	checked_users = request.form.getlist('checked')
	
	if checked_users == []:
		flash('No users checked', 'danger')
		return back.redirect()
	elif affil == []:
		flash('No affiliations checked', 'danger')
		return back.redirect()
	else:
		push_mail = SendMessage(sender, sender_name, affil, action, checked_users)
		flash('An email has been sent to the Help Desk', 'success')
		return back.redirect()