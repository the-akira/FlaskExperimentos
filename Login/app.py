from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

# >>> from app import db, User
# >>> db.create_all()
# >>> gabriel = User(username='Gabriel')
# >>> db.session.add(gabriel)
# >>> db.session.commit()
# >>> results = User.query.all()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'chave-secreta'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    user = User.query.filter_by(username='Gabriel').first()
    login_user(user)
    return 'You are now logged in...'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

@app.route('/home')
@login_required
def home():
    return f'O usuário atual é {current_user.username}'

if __name__ == '__main__':
    app.run(debug=True)