"""
BluePrint for product page route and logic

Written by Alex Kohanim

Please contact of questions arise

"""


from flask import Blueprint, render_template, session, request, abort
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

product_blueprint = Blueprint('product', __name__)


@product_blueprint.route("/products/<product_id>", methods=["POST", "GET"])
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
