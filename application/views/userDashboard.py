from flask import Blueprint, render_template, session, request, abort, redirect
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

userDashboard_blueprint = Blueprint('userDashboard', __name__)


@userDashboard_blueprint.route("/user-dashboard")
def user_dashboard():
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    categories = []

    if sessionUser == "":
        abort(404)
    cursor = getCursor()[1]
    # To fetch items for a user from db
    cursor.execute(query().PRODUCTS_FOR_USER(sessionUser['u_id']))
    data = cursor.fetchall()
    # To fetch categories from db
    cursor.execute(query().fetchAllCategories())
    allCategories = cursor.fetchall()
    categories = [allCategories[i][0] for i in range(len(allCategories))]

    productList = []

    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories

    return render_template("user-dashboard.html", sessionUser=sessionUser, productList=productList,
                           currentSearch=currentSearch, categoryName=categoryName, categories=categories)



@userDashboard_blueprint.route("/user-dashboard/<item_id>/<action>")
def contact_seller_action(item_id, action):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    if sessionUser == "":
        abort(404)

    if action == "sold":
        db, cursor = getCursor()
        cursor.execute(query().SELL_ITEM(item_id))
        db.commit()
        return redirect("/user-dashboard")
    else:
        abort(404)
