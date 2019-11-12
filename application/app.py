"""
Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""


import gatorProduct as product  # class made by alex
import gatorUser as user

from flask import Flask, render_template, request, session, redirect, url_for, abort
from about_info import dev
import pymysql
import jinja2
import bleach  # sql santization lib

import hashlib
import time

# from livereload import Server   # PHILIPTEST

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
# app.config['DEBUG'] = 'True'    # PHILIPTEST


# mysql = MySQL()
# mysql.init_app(app)conn = mysql.connect()
# cursor = conn.cursor()


# Open database connection
db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                     app.config['MYSQL_DATABASE_USER'],
                     app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_DB'])

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

# testuser

cursor.execute("SELECT * FROM user WHERE user.u_is_admin=1 LIMIT 1;")
testUser = user.makeUser(cursor.fetchone())

# name=session.get("username", "Unknown")
@app.route("/", methods=["POST", "GET"])
def home():
    productList = []
    return render_template("home.html", products=productList, feedback="")


@app.route('/results', methods=['POST', 'GET'])
def searchPage():
    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'], app.config['MYSQL_DATABASE_PASSWORD'],
                         app.config['MYSQL_DATABASE_DB'])

# prepare a cursor object using cursor() method
    cursor = db.cursor()

    print(len(request.form))

    formsLen = len(request.form)

    feedback, data = "", ""
    if formsLen > 0:
        search = request.form['text']

        search = str(bleach.clean(search))  # sanitizing a bad search
        # Open database connection
        starting = "" + search + "%"
        ending = "%" + search + ""
        starting2 = " " + search + "%"
        ending2 = "%" + search + " "
        middle = "%" + search + "%"
        exact = search
        cursor.execute("""
        SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
        FROM item AS i
        JOIN item_image AS ii
        ON i.i_id = ii.ii_i_id
        JOIN category as c
        ON c.c_id = i.i_c_id
        WHERE i.i_status = 1
        AND i.i_sold_ts IS NULL
        AND (i.i_desc LIKE '""" + starting + """'
        OR i.i_desc LIKE '""" + ending + """'
        OR i.i_desc LIKE '""" + starting2 + """'
        OR i.i_desc LIKE '""" + ending2 + """'
        OR i.i_desc LIKE '""" + middle + """'
        OR i.i_desc LIKE '""" + exact + """');
        """)
        # cursor.execute("SELECT * FROM item;")
        data = cursor.fetchall()
        print("All items?", data)
    productList = []

    if len(data) == 0:
        if formsLen > 0:
            feedback = "No Results, Consider these Items"
        cursor.execute("""
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    WHERE i.i_status = 1
    AND i.i_sold_ts IS NULL;
    """)
    # cursor.execute("SELECT * FROM item;")
        data = cursor.fetchall()

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)
    if feedback == "" and formsLen != 0:
        if len(data) == 1:
            feedback = str(len(data)) + " Result Found"
        else:
            feedback = str(len(data)) + " Results Found"

    return render_template("home.html", products=productList, feedback=feedback)


@app.route("/products/<product_id>", methods=["POST", "GET"])
def productPage(product_id):

    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'],
                         app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_DB'])

    cursor = db.cursor()
    product_id = str(bleach.clean(product_id))  # sanitizing a bad redirect

    # Open database connection

    query = """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    WHERE i.i_id = """ + product_id + """
    AND i.i_status >= 0;"""

    cursor.execute(query)
    # cursor.execute("SELECT * FROM item;")
    data = cursor.fetchall()
    if len(data) == 0:
        abort(404)
        # return redirect("/")

    query = """
    SELECT u.u_id, u.u_email, u.u_fname, u.u_lname, i.i_u_id FROM user AS u
    JOIN item as i
    ON i.i_u_id = u.u_id;
    """
    cursor.execute(query)
    userObject = cursor.fetchone()

    print(userObject)

    print(data[0])
    productObject = product.makeProduct(data[0])
    if productObject.getStatus() == 0 and not testUser.isAdmin():
        abort(404)
    print("Redirecting to Product page", product_id)
    return render_template("products/product.html", product=productObject, user=userObject)


@app.route("/categories/<categoryName>", methods=["POST", "GET"])
def selectCategory(categoryName):
    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'],
                         app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_DB'])

    cursor = db.cursor()
    print(categoryName)

    query = """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    HAVING c.c_name = '""" + categoryName + """'
    AND i.i_status = 1;"""

    cursor.execute(query)
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)

    productList = []

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    return render_template("home.html", products=productList, feedback=categoryName)


@app.route("/login", methods=['GET', 'POST'])
def login():
    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'],
                         app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_DB'])

    cursor = db.cursor()
    
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['pwd']    
        print(email, " tried to login")
        
        #u.u_id, u.u_email, u.u_fname, u.u_lname, u.u_is_admin
        query = """
        SELECT * 
        FROM user u 
        WHERE u_email = %(email)s
        AND u_status = 1"""
        
        cursor.execute(query, {'email':email})
        data = cursor.fetchone()
        if data is None:
            print("User not found!")
            return render_template("login.html", code=404, message = "Page Not Found")
        print(data)
        userObject = user.makeUser(data)
        
        if pwd == userObject.u_pwd:
            print("Authentication Successful")
            return render_template("home.html",code=200, userObject = userObject, message = "Success")
        else:
            print("Authentication Failed!")
            return render_template("login.html", code=401, message = "Unauthorized")
        
    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    
    db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                         app.config['MYSQL_DATABASE_USER'],
                         app.config['MYSQL_DATABASE_PASSWORD'], app.config['MYSQL_DATABASE_DB'])
    cursor = db.cursor()
    
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        created_ts = time.strftime('%Y-%m-%d %H:%M:%S')
        updated_ts = time.strftime('%Y-%m-%d %H:%M:%S')
        
        
        #check if user already exists
        query = """
        SELECT * 
        FROM user u 
        WHERE u_email = %(email)s
        AND u_status = 1"""
        
        cursor.execute(query, {'email':email})
        data = cursor.fetchone()
        if data is not None:
            print("Registeration of %s Failed. User Already Exists!",email)
            return render_template("login.html", code=409, message = "Conflict")
        
        query = """
        INSERT INTO
        user (u_email, u_pass, u_fname, u_lname, u_created_ts, u_updated_ts)
        values 
        (%(email)s, %(password)s, %(fname)s, %(lname)s, %(created_ts)s, %(updated_ts)s);"""
        
        d = cursor.execute(query, {'email':email,'password':password,'fname':fname, 'lname':lname,
                                  'created_ts':created_ts, 'updated_ts':updated_ts })
        print(d)

        db.commit()
        if d == 1:
            print("Registeration of %s Successful",email)
            return render_template("login.html", code=200, message = "Success")
            
    
    print("Simple Register Page Click")
    return render_template("register.html")


@app.route("/admin-dashboard")
def admin_dashboard():
    return render_template("admin-dashboard.html")


@app.route("/about")
def about():
    return render_template("about/about.html")


@app.route("/about/<member>")
def about_mem(member):
    return render_template("about/info.html", name=dev[member]['name'],
                           title=dev[member]['title'],
                           image=dev[member]['img'],
                           description=dev[member]['description'],
                           linkedin=dev[member]['linkedin'],
                           github=dev[member]['github'],
                           email=dev[member]['email']
                           )


@app.route("/admin/<user_id>")
def admin_page(user_id):
    if testUser.u_id < 1 or testUser.u_id != int(user_id):
        abort(404)
    conncetion, cursor = makeCursor()

    query = """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    WHERE i.i_status = 0
    AND i.i_sold_ts IS NULL;
    """

    cursor.execute(query)
    data = cursor.fetchall()
    productList = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    cursor.execute(
        "SELECT * FROM user WHERE user.u_is_admin=0 AND user.u_status>0 ;")
    data = cursor.fetchall()
    userList = []

    for d in data:
        if len(d) == 9:
            userObject = user.makeUser(d)
            userList.append(userObject)
    query = query.replace("i.i_status = 0", "i.i_status = 1")
    cursor.execute(query)
    data = cursor.fetchall()

    productList2 = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList2.append(productObject)

    return render_template("admin/admin.html", id=user_id, products=productList, users=userList, approvedProducts=productList2)


@app.route("/admin/item/<item_id>/<action>")
def admin_item_action(item_id, action):
    item_id = int(item_id)
    if testUser.u_id < 1:
        abort(404)
    connection, cursor = makeCursor()
    print(connection, cursor)
    cursor.execute("SELECT MAX(item.i_id) FROM item")
    data = cursor.fetchone()
    print(data)

    if not 0 < item_id <= data[0]:
        abort(404)

    if action == "approve":
        print("approving:", item_id)
        cursor.execute(
            "UPDATE item SET i_status=1 WHERE i_id=" + str(item_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(testUser.u_id))
    elif action == "deny":
        cursor.execute(
            "UPDATE item SET i_status=-1 WHERE i_id=" + str(item_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(testUser.u_id))
    elif action == "remove":
        cursor.execute(
            "UPDATE item SET i_status=-2 WHERE i_id=" + str(item_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(testUser.u_id))
    elif action == "moreinfo":
        print("moreinfo")
        return redirect("/products/"+str(item_id))
    else:
        abort(404)


@app.route("/admin/user/<user_id>/<action>")
def admin_user_action(user_id, action):
    user_id = int(user_id)
    if testUser.u_id < 1:
        abort(404)
    connection, cursor = makeCursor()
    cursor.execute("SELECT MAX(user.u_id) FROM user")

    if not 0 < user_id <= int(cursor.fetchone()[0]):
        abort(404)

    if action == "ban":
        cursor.execute(
            "UPDATE user SET u_status=0 WHERE u_id=" + str(user_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(testUser.u_id))
    else:
        abort(404)


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", url_for_redirect="/")


def makeCursor():
    connection = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                                 app.config['MYSQL_DATABASE_USER'],
                                 None, app.config['MYSQL_DATABASE_DB'])
    cursor = connection.cursor()

    return [connection, cursor]


db.close()

if __name__ == "__main__":
     app.run("0.0.0.0")
#    server = Server(app.wsgi_app)   # PHILIPTEST
#    server.serve()  # PHILIPTEST
