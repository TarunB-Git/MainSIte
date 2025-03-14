from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, login_required, logout_user, LoginManager, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="STUDENTK",
    password="bytew0rld",
    hostname="STUDENTK.mysql.pythonanywhere-services.com",
    databasename="STUDENTK$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = "iammagic"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

class Rules(db.Model):

    __tablename__ = "rules"

    id = db.Column(db.Integer, primary_key=True)
    rule_desc = db.Column(db.String(4096))

class Transacs(db.Model):
    __tablename__ = "transacs"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

class Accounts(db.Model):

    __tablename__ = "accs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    acc_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    dob = db.Column(db.DateTime)
    address = db.Column(db.String(4096))

class Issues(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, primary_key=True)
    transacid = db.Column(db.Integer, db.ForeignKey('transacs.id'), nullable=True)
    ruleid = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=True)
    rule = db.relationship('Rules', foreign_keys=ruleid)
    transac = db.relationship('Transacs', foreign_keys=transacid)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    comment = Comment(content=request.form["contents"], commenter=current_user)

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/temp")

def temp():

    celsius = request.args.get("celsius", "")

    if celsius:

        kelvin = kelvin_from(celsius)
        fahrenheit = fahrenheit_from(celsius)
    else:

        kelvin = ""
        fahrenheit = ""
    return (

        """<form action="" method="get">

                Celsius temperature: <input type="text" name="celsius">

                <input type="submit" value="Convert to Kelvin and Fahrenheit">

            </form>"""

        + "Celsius: "

        + celsius

        + "<br>Kelvin: "

        + kelvin


        + "<br>Fahrenheit: "

        + fahrenheit


    )

def kelvin_from(celsius):

    try:

        kelvin = float(celsius) - 273.15

        kelvin = round(kelvin, 1)

        return str(kelvin)

    except ValueError:

        return "Invalid Input"


def fahrenheit_from(celsius):

    """Convert Celsius to Fahrenheit degrees."""

    try:

        fahrenheit = float(celsius) * 9 / 5 + 32

        fahrenheit = round(fahrenheit, 3)  # Round to three decimal places

        return str(fahrenheit)

    except ValueError:

        return "Invalid Input"

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))