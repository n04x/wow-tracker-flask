from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3

from item import bisItemsExtract
from mats import matList
from user import *
from database import defaultBISDisplay, userBISDisplay

app = Flask(__name__)
app.secret_key = 'n04xMadeThisToScatterThroughTheWind'

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
            print('logged in')
            rows = userBISDisplay(bis_class, bis_specialization)
        else:
            rows = defaultBISDisplay(bis_class, bis_specialization)
    
    return render_template('bis-result.html', rows=rows)

    
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
# ALWAYS ADD ROUTE BEFORE THE IF-STATEMENT BELOW
# ========================================================
if __name__ == "__main__":
    app.run(debug=True)