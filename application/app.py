"""
Main Python File for running Flask
registers blueprints that hold backend logic

Session used with a unique key per thread keeping user session persistant.
Please consult Back-End Lead if any questions arise from this file
or any of the files in "views"

item status:
-2 - removed
-1 - rejected 
0 - pending
1 - approved
2 - sold


For refrence: http://exploreflask.com/en/latest/blueprints.html
"""


from queries import query
from dbCursor import getCursor


from flask import Flask, abort, render_template

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

import os


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['DEBUG'] = 'True'    # PHILIPTEST

# Might need to rework this, random now to ensure unique sessions (with high probability)
app.secret_key = os.urandom(32)

# Master Connection
db = getCursor()[0]

cursor = getCursor()[1]

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

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
    # server = Server(app.wsgi_app)   # PHILIPTEST
    # server.serve()  # PHILIPTEST
    app.run("0.0.0.0")
