"""
Class for holding logic for a single db instance

Saves memory and can be accessed instead of recreated whenever needed

Created By Alex Kohanim

Please Contact if Questions Arise

"""


import pymysql
host = '0.0.0.0'
user_name = 'root'
password = None
db_name = 'gatorbarter'

db = pymysql.connect(host, user_name, password, db_name)


def getCursor():
    return [db, db.cursor()]
