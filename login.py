
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

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')