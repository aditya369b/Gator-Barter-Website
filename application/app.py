"""
Main Python File for running Flask
Handels the routs and backend logic

Session used with a unique key per thread keeping user session persistant.
Please consult Back-End Lead if any questions arise from this file

item status:
-2 - removed
-1 - rejected 
0 - pending
1 - approved
2 - sold


Template Taken From: https://github.com/tecladocode/simple-flask-template-app by Alex Kohanim
More blog posts from the original author: https://blog.tecladocode.com/
Might incorperate some features mentioned in the blog post(s)
Also, this blog post: https://blog.tecladocode.com/handling-the-next-url-when-logging-in-with-flask/
"""

import gatorProduct as product  # class made by alex
import gatorUser as user
import gatorMessage as message
from queries import query
from dbCursor import getCursor
from filterData import filter_data
from about_info import dev

from flask import Flask, render_template, request, session, redirect, url_for, abort, flash

from views.index import index_blueprint
from views.authentication import authentication_blueprint
from views.filter import filter_blueprint
from views.product import product_blueprint
from views.itemPosting import itemPosting_blueprint

import pymysql
import jinja2
import bleach  # sql santization lib
import time
import calendar
import os
import base64
import uuid
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename  # for input picture loading

# from livereload import Server   # PHILIPTEST

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = None
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
# app.config['DEBUG'] = 'True'    # PHILIPTEST
app.secret_key = os.urandom(32)

# Master Connection, Server ready, don't push changes.

db = getCursor()[0]

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

app.register_blueprint(index_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(filter_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(itemPosting_blueprint)




@app.route('/contact-seller/<item_id>', methods=['GET', 'POST'])
def contact_seller(item_id):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    # if sessionUser == "":
    #     abort(404)  # TODO lazy registration
    if 'lazyRegistration' in session:
        makeAndInsertMessageForSeller(
            session['buyerContact'], session['buyerMessage'], item_id, sessionUser)
        session.pop('lazyRegistration')
        session.pop('lazyPage')
        return render_template('contact-seller.html', sessionUser=sessionUser, id=-1)

    if request.method == "GET":
        print("Got a Get")

    if request.method == "POST":
        buyerContact = str(bleach.clean(request.form['contactType']))
        buyerMessage = str(bleach.clean(request.form['buyerMessage']))

        isRegistered = not sessionUser == ""
        session['item_id'] = item_id
        if not isRegistered:
            session['lazyRegistration'] = True
            session['lazyPage'] = 'contact-seller'
            session['buyerContact'] = buyerContact
            session['buyerMessage'] = buyerMessage
            print("going to login?")
            return redirect("/login")
        makeAndInsertMessageForSeller(
            buyerContact, buyerMessage, item_id, sessionUser)
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





@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", url_for_redirect="/")


if __name__ == "__main__":
    #    server = Server(app.wsgi_app)   # PHILIPTEST
    #    server.serve()  # PHILIPTEST
    app.run("0.0.0.0")
