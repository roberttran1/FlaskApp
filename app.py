from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/submit/", methods=["POST","GET"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else:
        get_message_db()
        insert_message(request)
        return render_template("submit.html", message = request.form["message"], name = request.form["name"])

@app.route("/view/")
def view():
    return render_template("view.html", message = random_messages(5))


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
    db = get_message_db()
    message = request.form['message']
    name = request.form['name']
    try:
        return g.message_db
    except:
        db = sqlite3.connect("messages_db.sqlite")
        cmd = 'INSERT INTO messages VALUES(COUNT(*), name, message)'
        cursor = db.cursor()
        cursor.execute(cmd)
        cursor.commit()


def random_messages(n):
    cmd = 'SELECT * FROM messages ORDER BY RANDOM() LIMIT {0};'.format(n)
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute(cmd)
    rows = cursor.fetchall()
    messages = [(row[1],row[2]) for row in rows]
    cursor.close()
    return messages