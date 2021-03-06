"""
BluePrint for all of the Admin Routs and Functioality

Multiple checks to verify that only Admins can access these pages

All logic Written by Alex Kohanim, if anythin needs clarifing, please contact

"""


from flask import Blueprint, render_template, session, request, abort, redirect
import gatorProduct as product  # class made by alex
import gatorUser as user

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route("/admin-dashboard")
def admin_dashboard():
    try:
        return redirect("/admin/"+str(session['sessionUser']['u_id']))
    except KeyError:
        abort(404)


@admin_blueprint.route("/admin/<user_id>")
def admin_page(user_id):
    try:
        if session['sessionUser']['u_id'] < 1 or session['sessionUser']['u_id'] != int(user_id):
            abort(404)
    except KeyError:
        abort(404)
    conncetion, cursor = getCursor()
    categories = []
    cursor.execute("SELECT * FROM user;")
    print(cursor.fetchall())
    # fetch the items for admin approval from db
    cursor.execute(query().ALL_PENDING_LISTINGS())
    data = cursor.fetchall()
    # Fetch the categories from db
    cursor.execute(query().fetchAllCategories())
    allCategories = cursor.fetchall()
    categories = [allCategories[i][0] for i in range(len(allCategories))]

    productList = []
    productListUsers = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)
            cursor.execute(query().FULL_USER_FOR_PRODUCT(
                str(productObject.i_u_id)))
            productListUsers.append(user.makeUser(cursor.fetchone()))

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
    approvedProductsUsers = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            approvedProducts.append(productObject)
            cursor.execute(query().FULL_USER_FOR_PRODUCT(
                str(productObject.i_u_id)))
            approvedProductsUsers.append(user.makeUser(cursor.fetchone()))

    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories

    return render_template("admin/admin.html", sessionUser=sessionUser, id=user_id, products=productList, users=userList, approvedProducts=approvedProducts,
                           currentSearch=currentSearch, categoryName=categoryName, categories=categories, approvedProductsUsers=approvedProductsUsers, productListUsers=productListUsers)


@admin_blueprint.route("/admin/item/<item_id>/<action>")
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


@admin_blueprint.route("/admin/user/<user_id>/<action>")
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
