import cv2 as cv
import torch
from PIL import Image
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
import glob

def find_coord(pic_path):
    img = cv.imread(pic_path)
    path = 'models'
    model = torch.hub.load(path, 'best', source='local', force_reload=True)


    box_list = []
    h, w, c = img.shape[:3]
    result = model(img)
    x1, y1, x2, y2, confidence, clas = result.xyxy[0][0] #most confidence result
    x1 = x1.item() #convert to float
    y1 = y1.item()
    x2 = x2.item()
    y2 = y2.item()
    confidence = confidence.item()
    cv.rectangle(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),3)
#     cv.imwrite(path,i)
    cv.imwrite(pic_path.replace('source','output'), img)
    with open("coord.txt", "a") as text_file:
        text_file.write(str((x1+x2)/2)+' ') #x_coord
        text_file.write(str((y1+y2)/2)+'\n') #y_coord

if __name__ == "__main__":
    #删除储存坐标的txt文档内容
    file = open('coord.txt', 'r+')
    file.truncate(0)
    file.close()
    for pic_path in glob.glob("source/*"):
        find_coord(pic_path)
