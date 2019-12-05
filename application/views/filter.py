from flask import Blueprint, render_template, session
import gatorProduct as product  # class made by alex

from queries import query
from dbCursor import getCursor

from filterData import filter_data
filter_blueprint = Blueprint('filter', __name__ )


@filter_blueprint.route('/apply_filter/<filter_type>')
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

