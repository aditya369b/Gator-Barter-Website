"""
Common Helper functions used in multiple routs

Made a class for them to reduce repeated code

File made by Alex Kohanim

Functions made by multiple team members

Please Contact Alex if any questions arise and if He can't answer your question
He will redirect you to the appropriate developer
"""

from dbCursor import getCursor
from queries import query
import gatorProduct as product

from flask import session
import time
import os
from werkzeug.utils import secure_filename  # for input picture loading


db = getCursor()[0]

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def messageForSeller(buyerName, buyerConact, messageBody, itemTitle, itemTS, itemPrice):
    completeMessage = ["This is a message in regaurds to " + itemTitle]
    completeMessage.append("Which was posted at " + str(itemTS))
    completeMessage.append("For the price of " + str(itemPrice))
    completeMessage.append(messageBody)
    completeMessage.append(buyerName)
    completeMessage.append(buyerConact)

    return completeMessage


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def insertItemPost(item_name, item_category, item_desc, item_price, is_tradable, item_images, sessionUser, isLazyReg):

    cursor = db.cursor()
    user_id = sessionUser['u_id']  # else get current logged in user's user id
    images_path = []

    # store image in separate folder as per category
    UPLOAD_FOLDER = 'static/images/' + item_category
    session['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print('Upload folder is: ', UPLOAD_FOLDER)
    print('App config Upload folder is: ', session['UPLOAD_FOLDER'])

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
                file_path = os.path.join(session['UPLOAD_FOLDER'], filename)
                print("file path is:", file_path)
                # file = open(file,"wr")
                print(os.getcwd())
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
