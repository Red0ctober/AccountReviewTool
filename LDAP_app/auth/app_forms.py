from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField, TextAreaField
from wtforms.validators import InputRequired

class LoginForm(Form):
	username = TextField('Username', [InputRequired()])
	password = PasswordField('Password', [InputRequired()])

class SearchForm(Form):
	search = TextField('Search', [InputRequired()])

class AddRemoveBtn(Form):
	submit = TextField('submit')
	affiliation = TextField('affiliation')

class EditPublicBtn(Form):
	edit_public_btn = TextField('edit_public_btn')

class EditPrivateBtn(Form):
	edit_private_btn = TextField('edit_private_btn')

class EditPublicForm(Form):
	editing_public_form = TextAreaField('editing_public', [InputRequired()])

class EditPrivateForm(Form):
	editing_private_form = TextAreaField('editing_private', [InputRequired()])
	private_affiliation = TextField('priv_affiliation', [InputRequired()])