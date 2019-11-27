from flask import Blueprint, render_template, session, request, abort
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

userDashboard_blueprint = Blueprint('userDashboard', __name__)


@userDashboard_blueprint.route("/user-dashboard")
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


