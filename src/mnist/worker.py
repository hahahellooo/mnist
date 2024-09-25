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
            sql = "SELECT num, label, file_path, prediction_result FROM image_processing WHERE prediction_result IS NULL LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()

  # STEP 2
  # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
  # 동시에 prediction_model, prediction_time 도 업데이트
  
    if result is None:
        data = {"message":f"❌예측할 모델이 없습니다❌"}
        print(data)
    else:

        num = result['num']
        file_path = result['file_path']
        label = result['label']
        from mnist.predict import  predict_digit
        prediction_result = predict_digit(file_path)
        prediction_model = 'n21'
        prediction_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
        
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                sql = """UPDATE image_processing 
                         SET prediction_result=%s, 
                             prediction_model=%s, 
                             prediction_time=%s
                             label=%s
                         WHERE num = %s"""
                cursor.execute(sql,(prediction_result, prediction_model, prediction_time, label, num))
                connection.commit()
    
    # STEP 3
    # LINE 으로 처리 결과 전송
    KEY = os.getenv("LINE_TOKEN")
    url = "https://notify-api.line.me/api/notify"
    if result is not None:

        data = {"message":f"👌모델 {prediction_result}을/를 성공적으로 저장했습니다👌"}
        # API 호출시 사용되는 헤더 정보
        headers={"Authorization":f"Bearer {KEY}"}
        response = requests.post(url, data, headers=headers)
    else:
        data = {"message":f"저장할 데이터가 없습니다."}
        # API 호출시 사용되는 헤더 정보
        headers={"Authorization":f"Bearer {KEY}"}
        response = requests.post(url, data, headers=headers)
    #서버로부터 받은 응답 출력(성공시에는 {"status":200,"message":"ok"}와 같은 메시지 반환
    print(response.text)
    return True

