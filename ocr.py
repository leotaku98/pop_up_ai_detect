import cv2 as cv
import requests
import base64
import os


def ocr(pic_path):
    with open(pic_path, 'rb') as image_file:
        img = base64.b64encode(image_file.read())

    my_file = open("word_list.txt", "r",encoding='utf-8')
    content = my_file.read()
    word_list = content.split()
    my_file.close()

    url = 'https://ai-general-ocr.vivo.com.cn/ocr/general_recognition'
    data = {'image': img, "businessid": "bbff6230407c3aff24f39e33f852d872","pos":1}
    try:
        response = requests.post(url, data=data, timeout=100).json()
    except Exception as err:
        print(err)
        #return None

    RESULT = response['result']['OCR']
    for item in RESULT:
        x = item['location']['top_left']['x']+(item['location']['top_right']['x']-item['location']['top_left']['x'])/2
        y = item['location']['top_left']['y'] + (item['location']['down_left']['y'] - item['location']['top_left']['y']) / 2

        matched = [i for i in word_list if i in item['words']]
        if len(matched) == 1:
            print(x,y)
            return True
    return False

if __name__ == "__main__":
    has_found_matched = ocr('source/284.jpg')
    if not has_found_matched:
        os.system('python detect.py')
