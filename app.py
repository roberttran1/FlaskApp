from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/submit/")
def submit():
    return render_template("submit.html")


def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = 'CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)'
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    