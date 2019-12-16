"""
BluePrint for seller-inbox route and logic

Not much logic here, just sends messages and the product to the front end

Written by Alex Kohanim

Please contact if questions arise

"""

from flask import Blueprint, render_template, session, request, abort
import gatorProduct as product  # class made by alex
import gatorMessage as message

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

sellerInbox_blueprint = Blueprint('sellerInbox', __name__)


@sellerInbox_blueprint.route('/seller-inbox/<item_id>')
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
