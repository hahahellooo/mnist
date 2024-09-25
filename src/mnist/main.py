from typing import Annotated
import os 
from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from pytz import timezone
import pymysql.cursors
from mnist.db import get_connection

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    
    current_time=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    img = await file.read()
    file_name = file.filename
    file_ext = file.content_type.split("/")[-1] #"image/png"
    file_label = file_name.split('.')[0][0]
    upload_dir = os.getenv("UPLOAD_DIR",'/home/hahahellooo/code/mnist/img')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
    import uuid
    file_full_path = os.path.join(upload_dir, f'{uuid.uuid4()}.{file_ext}')
    # "/home/hahahellooo/code/mnist/img/6d1668ec-893f-4107-95b9-8c3c364a5bc2.png"

    with open(file_full_path, "wb") as f:
        f.write(img)
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `image_processing`(file_name, label, file_path, request_time, request_user) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(file_name, file_label, file_full_path, current_time, 'n21'))
            result = cursor.fetchone()
        connection.commit()
    
    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)

    return {
            "filename": file.filename,
            "filelabel": file_label,
            "content_type":file.content_type,
            "file_full_path":file_full_path            
            }

@app.get("/all/")
def all():
    connection = get_connection()
    with connection:                                              
        with connection.cursor() as cursor:
            sql = "SELECT * FROM image_processing"
            cursor.execute(sql)
            result = cursor.fetchall()
    #DB 연결SELECT ALL
    #결과값 리턴
    return result

@app.get("/one/")
def one():
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT file_name FROM image_processing"
            cursor.execute(sql)
            result = cursor.fetchone()
    #DB연결 SELECT 값 중 하나만 리턴
    # 결과값 리턴
    return result

@app.get("/many/")
def many(size: int = -1):
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM image_processing"
            cursor.execute(sql)
            result=cursor.fetchmany(size)
    return result

