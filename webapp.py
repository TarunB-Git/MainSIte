from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
    send_from_directory
)
import requests
from flask import jsonify
import json
import os
import logging
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField, BooleanField
#from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from flask_bcrypt import Bcrypt
from flask import Response
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
import base64
from io import BytesIO
from matplotlib.figure import Figure
import csv
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_login import UserMixin
from flask_login import LoginManager

app = Flask(__name__)
UPLOAD_FOLDER = 'images/'
UPLOADS_FOLDER = 'uploads/'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
ALLOWED_EXTENSIONS= ['.txt', '.csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif' ]


app = Flask(__name__)
app.secret_key = 'magic'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class User:
    def __init__(self, userid, username, password):
        self.userid = userid
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(userid=1, username='Admin', password='MTK'))
users.append(User(userid=2, username='Guest', password='noob'))
users.append(User(userid=3, username='Member', password='EMBER'))

@app.before_request
def before_request():
    g.user = None

    if 'user_userid' in session:
        user = [x for x in users if x.userid == session['user_userid']][0]
        g.user = user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_userid', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_userid'] = user.userid
            return redirect(url_for('profile'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

@app.route('/')
def index():

    return render_template('index.html')
# Constants
FULL_TICKET_PRICE = 500
HALF_TICKET_PRICE = 250
TOUR_GUIDE_COST = 200
DISCOUNT_10_PERCENT = 0.10
DISCOUNT_20_PERCENT = 0.20
INDIAN_DISCOUNT = 0.90
SAARC_DISCOUNT = 0.50

# Dummy database for nationalities
SAARC_COUNTRIES = ['Bangladesh', 'Nepal', 'Sri Lanka', 'Pakistan', 'Bhutan', 'Maldives']

# Global variable to store booking data
booking_data = {}

# Helper function to check if the museum is open
def is_museum_open(date, timeslot):
    weekday = date.weekday()
    if weekday >= 5:  # 5 is Saturday, 6 is Sunday
        return False
    if not (9 <= timeslot.hour < 18):
        return False
    return True
@app.route('/hbd')
def hbd():

    return render_template('hbd.html')
@app.route('/chat')
def chat():
    return render_template('gpt2.html')


@app.route('/home')
def home():

    return render_template('home.html')

@app.route("/home.png")
def dash():

        fig = Figure()
        fig.set_figwidth(15)
        fig.set_figheight(3)
        axis1 = fig.add_subplot(1, 6, 1)
        axis2 = fig.add_subplot(1, 6, 3)
        axis3 = fig.add_subplot(1, 6, 5)

        fig.tight_layout()

        p = np.array([55, 15, 30])
        mylab = ["Tasks", "Open", "Overdue"]
        mylabel = ["Tasks", "", ""]
        mylabels = ["Tasks", "", ""]

        #myexplode = [0.2, 0, 0]

        axis1.pie(p, labels = mylab, shadow = True)
        axis2.pie(p, labels = mylabel,  shadow = True)
        axis3.pie(p, labels = mylabels, shadow = True)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/aml')
def aml():

    return render_template('aml.html')

@app.route("/aml.png")
def aml_png():

        fig = Figure()
        fig.set_figwidth(10)
        fig.set_figheight(4)
        axis1 = fig.add_subplot(1, 4, 2)
        axis2 = fig.add_subplot(1, 4, 4)

        fig.tight_layout()

        p = np.array([55, 15, 30])
        mylab = ["Tasks", "", "Overdue"]
        mylabel = [" Low Tasks", "Critical", "Major"]

        #myexplode = [0.2, 0, 0]

        axis1.pie(p, labels = mylab, shadow = True)
        axis2.pie(p, labels = mylabel,  shadow = True)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route('/rules')
def rules():

    return render_template('rules.html')

@app.route('/analytics1')
def analytics():

    return render_template('analytics.html')
@app.route('/analytics2')
def analytics2():

    return render_template('analyticstwo.html')

@app.route('/analytics2success', methods = ['GET','POST'])
def asu():
        try:
            f = request.files['file']
            if f:
                extension = os.path.splitext(f.filename)[1].lower()

                if extension not in ALLOWED_EXTENSIONS:
                   return 'File not allowed'

                file_path = os.path.join(UPLOADS_FOLDER,secure_filename(f.filename))
                f.save(file_path)
        except RequestEntityTooLarge:
            return 'File larger than 16MB limit'

        fig = Figure()
        ax = fig.add_subplot(2,2,1)
        axis1 = fig.add_subplot(2, 2, 2)
        axis2 = fig.add_subplot(2, 2, 3)
        axis3 = fig.add_subplot(2, 2, 4)

        p = np.array([35, 25, 25, 15])
        mylabels = ["Sepa", "HighRisk Regions", "Indemnity", "Account Risk"]
        myexplode = [0.2, 0, 0, 0]

        x = []
        y = []
        xpoints = []
        ypoints = []




        with open(file_path, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                x.append(row[1])
                y.append(row[2])
                xpoints.append(row[0])
                ypoints.append(row[3])

        # Generate the figure **without using pyplot**.

        ax.plot(x,y)
        axis1.scatter(xpoints, ypoints,  marker="o")
        axis2.plot(xpoints, ypoints)
        axis3.pie(p, labels = mylabels, explode = myexplode, shadow = True)
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        img = f"data:image/png;base64,{data}"
        #output = io.BytesIO()
        #FigureCanvas(fig).print_png(output)
        #return Response(output.getvalue(), mimetype='image/png')
        return render_template("success.html", name= f.filename, imf = img)

@app.route('/analytics3')
def analytics3():

    return render_template('analytics3.html')

@app.route("/analytics.png")
def analytics_png():

        fig = Figure()
        axis1 = fig.add_subplot(2, 2, 1)

        xpoints = [1,3,5,7,4,2]
        ypoints = [2,3,7,10,3,1]


        #myexplode = [0.2, 0, 0]

        axis1.plot(xpoints, ypoints)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

@app.route("/analyticstwo")
def analytics2_png():

    return render_template("analyticstwo.html")



@app.route("/analytics3.png")
def analytics3_png():

        fig = Figure()
        axis1 = fig.add_subplot(2, 2, 1)
        x = [3,5,6,9]
        y = [2,3,4,2]
        xpoints = [1,3,5,7,4,2]
        ypoints = [2,3,7,10,3,1]
        axis1.bar(x, y)
        axis1.plot(x, y)
        axis1.bar(xpoints, ypoints)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')


@app.route('/reports')
def reports():

    return render_template('reports.html')

@app.route('/blog', methods=['GET', 'POST'])
def posts():

    all_posts = BlogPost.query.order_by(desc(BlogPost.date_posted)).all()
    return render_template('posts.html', posts=all_posts)

@app.route('/blog/delete/<int:id>')
def delete(id):

    if not g.user:
        return redirect(url_for('login'))

    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/blog')

@app.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('edit.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if not g.user:
        return redirect(url_for('login'))

    if request.method == 'POST':

        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/blog')
    else:
        return render_template('create.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tandc')
def terms():

    return render_template('tanc.html')


@app.route('/proj')
def proj():
    return render_template("proj.html")

@app.route('/success', methods = ['GET','POST'])
def success():
        try:
            f = request.files['file']
            if f:
                extension = os.path.splitext(f.filename)[1].lower()

                if extension not in ALLOWED_EXTENSIONS:
                   return 'File not allowed'

                file_path = os.path.join(UPLOADS_FOLDER,secure_filename(f.filename))
                f.save(file_path)
        except RequestEntityTooLarge:
            return 'File larger than 16MB limit'

        fig = Figure()
        ax = fig.add_subplot(2,2,1)
        axis1 = fig.add_subplot(2, 2, 2)
        axis2 = fig.add_subplot(2, 2, 3)
        axis3 = fig.add_subplot(2, 2, 4)

        p = np.array([35, 25, 25, 15])
        mylabels = ["Sepa", "HighRisk Regions", "Indemnity", "Account Risk"]
        myexplode = [0.2, 0, 0, 0]

        x = []
        y = []
        xpoints = []
        ypoints = []




        with open(file_path, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:
                x.append(row[1])
                y.append(row[2])
                xpoints.append(row[0])
                ypoints.append(row[3])

        # Generate the figure **without using pyplot**.

        ax.plot(x,y)
        axis1.scatter(xpoints, ypoints,  marker="o")
        axis2.plot(xpoints, ypoints)
        axis3.pie(p, labels = mylabels, explode = myexplode, shadow = True)
        # Save it to a temporary buffer.
        #buf = BytesIO()
        #fig.savefig(buf, format="png")
        # Embed the result in the html output.
        #data = base64.b64encode(buf.getbuffer()).decode("ascii")
        #img = f"data:image/png;base64,{data}"
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
        #return render_template("success.html", name= f.filename, imf = img)

@app.route('/post', methods = ['GET','POST'])
def post():
  files = os.listdir(UPLOAD_FOLDER)
  images = []

  for file in files:
    #if os.path.splitext(file)[1].lower() in ALLOWED_EXTENSIONS:
        images.append(file)
  return render_template('image.html', images=images)

@app.route('/upload', methods = ['POST'])
def upload():
  try:
    file = request.files['file']
    if file:
      #extension = os.path.splitext(file.filename)[1].lower()

      #if extension not in ALLOWED_EXTENSIONS:
        #return 'File is not an image.'
      file.save(os.path.join(
        UPLOAD_FOLDER,
        secure_filename(file.filename)
      ))

  except RequestEntityTooLarge:
    return 'File is larger than the 16MB limit.'

  return redirect('/post')

@app.route('/ss/<filename>', methods=['GET'])
def serve_image(filename):
   return send_from_directory(UPLOAD_FOLDER, filename)



if __name__ == "__main__":

    app.run(debug=True)

