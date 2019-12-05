import pymysql
db = pymysql.connect('localhost', 'root', 'root', 'gatorbarter')

def getCursor():
    return [db, db.cursor()]