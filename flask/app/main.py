from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# from item import bisItemsExtract
from mats import matList
from user import *
from database import defaultBISDisplay, userBISDisplay, userBISProfileDisplay, queryItemsBySpecialization, queryObtainedItems, ObtainedBISList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bis.db'
app.secret_key = 'n04xMadeThisToScatterThroughTheWind'
db = SQLAlchemy(app)
user = SQLAlchemy(app)
# ========================================================
# Create bis_items class to handle database entries
# ========================================================
class bis_items(db.Model):
    Class = db.Column(db.String(20))
    Specialization = db.Column(db.String(50))
    ID = db.Column(db.String(10), primary_key = True)
    Slot = db.Column(db.String(15))
    Name = db.Column(db.String(100))
    Source = db.Column(db.String(100))
    Location = db.Column(db.String(50))
    Quality = db.Column(db.String(20))

    def __init__(self, item_class, item_spec, item_slot, item_name, item_src, item_loc, item_quality):
        self.Class = item_class
        self.Specialization = item_spec
        self.ID = item_id
        self.Slot = item_slot
        self.Name = item_name
        self.Source = item_src
        self.Location = item_loc
        self.Quality = item_quality

class USER_BIS(user.Model):
    Name = user.Column(user.String(50))
    ID = user.Column(db.String(10), primary_key = True)

    def __init__(self, user_name, user_id):
        self.Name = user_name
        self.ID = user_id

# ========================================================
# HOME PAGE
# ========================================================
@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('bis.html')
    return render_template('index.html')

# ========================================================
# BEST-IN-SLOT ROUTES
# ========================================================
@app.route('/bis')
def bis():
    return render_template('bis.html')

@app.route('/bis-result', methods = ['POST', 'GET'])
def bisDB():
    if request.method == 'POST':
        if 'holy_paladin' in request.form:
            bis_class = 'Paladin'
            bis_specialization = 'Holy'
        elif 'ret_paladin' in request.form:
            bis_class = 'Paladin'
            bis_specialization = 'Retribution'

        if 'username' in session:
            # rows = userBISDisplay(bis_class, bis_specialization)
            obtained = ObtainedBISList(bis_items, USER_BIS, bis_class, bis_specialization)
            rows = queryItemsBySpecialization(bis_items, bis_class, bis_specialization)
        else:
            # rows = defaultBISDisplay(bis_class, bis_specialization)
            rows = queryItemsBySpecialization(bis_items, bis_class, bis_specialization)
            obtained = []
            for i in range(len(rows)):
                obtained.append(0)

    return render_template('bis-result.html', results=zip(rows, obtained))

    
# ========================================================
# FARMING ROUTES
# ========================================================
@app.route('/farming')
def farm():
    return render_template('farming.html')

@app.route('/farming-result', methods = ['POST', 'GET'])
def farmResult():
    if request.method == 'POST':
        materials = dict()
        mat_lists = matList()
        item_id = None
        for i in range(len(mat_lists)):
            if request.form.get("Name") == mat_lists[i].name:
                item_id = mat_lists[i].item_id
                for m in mat_lists[i].mats:
                    print(m)
                    print(mat_lists[i].mats)
                    materials[m] = int(request.form.get('Amount')) * mat_lists[i].mats[m]
        return render_template('farming-result.html', item_id = item_id, materials = materials, name = request.form.get("Name"), amount = request.form.get("Amount"))

# ========================================================
# LOGIN ROUTES
# ========================================================
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        session['username'] = request.form['username']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['username'] = username
            # session['user_id'] = user.id
            return redirect(url_for('bis'))

        return redirect(url_for('login'))
    
    return render_template('login.html')

# ========================================================
# PROFILE ROUTE
# ========================================================
@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if not session.get('username') is None:
        username = session.get('username')
        rows = queryObtainedItems(USER_BIS)
        return render_template('profile.html', result=rows)
    return "You are not logged in <br><a href='/login'>"+ "Click here to login</a>"

# ========================================================
# ALWAYS ADD ROUTE BEFORE THE IF-STATEMENT BELOW
# ========================================================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=(5000))