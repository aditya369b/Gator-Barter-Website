import pymysql
db = pymysql.connect('0.0.0.0', 'root', None, 'gatorbarter')

def getCursor():
    return [db, db.cursor()]