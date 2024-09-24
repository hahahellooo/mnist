import pymysql.cursors
import os

def get_connection():

    connection = pymysql.connect(host=os.getenv("DB_IP",'localhost'), 
                                 port =os.getenv("DB_PORT", "53306"),
                                 user = 'mnist', password = '1234',
                                 database = 'mnistdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


