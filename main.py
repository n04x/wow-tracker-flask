from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3

from item import bisItemsExtract
from mats import matList
app = Flask(__name__)
app.secret_key = 'any random string'
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



# @app.route('/bis-result', methods = ['POST', 'GET'])
# def bisCSV():
#     if 'holy_paladin' in request.form:
#         bis_class = 'Paladin'
#         bis_specialization = 'Holy'
#         bis_items = bisItemsExtract(bis_class, bis_specialization)
#     elif 'ret_paladin' in request.form:
#         bis_class = 'Paladin'
#         bis_specialization = 'Retribution'
#         bis_items = bisItemsExtract(bis_class, bis_specialization)
    
#     return render_template('bis-result.html', items = bis_items, bis_specialization=bis_specialization, bis_class=bis_class)

@app.route('/bis-result', methods = ['POST', 'GET'])
def bisDB():
    if request.method == 'POST':
        if 'holy_paladin' in request.form:
            bis_class = 'Paladin'
            bis_specialization = 'Holy'
        elif 'ret_paladin' in request.form:
            bis_class = 'Paladin'
            bis_specialization = 'Retribution'


        db_con = sqlite3.connect('bis.db')
        db_con.row_factory = sqlite3.Row

        db_cur = db_con.cursor()
        db_cur.execute("SELECT * FROM BIS WHERE Class = ? AND Specialization = ?", (bis_class, bis_specialization))
        rows = db_cur.fetchall()
    
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
        # if request.form.get('Name') == result[0].name:
        #     for m in result[0].mats:
        #         materials[m] = int(request.form.get('Amount')) * int(result[0].mats[m])
        return render_template('farming-result.html', item_id = item_id, materials = materials, name = request.form.get("Name"), amount = request.form.get("Amount"))

# ========================================================
# LOGIN ROUTES
# ========================================================


# ========================================================
# ALWAYS ADD ROUTE BEFORE THE IF-STATEMENT BELOW
# ========================================================
if __name__ == "__main__":
    app.run(debug=True)