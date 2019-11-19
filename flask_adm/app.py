from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
	return User.query.get(user_id)

# >>> from app import db, User
# >>> db.create_all()
# >>> gabriel = User(name='Gabriel')
# >>> db.session.add(gabriel)
# >>> db.session.commit()
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))

class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

@app.route('/login')
def login():
	user = User.query.get(1)
	login_user(user)
	return 'Logged In'

@app.route('/logout')
def logout():
	logout_user()
	return 'Logged Out'

if __name__ == '__main__':
	app.run(debug=True, port=8787)