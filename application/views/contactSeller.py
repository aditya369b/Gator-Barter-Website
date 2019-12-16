"""
BluePrint for contactseller route and logic

Incorparated Laxy Registration logic by using session (backend) variables

Written and revised by Adatiya Bodi, Alex Kohanim and Tejasvi Belsare

All three of them shoudl be able to answer most if not all questions about this blueprint

Please contact if any questions arise

"""


from flask import Blueprint, render_template, session, request, redirect
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
from helperFunctions import makeAndInsertMessageForSeller
import bleach

contactSeller_blueprint = Blueprint('contactSeller', __name__)


@contactSeller_blueprint.route('/contact-seller/<item_id>', methods=['GET', 'POST'])
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
        cursor = getCursor()[1]
        cursor.execute(query().APPROVED_ITEM(str(item_id)))
        itemObject = product.makeProduct(cursor.fetchone())
        cursor.close()
        currentItem = itemObject.toDict()
        session['contact_seller_item'] = currentItem

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

        currentItem = "" if 'contact_seller_item' not in session else session[
            'contact_seller_item']
    try:
        session.pop('contact_seller_item')
    except KeyError:
        print('yo, dat contact_seller_item was not in the session bro')
        print('Have a nice day!')

    return render_template('contact-seller.html', sessionUser=sessionUser, id=item_id, currentItem=currentItem)
