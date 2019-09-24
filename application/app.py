"""
Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
users = []

# name=session.get("username", "Unknown")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
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
