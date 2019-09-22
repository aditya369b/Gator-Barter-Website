"""
Code Taken From: https://github.com/tecladocode/simple-flask-template-app
"""

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", name=session.get("username", "Unknown"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    # Here you could register the user.
    # Add them to a database, for example.
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about/about.html")

@app.route("/about/abodi")
def abodi():
    return render_template("about/abodi.html")

@app.route("/about/akasar")
def akasar():
    return render_template("about/akasar.html")

@app.route("/about/akohanim")
def akohanim():
    return render_template("about/akohanim.html")

@app.route("/about/ang")
def ang():
    return render_template("about/ang.html")

@app.route("/about/dyan")
def dyan():
    return render_template("about/dyan.html")

@app.route("/about/pyu")
def pyu():
    return render_template("about/pyu.html")

@app.route("/about/tbelsare")
def tbelsare():
    return render_template("about/tbelsare.html")

if __name__ == "__main__":
    app.run("0.0.0.0")
