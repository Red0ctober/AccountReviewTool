from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////www/web/sscc/flaskLDAP/LDAP_app/tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'Developement Key'
app.config['LDAP_PROVIDER_URL'] = 'ldaps://ldap.ssc.wisc.edu'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)

app.secret_key = 'random_developement_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from LDAP_app.auth.views import auth
app.register_blueprint(auth)

db.create_all()