from flask import Flask, redirect, url_for, render_template, request, make_response
from item import bisHolyPaladin

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bis/holy-paladin')
def bisHP():
    test = bisHolyPaladin()
    return render_template('bis.html', items = test)
    

if __name__ == "__main__":
    app.run(debug=True)