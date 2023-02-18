from flask import Flask
from flask import render_template, abort, redirect, url_for
from flask import request, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html") # renders homepage

@app.route("/submit/", methods=["POST","GET"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else: # performs code if method is "POST"
        get_message_db() # creates db if doesn't exist
        insert_message(request) # adds message to db
        return render_template("submit.html", message = request.form["message"], name = request.form["name"])

@app.route("/view/", methods=["GET"])
def view():
    messages = random_messages(5) # gets 5 random messages to display
    return render_template("view.html", messages=messages)


def get_message_db():
    try:
        return g.message_db # checks to see if db exists
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = 'CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)'
        cursor = g.message_db.cursor()
        cursor.execute(cmd) # creates table with three columns
        return g.message_db

def insert_message(request):
    db = get_message_db()
    message = request.form['message'] # parses request to get values for table
    name = request.form['name']
    db = sqlite3.connect("messages_db.sqlite")
    cmd = 'INSERT INTO messages (handle, message) VALUES(\"{0}\", \"{1}\")'.format(name, message)
    cursor = db.cursor()
    cursor.execute(cmd) # adds row to table
    db.commit()


def random_messages(n):
    cmd = 'SELECT * FROM messages ORDER BY RANDOM() LIMIT {0};'.format(n)
    db = get_message_db() # fetches db
    cursor = db.cursor()
    cursor.execute(cmd)
    rows = cursor.fetchall() # fetch messages from db
    messages = [(row[1],row[2]) for row in rows] # add messages to a list
    db.close() # close connection
    return messages