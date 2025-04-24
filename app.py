from flask import Blueprint,Flask, render_template,request,redirect,url_for
from models import db,User
from routes_tickets import ticketsRouting
from routes_auth import authRouting
from forms import LoginForm
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_migrate import Migrate

app = Flask(__name__)

app.register_blueprint(ticketsRouting)
app.register_blueprint(authRouting)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'clave_secreta'
migrate = Migrate(app, db)

db.init_app(app)

# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.get_user(user_id)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)