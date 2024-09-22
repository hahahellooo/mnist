import pymysql.cursors

def get_connection():
  connection = pymysql.connect(host='localhost', port = 53306,
                            user = 'mnist', password = '1234',
                            database = 'mnistdb',
                            cursorclass=pymysql.cursors.DictCursor)
  return connection


def dml(sql, *values):
  connection = get_connection()

  with conn:
    with conn.cursor() as cursor:
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount
