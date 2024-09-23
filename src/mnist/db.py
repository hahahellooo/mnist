import pymysql.cursors
import os

def get_connection():

    connection = pymysql.connect(host=os.getenv("DB_IP",'172.17.0.1'), port = 53306,
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
    return connection


