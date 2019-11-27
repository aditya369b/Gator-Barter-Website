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

