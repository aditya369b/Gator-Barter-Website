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

# import gatorProduct as product  # class made by alex
# import gatorUser as user
# import gatorMessage as message
from queries import query
from dbCursor import getCursor
# from filterData import filter_data
# from about_info import dev

from flask import Flask, render_template, request, session, redirect, url_for, abort, flash

from views.index import index_blueprint
from views.authentication import authentication_blueprint
from views.filter import filter_blueprint
from views.product import product_blueprint
from views.itemPosting import itemPosting_blueprint
from views.contactSeller import contactSeller_blueprint
from views.sellerInbox import sellerInbox_blueprint
from views.userDashboard import userDashboard_blueprint
from views.about import about_blueprint
from views.admin import admin_blueprint


# import pymysql
# import jinja2
# import bleach  # sql santization lib
# import time
# import calendar
import os
# import base64
# import uuid
# from passlib.hash import sha256_crypt
# from werkzeug.utils import secure_filename  # for input picture loading

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
app.register_blueprint(contactSeller_blueprint)
app.register_blueprint(sellerInbox_blueprint)
app.register_blueprint(userDashboard_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(admin_blueprint)


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", url_for_redirect="/")

if __name__ == "__main__":
    #    server = Server(app.wsgi_app)   # PHILIPTEST
    #    server.serve()  # PHILIPTEST
    app.run("0.0.0.0")
