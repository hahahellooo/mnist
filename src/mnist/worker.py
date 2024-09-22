import random
import os
import requests
from datetime import datetime
from pytz import timezone
import pymysql.cursors
from mnist.db import get_connection


def run():
# STEP 1                                                                           # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기 
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELELCT prediction_result FROM image_processing WHERE prediction_result IS NULL LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

  # STEP 2
  # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
  # 동시에 prediction_model, prediction_time 도 업데이트
    prediction_result = random.randint(0,9)
    prediction_model = 'RandomModel'
    prediction_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = """UPDATE image_processing 
                     SET prediction_result=%s, 
                         prediction_model=%s, 
                         prediction_time=%s
                     WHERE num = %s"""
            cursor.execute(sql,(prediction_result, prediction_model, prediction_time, num))
            connection.commit()

  # STEP 3
  # LINE 으로 처리 결과 전송
   # curl -X POST -H 'Authorization: Bearer UuAPZM7msPnFaJt5wXTUx34JqYKO7n3AUlLq4b3eyZ4' -F 'message={{ dag_run.dag_id }} success' https://notify-api.line.me/api/notify
    KEY = os.environ.get('LINE_TOKEN')
    url = "https://notify-api.line.me/api/notify"
    data = {"message":f"{prediction_result}를 성공적으로 저장했습니다!"}
    headers={"Authorization":f"Bearer {KEY}"}
    response = requests.post(url, data, headers=headers)

    print(response.text)
    
    return True

