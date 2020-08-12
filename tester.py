from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

users = {
    "n04x": {
        "username": "n04x",
        "email": "n04x@contoso.com",
        "password": "example",
        "bio": "some random guy from internet"
    },
    "mela101": {
        "username": "mela101",
        "email": "mela101@contoso.com",
        "password": "p0tat0",
        "bio": "i love potatoes"
    },
    "bobcashflow": {
        "username": "bobcashflow",
        "email": "bobcashflow@contoso.com",
        "password": "bob101",
        "bio": "Bob Cashflow, I am rich"
    }
}
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href= '/sign-out'>Click here to logout</a></b>"
    return "You are not logged in <br><a href='/sign-in'>"+ "Click here to login</a>"

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        req = request.form

        username = req.get('username')
        print(username)
        password = req.get('password')

        if not username in users:
            print('username not found')
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user['password']:
            print('Incorrect password')
            return redirect(request.url)
        else:
            session['USERNAME'] = user['username']
            print('session username set')
            return redirect(url_for('profile'))
    
    return render_template('sign-in.html')

@app.route('/profile')
def profile():

    if not session.get('USERNAME') is None:
        username = session.get('USERNAME')
        user = users[username]
        return render_template('profile.html', user=user)
    else:
        print("No username found in session")
        return redirect(url_for("sign_in"))

@app.route('/sign-out')
def sign_out():
    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))

if __name__ == "__main__":
    app.run(debug=True)