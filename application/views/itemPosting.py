
from flask import Blueprint, render_template, session, request, abort, redirect, flash
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data

from helperFunctions import allowed_file, insertItemPost
import bleach
import uuid
import os
from werkzeug.utils import secure_filename  # for input picture loading

itemPosting_blueprint = Blueprint('itemPosting', __name__)

session_file = []

@itemPosting_blueprint.route("/item-posting", methods=["POST", "GET"])
def item_posting():

    # cursor = db.cursor()
    print(request.form)
    formsLen = len(request.form)
    images_path = []

    if 'lazyRegistration' in session:
        print('session file is: ', session_file)
        insertItemPost(session['item_name'], session['item_category'], session['item_desc'],
                       session['item_price'], session['is_tradable'], session['item_images'],
                       session['sessionUser'], True)
        session_file.clear()
        session.pop('lazyRegistration')
        session.pop('lazyPage')
        print('Rediret from lazy login to home')
        # return render_template('home.html', sessionUser=session['sessionUser'], id=-1,categoryName="Catogory")
        return redirect("/")

    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    # print("Session user", sessionUser)

    if request.method == "POST":
        if request.form:
            print("printing request form", request.form)

        if formsLen > 0:
            item_name = str(bleach.clean(request.form['item_title']))
            item_category = request.form['category']
            item_desc = str(bleach.clean(request.form['item_desc']))
            item_price = request.form['item_price']
            is_tradable = '0' if 'isTradable' not in request.form else request.form['isTradable']  #str(1) if 'isTradable' in request.form else str(0)
            item_images = []
            if sessionUser == "":
                session['item_images'] = []

            # store image in separate folder as per category
            UPLOAD_FOLDER = 'static/images/' + item_category
            session['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            for file in request.files.getlist('file'):
                if file.filename == '':
                    print('No file selected for uploading')
                else:
                    # session['item_image'].append(base64.b64encode(file.read()).decode('ascii'))
                    if sessionUser == "":
                        # session_file.append(file)

                        if file and allowed_file(file.filename):

                            filename = secure_filename(file.filename)

                    # unique filename
                        uuid_val = uuid.uuid1()
                        filename = str(uuid_val) + '.' + \
                            filename.rsplit('.', 1)[1].lower()
                        print(os.path.curdir)
                        file_path = os.path.join(session['UPLOAD_FOLDER'], filename)
                        print("file path from item-posting post req is:", file_path)
                        # file = open(file,"wr")
                        file.save(file_path)
                        session['item_images'].append(file_path)
                    else:
                        item_images.append(file)

            if sessionUser == "":
                session['lazyRegistration'] = True
                session['lazyPage'] = 'item-posting'
                session['item_name'] = item_name
                session['item_category'] = item_category
                session['item_desc'] = item_desc
                session['item_price'] = item_price
                session['is_tradable'] = is_tradable
                # session['item_userid'] =
                # session['item_images'] = None #item_images

                print("going to login?")
                return redirect("/login")

            else:
                # sessionUser = session['sessionUser']
                insertItemPost(item_name, item_category, item_desc,
                               item_price, is_tradable, item_images, sessionUser, False)

    if request.method == "GET":
        return render_template("item-posting.html")

    flash("Item Posted Successfully")

    return redirect('/')
