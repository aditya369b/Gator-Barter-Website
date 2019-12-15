from flask import Blueprint, render_template, session, request, redirect, flash
import gatorProduct as product  # class made by alex
import gatorUser as user  # class made by alex

from queries import query
from dbCursor import getCursor
from filterData import filter_data
import bleach
from passlib.hash import sha256_crypt
import time

authentication_blueprint = Blueprint('authentication', __name__)

db = getCursor()[0]


@authentication_blueprint.route("/login", methods=['GET', 'POST'])
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
                    flash('Message Sent Successfully')
                    return redirect("/contact-seller/"+session['item_id'])
                elif session['lazyPage'] == 'item-posting':
                    flash('Item Pending Approval')
                    return redirect("/item-posting")

            return redirect("/")
        else:
            print("Authentication Failed!")
            flash("Authentication Failed!")
            return render_template("login.html", code=401, message="Unauthorized")

    return render_template("login.html")


@authentication_blueprint.route("/register", methods=['GET', 'POST'])
def register():

    cursor = getCursor()[1]

    if request.method == "POST":
        print(request.form)
        email = str(bleach.clean(request.form['email']))
        password = sha256_crypt.encrypt(
            str(bleach.clean(request.form['password'].strip())))
        confirm_password = sha256_crypt.encrypt(
            str(bleach.clean(request.form['confirm-password'].strip())))
        fname = str(bleach.clean(request.form['fname']))
        lname = str(bleach.clean(request.form['lname']))
        created_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))
        updated_ts = str(bleach.clean(time.strftime('%Y-%m-%d %H:%M:%S')))

        if not request.form['password'] == request.form['confirm-password'] :
            pass_temp = request.form['password']
            confirm_pass_temp = request.form['confirm-password']
            print(pass_temp, confirm_pass_temp)
            print(pass_temp == confirm_pass_temp)
            flash("passwords do not match")
            return redirect("/register")


        # check if user already exists
        cursor.execute(query().GET_USER_BY_EMAIL(email))
        data = cursor.fetchone()

        if data is not None:
            print("Registeration of " + email +
                  " Failed. User Already Exists!")
            flash("Registeration of " + email +
                  " Failed. User Already Exists!")
            return redirect("/login")

        if not email.endswith("@mail.sfsu.edu"):
            flash("email needs to end with @mail.sfsu.edu")
            return redirect("/register")

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


@authentication_blueprint.route("/logout")
def logout():
    try:
        session.pop('sessionUser')
    except KeyError:
        pass
    return redirect('/')
