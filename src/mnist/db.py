import pymysql.cursors

def get_connection():

    connection = pymysql.connect(host='localhost', port = 53306,
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection


