from flask import Blueprint, render_template, session, request
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/", methods=["POST", "GET"])
def home():
    n = 5  # number of most recent items to grab
    productList = []
    cursor = getCursor()[1]
    cursor.execute(query().MOST_RECENT_ITEMS(n))
    data = cursor.fetchall()
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
# Storing previous query for filtering
    session['previousQuery'] = [product.toDict() for product in productList]

    return render_template("home.html", products=session['previousQuery'], feedback=feedback, sessionUser=sessionUser, sortOption="Sort By")


@index_blueprint.route('/results', methods=['POST', 'GET'])
def searchPage():

    cursor = getCursor()[1]

    print(len(request.form))

    formsLen = len(request.form)

    feedback, data = [], ""
    if formsLen > 0:
        search = request.form['text']

        search = str(bleach.clean(search))  # sanitizing a bad search
        cursor.execute(query().SEARCH_QUERY(search))

        data = cursor.fetchall()
        print("All items?", data)
    productList = []

    if len(data) == 0:
        if formsLen > 0:
            feedback.append("No Results, Consider these Items")
        cursor.execute(query().ALL_APPROVED_LISTINGS())
        data = cursor.fetchall()
    cursor.close()

    for d in data:
        if len(d) > 11:
            productObject = product.makeProduct(d)
            productList.append(productObject)

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

    return render_template("home.html", products=data, feedback=feedback, sessionUser=sessionUser, sortOption="Sort By")


@index_blueprint.route("/categories/<categoryName>", methods=["POST", "GET"])
def selectCategory(categoryName):
    sessionUser = "" if 'sessionUser' not in session else session['sessionUser']

    cursor = getCursor()[1]
    print(categoryName)
    feedback = []

    if 'previousQuery' in session:  # Some sort of filtering before
        data = session['previousQuery']
        print("data from  prev query in Category ", data)
    else:
        cursor.execute(query().APPROVED_ITEMS_FOR_CATEGORY(categoryName))
        data = [product.makeProduct(d).toDict() for d in cursor.fetchall()]
    cursor.close()

    data = [d for d in data if d['c_name'] == categoryName]

    if len(data) == 0:
        feedback.append("No Results Found, Consider these")
        data = session['previousQuery']
    else:
        feedback.append(categoryName)

    session['currentCategory'] = categoryName
    productList = []

    if 'sortOption' in session:
        data = filter_data(data, session['sortOption'])

    return render_template("home.html", products=data, feedback=feedback, sessionUser=sessionUser, sortOption="Sort By")
