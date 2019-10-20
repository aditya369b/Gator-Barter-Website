"""
Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""

import gatorProduct as product  # class made by alex
from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
import jinja2
import bleach  # sql santization lib

app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'


# mysql = MySQL()
# mysql.init_app(app)conn = mysql.connect()
# cursor = conn.cursor()

# Open database connection
db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                     app.config['MYSQL_DATABASE_USER'],
                     None, app.config['MYSQL_DATABASE_DB'])

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

# alex tests


# disconnect from server

# name=session.get("username", "Unknown")
@app.route("/", methods=["POST", "GET"])
def home():
    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'], None,
                         app.config['MYSQL_DATABASE_DB'])

# prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Open database connection
    cursor.execute("""
    SELECT i.*, ii.ii_url, ii.ii_status FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    WHERE i.i_status = 1
    AND i.i_sold_ts IS NULL;
    """)
    # cursor.execute("SELECT * FROM item;")
    data = cursor.fetchall()
    print("All items?", data)
    productList = []
    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)
    return render_template("home.html", products=productList)


@app.route("/products/<product_id>", methods=["POST", "GET"])
def productPage(product_id):

    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'],
                         None, app.config['MYSQL_DATABASE_DB'])

    cursor = db.cursor()
    product_id = str(bleach.clean(product_id))  # sanitizing a bad redirect

    # Open database connection

    query = """
    SELECT i.*, ii.ii_url, ii.ii_status FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    WHERE i.i_id = """ + product_id + """;"""

    cursor.execute(query)
    # cursor.execute("SELECT * FROM item;")
    data = cursor.fetchall()
    print("Redirecting to Product page", product_id)
    print(data[0])
    productObject = product.makeProduct(data[0])
    return render_template("products/product.html", product=productObject)


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


db.close()

if __name__ == "__main__":
    app.run("0.0.0.0")
