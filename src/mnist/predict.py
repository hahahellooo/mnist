import os
from tensorflow.keras.datasets import mnist
from PIL import Image
import numpy as np
from keras.models import load_model

def get_image():
    file_name = 'mnist240924.keras'
    my_path = __file__
    dir_name = os.path.dirname(my_path)
    image_path = os.path.join(dir_name, file_name)
    return image_path
model = load_model(get_image())
# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    # img = 255 - np.array(img)  # 흑백 반전
    img = np.array(img)

    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

# 예측

def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit
