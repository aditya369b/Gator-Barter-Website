from flask import Blueprint, render_template, session, request
import gatorProduct as product  # class made by alex
from about_info import dev  # class by Aditya


from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach

about_blueprint = Blueprint('about', __name__)


@about_blueprint.route("/about")
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


@about_blueprint.route("/about/<member>")
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
                           currentSearch=currentSearch,categoryName=categoryName,categories=categories
                           )


