"""
BluePrint for Landing Page route and Search Results page route
As well as the logic for those routs

Many decisions for persistant search results and combining filter types present

This BluePrint is not an easy read

Please contact Alex Kohanim if any questions arise

"""


from flask import Blueprint, render_template, session, request
import gatorProduct as product  # class made by alex

import bleach
import gatorUser as user
from queries import query
from dbCursor import getCursor
from filterData import filter_data
index_blueprint = Blueprint('index', __name__)

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/", methods=["POST", "GET"])
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
    print("categories fetched are: ", categories, " and type is: ")

    feedback = []
    productUsers = []
    for d in data:
        if len(d) == 16:
            productObject = product.makeProduct(d)
            productList.append(productObject)
            cursor.execute(query().FULL_USER_FOR_PRODUCT(str(productObject.i_id)))
            productUser = user.makeUser(cursor.fetchone())
            productUsers.append(productUser.toDict())

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
                     sortOption="Sort By", currentSearch=currentSearch,categoryName=categoryName,categories=categories, productUsers=productUsers)


@index_blueprint.route('/results', methods=['POST', 'GET'])
def searchPage():

    cursor = getCursor()[1]

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
        # cursor.close()

        productUsers = []

    # if catName != "":
    #     data = [d for d in data if d['c_name'] == catName]

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)
            data = [productObject.toDict() for d in cursor.fetchall()]

            cursor.execute(query().FULL_USER_FOR_PRODUCT(str(productObject.i_id)))
            productUser = user.makeUser(cursor.fetchone())
            productUsers.append(productUser) 

    cursor.close()
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

    return render_template("home.html", products=data, feedback=feedback, sessionUser=sessionUser, sortOption="Sort By", currentSearch=currentSearch,categoryName=categoryName,categories=categories, productUsers=productUsers)


@index_blueprint.route("/categories/<catName>", methods=["POST", "GET"])
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

