"""
Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""


import gatorProduct as product  # class made by alex
import gatorUser as user
import gatorMessage as message
from queries import query

from flask import Flask, render_template, request, session, redirect, url_for, abort
from about_info import dev
import pymysql
import jinja2
import bleach  # sql santization lib

import hashlib
import time
import os

# from livereload import Server   # PHILIPTEST


app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
# app.config['DEBUG'] = 'True'    # PHILIPTEST
app.secret_key = os.urandom(32)

# Master Connection, Server ready, don't push changes.
db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                     app.config['MYSQL_DATABASE_USER'],
                     None, app.config['MYSQL_DATABASE_DB'])


def getCursor():
    return [db, db.cursor()]


# prepare a cursor object using cursor() method
cursor = getCursor()[1]

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

# testuser
# cursor.execute("SELECT * FROM user WHERE user.u_is_admin=1 LIMIT 1;")
cursor.execute(query().TEST_USER)
# sessionUser = user.makeUser(cursor.fetchone())
cursor.close()


@app.route("/", methods=["POST", "GET"])
def home():
    productList = []
    cursor = getCursor()[1]
    cursor.execute(query().MOST_RECENT_ITEMS(5))
    data = cursor.fetchall()

    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    cursor.close()
    otherFeedback = "" if 'otherFeedback' not in session else session['otherFeedback'] + " "
    feedback = otherFeedback
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    if 'sessionUser' in session:
        feedback += "Welcome Back " + \
            session['sessionUser']['u_fname'] + " " + \
            session['sessionUser']['u_lname']
    
    feedback += "\nHere are the latest Items"

    try:
        session.pop('otherFeedback')
    except KeyError:
        pass
    return render_template("home.html", products=productList, feedback=feedback, sessionUser=sessionUser)


@app.route('/results', methods=['POST', 'GET'])
def searchPage():

    cursor = getCursor()[1]

    print(len(request.form))

    formsLen = len(request.form)

    feedback, data = "", ""
    if formsLen > 0:
        search = request.form['text']

        search = str(bleach.clean(search))  # sanitizing a bad search
        cursor.execute(query().SEARCH_QUERY(search))

        data = cursor.fetchall()
        print("All items?", data)
    productList = []

    if len(data) == 0:
        if formsLen > 0:
            feedback = "No Results, Consider these Items"
        cursor.execute(query().ALL_APPROVED_LISTINGS())
        data = cursor.fetchall()
    cursor.close()

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)
    if feedback == "" and formsLen != 0:
        if len(data) == 1:
            feedback = str(len(data)) + " Result Found"
        else:
            feedback = str(len(data)) + " Results Found"

    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    return render_template("home.html", products=productList, feedback=feedback, sessionUser=sessionUser)


@app.route("/products/<product_id>", methods=["POST", "GET"])
def productPage(product_id):

    cursor = getCursor()[1]
    product_id = str(bleach.clean(product_id))  # sanitizing a bad redirect

    cursor.execute(query().APPROVED_ITEM(product_id))
    data = cursor.fetchall()
    if len(data) == 0:
        abort(404)

    cursor.execute(query().USER_FOR_PRODUCT(product_id))
    userObject = cursor.fetchone()
    cursor.close()

    productObject = product.makeProduct(data[0])
    try:
        if productObject.getStatus() == 0 and not session['sessionUser']['u_is_admin'] > 0:
            abort(404)
    except KeyError:
        abort(404)
    print("Redirecting to Product page", product_id)
    return render_template("products/product.html", product=productObject, user=userObject)


@app.route("/categories/<categoryName>", methods=["POST", "GET"])
def selectCategory(categoryName):

    cursor = getCursor()[1]
    print(categoryName)

    cursor.execute(query().APPROVED_ITEMS_FOR_CATEGORY(categoryName))
    data = cursor.fetchall()
    cursor.close()

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

    cursor = getCursor()[1]

    if request.method == "POST":
        email = str(bleach.clean(request.form['email']))
        pwd = str(bleach.clean(request.form['pwd']))
        print(email, " tried to login")

        cursor.execute(query().GET_USER_BY_EMAIL(email))
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            print("User not found!")
            return render_template("login.html", code=404, message="Page Not Found")
        print(data)
        userObject = user.makeUser(data)

        if pwd == userObject.u_pwd:
            print("Authentication Successful")
            session['sessionUser'] = userObject.toDict()
            return redirect("/")
        else:
            print("Authentication Failed!")
            return render_template("login.html", code=401, message="Unauthorized")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    cursor = getCursor()[1]

    if request.method == "POST":
        email = str(bleach.clean(request.form['email']))
        password = str(bleach.clean(request.form['password']))
        fname = str(bleach.clean(request.form['fname']))
        lname = str(bleach.clean(request.form['lname']))
        created_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))
        updated_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))

        print(fname, lname, created_ts)

        # check if user already exists
        cursor.execute(query().GET_USER_BY_EMAIL(email))
        data = cursor.fetchone()

        if data is not None:
            print("Registeration of" + email + " Failed. User Already Exists!")
            return redirect("/login")

        # make new user row in db
        print(query().INSERT_USER(email, password,
                                  fname, lname, created_ts, updated_ts))
        d = cursor.execute(query().INSERT_USER(
            email, password, fname, lname, created_ts, updated_ts))
        print(d)

        db.commit()
        if d == 1:
            print("Registeration of" + email + "Successful")
            return redirect("/")
        cursor.close()

    print("Simple Register Page Click")
    return render_template("register.html")


@app.route("/logout")
def logout():
    try:
        session.pop('sessionUser')
    except:
        pass
    return redirect('/')


@app.route('/item-posting')
def item_posting():
    return render_template('item-posting.html')


@app.route('/contact-seller/<item_id>', methods=['GET', 'POST'])
def contact_seller(item_id):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    if sessionUser == "":
        abort(404) # TODO lazy registration
    print(request.form)

    if request.method == "GET":
        print("WHY IS IT GET??")

    if request.method == "POST":
        buyerContact = str(bleach.clean(request.form['contactType']))
        buyerMessage = str(bleach.clean(request.form['buyerMessage']))
        print("EITHER")

        cursor = getCursor()[1]
        cursor.execute(query().APPROVED_ITEM(item_id))
        item = product.makeProduct(cursor.fetchone())

        cursor.execute(query().USER_FOR_PRODUCT(item_id))
        seller = cursor.fetchone()

        completeMessageList = messageForSeller(sessionUser['u_fname'] + " " + sessionUser['u_lname'],
                                        buyerContact, buyerMessage, item.i_title, item.i_create_ts, item.i_price)
        completeMessage = '\n'.join(message for message in completeMessageList)
        
        print(query().INSERT_MESSAGE(completeMessage, sessionUser['u_id'], seller[0], item_id))

        cursor.execute(query().INSERT_MESSAGE(completeMessage, sessionUser['u_id'], seller[0], item_id))
        db.commit()
        cursor.close()
        redirect("/")
        session['otherFeedback'] = "Message Sent"
        return render_template('contact-seller.html', sessionUser=sessionUser, id=-1)

    return render_template('contact-seller.html', sessionUser=sessionUser, id=item_id)


@app.route('/seller-inbox/<item_id>')
def seller_inbox(item_id):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    if sessionUser == "":
        abort(404)
    cursor = getCursor()[1]
    cursor.execute(query().GET_ITEM_MESSAGES(item_id))
    data = cursor.fetchall()

    print(data)

    messageList = []

    for d in data:
        if len(d) > 3:
            messageObject = message.makeMessage(d)
            messageList.append(messageObject)

    cursor.execute(query().APPROVED_ITEM(item_id))
    data = cursor.fetchone()
    cursor.close()

    messageProduct = product.makeProduct(data)

    return render_template('seller-inbox.html', sessionUser=sessionUser, messages=messageList, messageProduct=messageProduct)


@app.route("/user-dashboard")
def user_dashboard():
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    if sessionUser == "":
        abort(404)
    cursor = getCursor()[1]
    cursor.execute(query().PRODUCTS_FOR_USER(sessionUser['u_id']))
    data = cursor.fetchall()

    productList = []

    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    return render_template("user-dashboard.html", sessionUser=sessionUser, productList=productList)


@app.route("/admin-dashboard")
def admin_dashboard():
    try:
        return redirect("/admin/"+str(session['sessionUser']['u_id']))
    except KeyError:
        abort(404)


@app.route("/about")
def about():
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    return render_template("about/about.html", sessionUser=sessionUser)


@app.route("/about/<member>")
def about_mem(member):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    return render_template("about/info.html", name=dev[member]['name'],
                           title=dev[member]['title'],
                           image=dev[member]['img'],
                           description=dev[member]['description'],
                           linkedin=dev[member]['linkedin'],
                           github=dev[member]['github'],
                           email=dev[member]['email'], sessionUser=sessionUser
                           )


@app.route("/admin/<user_id>")
def admin_page(user_id):
    try:
        if session['sessionUser']['u_id'] < 1 or session['sessionUser']['u_id'] != int(user_id):
            abort(404)
    except KeyError:
        abort(404)
    conncetion, cursor = getCursor()

    cursor.execute("SELECT * FROM user;")
    print(cursor.fetchall())

    cursor.execute(query().ALL_PENDING_LISTINGS())
    data = cursor.fetchall()
    productList = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    cursor.execute(query().ALL_NON_ADMIN_APPROVED_USERS())
    data = cursor.fetchall()
    userList = []

    for d in data:
        if len(d) == 9:
            userObject = user.makeUser(d)
            userList.append(userObject)
    cursor.execute(query().ALL_APPROVED_LISTINGS())
    data = cursor.fetchall()

    approvedProducts = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            approvedProducts.append(productObject)
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    return render_template("admin/admin.html", sessionUser=sessionUser, id=user_id, products=productList, users=userList, approvedProducts=approvedProducts)


@app.route("/admin/item/<item_id>/<action>")
def admin_item_action(item_id, action):
    item_id = int(item_id)
    try:
        if session['sessionUser']['u_id'] < 1:
            abort(404)
    except KeyError:
        abort(404)
    connection, cursor = getCursor()
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
        return redirect("/admin/" + str(session['sessionUser']['u_id']))
    elif action == "deny":
        cursor.execute(
            "UPDATE item SET i_status=-1 WHERE i_id=" + str(item_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(session['sessionUser']['u_id']))
    elif action == "remove":
        cursor.execute(
            "UPDATE item SET i_status=-2 WHERE i_id=" + str(item_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(session['sessionUser']['u_id']))
    elif action == "moreinfo":
        print("moreinfo")
        return redirect("/products/"+str(item_id))
    else:
        abort(404)


@app.route("/admin/user/<user_id>/<action>")
def admin_user_action(user_id, action):
    user_id = int(user_id)
    try:
        if session['sessionUser']['u_id'] < 1:
            abort(404)
    except KeyError:
        abort(404)
    connection, cursor = getCursor()
    cursor.execute("SELECT MAX(user.u_id) FROM user")

    if not 0 < user_id <= int(cursor.fetchone()[0]):
        abort(404)

    if action == "ban":
        cursor.execute(
            "UPDATE user SET u_status=0 WHERE u_id=" + str(user_id) + ";")
        connection.commit()
        return redirect("/admin/" + str(session['sessionUser']['u_id']))
    else:
        abort(404)


def messageForSeller(buyerName, buyerConact, messageBody, itemTitle, itemTS, itemPrice):
    completeMessage = ["This is a message in regaurds to " + itemTitle]
    completeMessage.append("Which was posted at " + str(itemTS))
    completeMessage.append( "For the price of " + str(itemPrice))
    completeMessage.append( messageBody)
    completeMessage.append( buyerName )
    completeMessage.append( buyerConact )

    return completeMessage


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", url_for_redirect="/")


if __name__ == "__main__":
    #    server = Server(app.wsgi_app)   # PHILIPTEST
    #    server.serve()  # PHILIPTEST
    app.run("0.0.0.0")
