from flask import Flask, render_template,request,redirect,url_for
from models import db,User
from routes_tickets import ticketsRouting
from forms import LoginForm
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_migrate import Migrate

app = Flask(__name__)

app.register_blueprint(ticketsRouting)

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
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html",form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
	# If a post request was made, find the user by 
	# filtering for the username
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
		# Check if the password entered is the 
		# same as the user's password
        if user and user.check_password(form.password.data):
        # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("index"))
		    # Redirect the user back to the home
		    # (we'll create the home route in a moment)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)