from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import InputRequired

class LoginForm(Form):
	username = TextField('Username', [InputRequired()])
	password = PasswordField('Password', [InputRequired()])

class SearchForm(Form):
	search = TextField('Search', [InputRequired()])

class AddRemoveBtn(Form):
	submit = TextField('submit')
	affiliation = TextField('affiliation')