from flask import Blueprint,redirect,url_for,render_template,session,g
from models import User,db
from forms import LoginForm
from flask_login import login_required,login_user,logout_user,current_user

authRouting = Blueprint('auth', __name__)
@authRouting.route('/register', methods=["GET", "POST"])
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
        return redirect(url_for("auth.login"))
    # Renders register template if user made a GET request
    return render_template("auth/register.html",form=form)

@authRouting.route("/login", methods=["GET", "POST"])
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
    return render_template("auth/login.html", form=form)

@authRouting.before_app_request
def load_logged_in_user():
    if current_user.is_authenticated:
        g.user = User.get_user(current_user.id)
    else:
        g.user = None

@authRouting.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))