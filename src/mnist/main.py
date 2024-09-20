from typing import Annotated
import os 
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    current_time=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')
    img = await file.read()
    file_name = file.filename
    upload_dir = "./photo"
    file_full_path = os.path.join(upload_dir, file_name)

    connection = pymysql.connect(host=os.getenv("DB_IP", "localhost"),
                                 user='mnist',
                                 password='1234',
                                 port=int(os.getenv("DB_PORT","53306")),
                                 database='mnistdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `image_processing`(num, file_name, file_path, request_time, request_user) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(num, file_name, file_full_path, current_time, 'n21'))
            result = cursor.fetchone()
        connection.commit()
    
    if not os.path.exists(file_full_path):
        os.makedirs(file_full_path, exist_ok=True)

    with open(file_full_path, "wb") as f:
        f.write(img)

    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)

    return {
            "filename": file.filename,
            "content_type":file.content_type,
            "file_full_path":file_full_path            
            }
