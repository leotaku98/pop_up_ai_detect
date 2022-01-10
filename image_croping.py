import cv2 as cv
import numpy as np
import glob
import os
from PIL import Image,ImageDraw
import subprocess




def nums_are_similar(x1, x2):
    if ((x1 / x2) < 1.1 or (x1 / x2) > 0.9):
        return True
    else:
        return False

def linreg(X, Y):
    """
    return a,b in solution to y = ax + b such that root mean square distance between trend line and original points is minimized
    """
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in zip(X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    return (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det

def grouper(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    group = []
    temp_group = []
    for i in range(len(keys)-1):

        if keys[i+1] - keys[i]< 41 and nums_are_similar(values[i+1], values[i]) and values[i] < -0.04:
            temp_group.append(keys[i])
        else:
            group.append(temp_group)
            temp_group = []

    max_len = 0
    index = 0
    for i in range(len(group)):
        if len(group[i]) > max_len:
            max_len = len(group[i])
            index = i
    return (min(group[index]), max(group[index]))




def convert2gray(pic_path, left_bound, right_bound):
    ori_img = cv.imread(pic_path)
    R = ori_img[:,:,0]
    G = ori_img[:,:,1]
    B = ori_img[:,:,2]
    img = 0.2989 * R + 0.5870 * G + 0.1140 * B
    img = np.uint8(img)
    height, width = img.shape[:2]

    '''
    截取图片（高度）

    '''
    img = img[:int(height*2/3), :]
    img = img[:, int(width/4):int(width*3/4)]
    h, w = img.shape[:2]
    slope_list = []
    dictionary = dict()
    for row_index in range(1,h-1):

        slope, constant =  linreg(range(len(img[row_index])), img[row_index])
        slope_list.append(slope)
    match = 0
    for i in range(1, len(slope_list)-1):
        if slope_list[i] < 0 and \
        ((slope_list[i] / slope_list[i-1]) < 1.1 or (slope_list[i] / slope_list[i-1]) > 0.9):
            match += 1
            if match == 20:

                dictionary[i] = slope_list[i]
                match = 0
    top, bot = grouper(dictionary)



    ori_img =  ori_img[top:bot, int(left_bound) : int(right_bound)]
    cv.imwrite(pic_path.replace('source','output'), ori_img)



os.system('python detect.py')
file = open('coord.txt', 'r+')
boundarys = []
for line in file:
    boundarys.append(line)

i = 0
for pic_path in glob.glob("source/*"):
    convert2gray(pic_path, float((boundarys[i].split()[0])), float(boundarys[i].split()[1]) )
    i+=1
file.close()