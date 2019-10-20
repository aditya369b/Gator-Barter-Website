"""
Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""

from flask import Flask, render_template, request, session, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

# Database connection info. Note that this is not a secure connection.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#initialize the db connection
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

users = []
d = None

# name=session.get("username", "Unknown")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        pswd = request.form['password']    
        print(username, " tried to login")
        
        data = cursor.execute("SELECT * FROM user where u_email = %s", (username))
        print(data)
        conn.commit()
        return render_template("home.html",code=200)
    
    print("Simple Login Page Click")
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        pswd = request.form['password']    
        print(username, " tried to register")
        
        d = cursor.execute("INSERT INTO user (u_email, u_pass, u_fname, u_lname) Values (%s, %s, %s, %s)", (username, pswd, "akshay", "kasar"))
        print(d)
        conn.commit()
        return render_template("home.html")
    
    print("Simple Register Page Click")
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
