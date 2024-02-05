from flask import Flask, redirect, render_template, session, flash
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, User, db, Feedback
from forms import RegisterUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "123456"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
    """Homepage redirects to register"""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def add_user():
    """User register form; handle adding."""

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template(
            "/users/register.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    if "username" in session:
            return redirect("/secret")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            # on successful login, redirect to secret page adn store user in session
            session['username'] = user.username

            return redirect(f"/users/{user.username}")

        else:
            # re-render the login page with an error
            form.username.errors = ["Bad name/password"]
            return render_template("/users/login.html", form=form)

    return render_template("/users/login.html", form=form)

    
@app.route("/logout")
def logout():

    session.pop("username")
    return redirect("/")
        
@app.route("/users/<username>")
def show_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)

    return render_template("users/show.html", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("/feedback/add.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    feedback = Feedback.query.get(feedback_id)

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")


@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    app.run(debug=True)
