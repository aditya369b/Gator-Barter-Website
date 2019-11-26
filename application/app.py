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


import gatorProduct as product  # class made by alex
import gatorUser as user
import gatorMessage as message
from queries import query

from flask import Flask, render_template, request, session, redirect, url_for, abort, flash
from about_info import dev
import pymysql
import jinja2
import bleach  # sql santization lib

from passlib.hash import sha256_crypt
import time
import calendar
import os
import base64
import uuid

from werkzeug.utils import secure_filename  # for input picture loading


# from livereload import Server   # PHILIPTEST


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
session_file = []


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = None
app.config['MYSQL_DATABASE_DB'] = 'gatorbarter'
app.config['MYSQL_DATABASE_HOST'] = '0.0.0.0'
# app.config['DEBUG'] = 'True'    # PHILIPTEST
app.secret_key = os.urandom(32)

# Master Connection, Server ready, don't push changes.
db = pymysql.connect(app.config['MYSQL_DATABASE_HOST'],
                     app.config['MYSQL_DATABASE_USER'],
                     None, app.config['MYSQL_DATABASE_DB'])


def getCursor():
    return [db, db.cursor()]


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


@app.route("/", methods=["POST", "GET"])
def home():
    n = 5  # number of most recent items to grab
    productList = []
    categories = []
    cursor = getCursor()[1]
    cursor.execute(query().MOST_RECENT_ITEMS(n))
    data = cursor.fetchall()

    cursor.execute(query().fetchAllCategories())
    allCategories = cursor.fetchall()
    categories = [allCategories[i][0] for i in range(len(allCategories))]
    print("categories fetched are: ",categories," and type is: ")

    feedback = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

    cursor.close()
    feedback.append(
        "" if 'otherFeedback' not in session else session['otherFeedback'])
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    if 'sessionUser' in session:
        feedback.append("Welcome Back " +
                        session['sessionUser']['u_fname'] + " " +
                        session['sessionUser']['u_lname'])

    feedback.append("Here are the latest Items")

    try:
        session.pop('otherFeedback')
    except KeyError:
        pass
#  Reseting filter options
    if 'currentCategory' in session:
        session.pop('currentCategory')
    if 'sortOption' in session:
        session.pop('sortOption')
    if 'previousQuery' in session:
        session.pop('previousQuery')
# Storing previous query for filtering
    session['previousQuery'] = [product.toDict() for product in productList]
    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories

    return render_template("home.html", products=session['previousQuery'], feedback=feedback, sessionUser=sessionUser,
                     sortOption="Sort By", currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route('/apply_filter/<filter_type>')
def applyFilter(filter_type):
    session['sortOption'] = filter_type
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    categories = [] if 'categories' not in session else session['categories']
    feedback = []
    cursor = getCursor()[1]
    if categories == "":
        cursor.execute(query().fetchAllCategories())
        allCategories = cursor.fetchall()
        categories = [allCategories[i][0] for i in range(len(allCategories))]


    if 'previousQuery' in session:
        data = session['previousQuery']
    else:
        cursor.execute(query().ALL_APPROVED_LISTINGS())
        data = [product.makeProduct(d).toDict() for d in cursor.fetchall()]

    if 'currentCategory' in session:
        feedback.append(session['currentCategory'])
        data = [d for d in data if d['c_name'] == session['currentCategory']]

    data = filter_data(data, filter_type)
    feedback.append(filter_type)
    currentSearch = "" if 'currentSearch' not in session else session['currentSearch']
    categoryName = "All" if 'categoryName' not in session else session['categoryName']

    return render_template("home.html", products=data, sessionUser=sessionUser, feedback=feedback, sortOption=session['sortOption'], currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route('/results', methods=['POST', 'GET'])
def searchPage():
    print(len(request.form))
    currentSearch = "" if 'currentSearch' not in session else session['currentSearch']
    # categoryName = "Category" if 'categoryName' not in session else session['categoryName']
    categories = [] if 'categories' not in session else session['categories']
    formsLen = len(request.form)

    feedback, data = [], ""
    productList = []
    if request.method == 'GET':
        pass
        # currentSearch = "" if 'currentSearch' not in session else session['currentSearch']

    if request.method == 'POST':
        cursor = getCursor()[1]
        if categories == "":
            cursor.execute(query().fetchAllCategories())
            allCategories = cursor.fetchall()
            categories = [allCategories[i][0] for i in range(len(allCategories))]


        if formsLen > 0:
            search = request.form['text']
            catName = "All" if request.form['category'] == "All" else request.form['category']
            if catName != "":
                session['categoryName'] = catName
            print("catname is: ",catName)
            search = str(bleach.clean(search))  # sanitizing a bad search
            print("search recieved:", search)
            session['currentSearch'] = search
            print("sessions's search", session['currentSearch'])
            currentSearch = "" if 'currentSearch' not in session else session['currentSearch']
            cursor.execute(query().SEARCH_QUERY(search,catName))

            data = cursor.fetchall()
            print("All items?", data)

        if len(data) == 0:
            if formsLen > 0:
                feedback.append("No Results, Consider these Items")
            cursor.execute(query().ALL_APPROVED_LISTINGS())
            data = cursor.fetchall()
        cursor.close()
        
    # if catName != "":
    #     data = [d for d in data if d['c_name'] == catName]

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)
            data = [productObject.toDict() for d in cursor.fetchall()]    
    
    


    session['previousQuery'] = [productObject.toDict()
                                for productObject in productList]

    if 'currentCategory' in session:
        session.pop('currentCategory')
    data = session['previousQuery']

    if len(feedback) == 0 and formsLen != 0:
        if len(data) == 1:
            feedback.append(str(len(data)) + " Result Found")
        else:
            feedback.append(str(len(data)) + " Results Found")

    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    # currentSearch = "" if 'currentSearch' not in session else session['currentSearch']
    categoryName = "All" if 'categoryName' not in session else session['categoryName']

    return render_template("home.html", products=data, feedback=feedback, sessionUser=sessionUser, sortOption="Sort By", currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route("/categories/<catName>", methods=["POST", "GET"])
def selectCategory(catName):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    cursor = getCursor()[1]
    print(catName)
    feedback = []

    if 'previousQuery' in session:  # Some sort of filtering before
        data = session['previousQuery']
        print("data from  prev query in Category ", data)
    else:
        cursor.execute(query().APPROVED_ITEMS_FOR_CATEGORY(catName))
        data = [product.makeProduct(d).toDict() for d in cursor.fetchall()]
    cursor.close()

    data = [d for d in data if d['c_name'] == catName]

    if len(data) == 0:
        feedback.append("No Results Found, Consider these")
        data = session['previousQuery']
    else:
        feedback.append(catName)

    session['currentCategory'] = catName
    session['categoryName'] = catName
    productList = []

    if 'sortOption' in session:
        data = filter_data(data, session['sortOption'])

    currentSearch = "" if 'currentSearch' not in session else session['currentSearch']
    categoryName = "All" if 'categoryName' not in session else session['categoryName']
    return render_template("home.html", products=data, feedback=feedback, sessionUser=sessionUser, sortOption="Sort By", currentSearch=currentSearch,categoryName=categoryName)


@app.route("/products/<product_id>", methods=["POST", "GET"])
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


@app.route("/login", methods=['GET', 'POST'])
def login():

    cursor = getCursor()[1]

    if request.method == "POST":
        email = str(bleach.clean(request.form['email']))
        pwd = str(bleach.clean(request.form['pwd']))
        print(email, " tried to login")

        cursor.execute(query().GET_USER_BY_EMAIL(email))
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            flash("User not found!")
            print("User not found!")
            return render_template("login.html", code=404, message="Page Not Found")
        print(data)
        userObject = user.makeUser(data)

        if sha256_crypt.verify(pwd, userObject.u_pwd):
            print("Authentication Successful")
            flash("Authentication Successful")
            session['sessionUser'] = userObject.toDict()
            session['sessionKey'] = int(time.time()*1000)
            if 'lazyRegistration' in session:
                # session.pop('lazyRegistration')
                # makeAndInsertMessageForSeller()
                if session['lazyPage'] == 'contact-seller':
                    return redirect("/contact-seller/"+session['item_id'])
                elif session['lazyPage'] == 'item-posting':
                    return redirect("/item-posting")

            return redirect("/")
        else:
            print("Authentication Failed!")
            flash("Authentication Failed!")
            return render_template("login.html", code=401, message="Unauthorized")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    cursor = getCursor()[1]

    if request.method == "POST":
        email = str(bleach.clean(request.form['email']))
        password = sha256_crypt.encrypt(
            str(bleach.clean(request.form['password'])))
        fname = str(bleach.clean(request.form['fname']))
        lname = str(bleach.clean(request.form['lname']))
        created_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))
        updated_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))

        print(fname, lname, created_ts)

        # check if user already exists
        cursor.execute(query().GET_USER_BY_EMAIL(email))
        data = cursor.fetchone()

        if data is not None:
            print("Registeration of " + email +
                  " Failed. User Already Exists!")
            flash("Registeration of " + email +
                  " Failed. User Already Exists!")
            return redirect("/login")

        # make new user row in db
        print(query().INSERT_USER(email, password,
                                  fname, lname, created_ts, updated_ts))
        d = cursor.execute(query().INSERT_USER(
            email, password, fname, lname, created_ts, updated_ts))
        print(d)

        db.commit()
        if d == 1:
            cursor.execute(query().GET_USER_BY_EMAIL(email))
            session['sessionUser'] = user.makeUser(cursor.fetchone()).toDict()
            print("Registeration of", email, "Successful")
            flash("Registeration of "+email + " Successful")
            session['sessionKey'] = int(time.time()*1000)
            if 'lazyRegistration' in session:
                # session.pop('lazyRegistration')
                if session['lazyPage'] == 'contact-seller':
                    return redirect("/contact-seller/"+session['item_id'])
                elif session['lazyPage'] == 'item-posting':
                    return redirect("/item-posting")

            return redirect("/")
        cursor.close()

    print("Simple Register Page Click")
    return render_template("register.html")


@app.route("/logout")
def logout():
    try:
        session.pop('sessionUser')
    except KeyError:
        pass
    return redirect('/')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/item-posting", methods=["POST", "GET"])
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
            is_tradable = str(1) if 'isTradable' in request.form else str(0)
            item_images = []
            if sessionUser == "":
                session['item_images'] = []

            # store image in separate folder as per category
            UPLOAD_FOLDER = 'static/images/' + item_category
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
                        file_path = os.path.join(
                            app.config['UPLOAD_FOLDER'], filename)
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

    return redirect('/')


@app.route('/contact-seller/<item_id>', methods=['GET', 'POST'])
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


@app.route('/seller-inbox/<item_id>')
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


@app.route("/user-dashboard")
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
                            currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route("/admin-dashboard")
def admin_dashboard():
    try:
        return redirect("/admin/"+str(session['sessionUser']['u_id']))
    except KeyError:
        abort(404)


@app.route("/about")
def about():
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    categories = []
    cursor = getCursor()[1]
    cursor.execute(query().fetchAllCategories())
    
    allCategories = cursor.fetchall()
    categories = [allCategories[i][0] for i in range(len(allCategories))]

    cursor.close()

    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories

    return render_template("about/about.html", sessionUser=sessionUser,
                            currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route("/about/<member>")
def about_mem(member):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']
    
    categories = []
    cursor = getCursor()[1]
    cursor.execute(query().fetchAllCategories())

    allCategories = cursor.fetchall()
    categories = [allCategories[i][0] for i in range(len(allCategories))]

    cursor.close()

    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories
    
    return render_template("about/info.html", name=dev[member]['name'],
                           title=dev[member]['title'],
                           image=dev[member]['img'],
                           description=dev[member]['description'],
                           linkedin=dev[member]['linkedin'],
                           github=dev[member]['github'],
                           email=dev[member]['email'], sessionUser=sessionUser,
                           currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route("/admin/<user_id>")
def admin_page(user_id):
    try:
        if session['sessionUser']['u_id'] < 1 or session['sessionUser']['u_id'] != int(user_id):
            abort(404)
    except KeyError:
        abort(404)
    conncetion, cursor = getCursor()
    categories=[]
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
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)

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
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            approvedProducts.append(productObject)
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    currentSearch = ""
    categoryName = "All"
    session['categories'] = categories

    return render_template("admin/admin.html", sessionUser=sessionUser, id=user_id, products=productList, users=userList, approvedProducts=approvedProducts,
                                                currentSearch=currentSearch,categoryName=categoryName,categories=categories)


@app.route("/admin/item/<item_id>/<action>")
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


@app.route("/admin/user/<user_id>/<action>")
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


def insertItemPost(item_name, item_category, item_desc, item_price, is_tradable, item_images, sessionUser, isLazyReg):

    cursor = db.cursor()
    user_id = sessionUser['u_id']  # else get current logged in user's user id
    images_path = []

    # store image in separate folder as per category
    UPLOAD_FOLDER = 'static/images/' + item_category
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print('Upload folder is: ', UPLOAD_FOLDER)
    print('App config Upload folder is: ', app.config['UPLOAD_FOLDER'])

    ts = time.strftime('%Y-%m-%d %H:%M:%S')

    # print ("Print request.files[1]", request.files,"  and the type is: ", type(request.files))

    query = 'INSERT INTO item(i_title, i_desc, i_price, i_is_tradable, i_u_id, i_c_id, i_status, i_created_ts, i_updated_ts) ' \
            'VALUES("' + item_name + '", ' \
            '"' + item_desc + '", ' \
            '"' + item_price + '", ' \
            '"' + is_tradable + '",' \
            ' "' + str(user_id) + '' \
            '", (SELECT c_id from category where c_name="' \
            '' + item_category + '"), 0, \'' + ts + "\', \'" + ts + '\'  );'

    print(query)
    data = cursor.execute(query)

    print("printing response from query", data)

    cursor_id = cursor.lastrowid
    print("ID", cursor_id)

    unique_variable = 0

    if isLazyReg:
        for file in item_images:
                    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            filename = str(user_id) + '_' + str(cursor_id) + '_' + \
                str(unique_variable) + '.' + file.rsplit('.', 1)[1].lower()
            new_path = file.rsplit('/', 1)[0] + '/' + filename
            print("The os rename values are: ", file, " and ", new_path)
            os.rename(file, new_path)
            images_path.append(new_path)
    else:
        for file in item_images:
            # file = request.files['file']
            #     print("single file ")
            # file = base64.b64decode(file)

            # print("printing file:", file)
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                # unique filename
                filename = str(user_id) + '_' + str(cursor_id) + '_' + \
                    str(unique_variable) + '.' + \
                    filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print("file path is:", file_path)
                # file = open(file,"wr")
                file.save(file_path)

                images_path.append(file_path)

        unique_variable += 1
        #####

    for path in images_path:

        query = 'insert into item_image(ii_url,ii_i_id) values("/' + \
            path+'",'+str(cursor_id)+')'
        print(query)
        cursor.execute(query)
    db.commit()

    # print("Item has been sent to admin for approval!")

    cursor.close()


def messageForSeller(buyerName, buyerConact, messageBody, itemTitle, itemTS, itemPrice):
    completeMessage = ["This is a message in regaurds to " + itemTitle]
    completeMessage.append("Which was posted at " + str(itemTS))
    completeMessage.append("For the price of " + str(itemPrice))
    completeMessage.append(messageBody)
    completeMessage.append(buyerName)
    completeMessage.append(buyerConact)

    return completeMessage


def filter_data(data, filter_type):
    if filter_type == "alpha_desc":
        data = sorted(data, key=lambda k: k['i_title'])
    elif filter_type == "alpha_asc":
        data = sorted(data, key=lambda k: k['i_title'], reverse=True)
    elif filter_type == "price_asc":
        data = sorted(data, key=lambda k: k['i_price'])
    elif filter_type == "price_desc":
        data = sorted(data, key=lambda k: k['i_price'], reverse=True)
    elif filter_type == "date_asc":
        data = sorted(data, key=lambda k: k['i_create_ts'])
    elif filter_type == "date_desc":
        data = sorted(data, key=lambda k: k['i_create_ts'], reverse=True)
    else:
        abort(404)
    return data


def makeAndInsertMessageForSeller(buyerContact, buyerMessage, item_id, sessionUser):
    cursor = getCursor()[1]
    cursor.execute(query().APPROVED_ITEM(item_id))
    item = product.makeProduct(cursor.fetchone())

    cursor.execute(query().USER_FOR_PRODUCT(item_id))
    seller = cursor.fetchone()

    completeMessageList = messageForSeller(sessionUser['u_fname'] + " " + sessionUser['u_lname'],
                                           buyerContact, buyerMessage, item.i_title, item.i_create_ts, item.i_price)
    completeMessage = '\n'.join(message for message in completeMessageList)

    print(query().INSERT_MESSAGE(completeMessage,
                                 sessionUser['u_id'], seller[0], item_id))

    cursor.execute(query().INSERT_MESSAGE(completeMessage,
                                          sessionUser['u_id'], seller[0], item_id))
    db.commit()
    cursor.close()
    session['otherFeedback'] = "Message Sent"


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", url_for_redirect="/")


if __name__ == "__main__":
    #    server = Server(app.wsgi_app)   # PHILIPTEST
    #    server.serve()  # PHILIPTEST
    app.run("0.0.0.0")
