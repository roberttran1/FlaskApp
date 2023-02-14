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

