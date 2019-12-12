import pymysql
host = '0.0.0.0'
user_name = 'root'
password = None
db_name = 'gatorbarter'

db = pymysql.connect(host, user_name, password, db_name)

def getCursor():
    return [db, db.cursor()]