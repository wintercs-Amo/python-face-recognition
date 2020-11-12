# coding:utf-8

import os
import numpy as np
import dlib
import io
import cv2 as cv
import imutils
from DBHelper import *
import json


# 校验对比返回最接近的值
# 定义两个列表用于存储名字与特征数据
namelist = []
datalist = []
# 定义一个用于存储需要检测的图片的人脸特征数据列表
dist = []
# 初始化数据库连接
db = Mssql()
list = db.Query("select * from pop")
for item in list:
    # 由于pymssql版本问题，中文的需要使用一下encode等进行格式化，否则中文乱码
    namelist.append(item[1].encode('latin1').decode('gbk'))
    # 将数据进行格式化
    tzlist = json.loads(item[2])['data']
    # 将数据转为np模式
    vv = np.array(tzlist)
    # 添加到特征数据列表
    datalist.append(vv)
    # 加载人脸识别模型
    detector = dlib.get_frontal_face_detector()
    # 加载人脸关键点检测模型
    predictor = dlib.shape_predictor('static/FaceTzData/shape_predictor_68_face_landmarks.dat')
    # 加载图片
    image = cv.imread(r'C:\Users\Administrator\Desktop\5.jpg')
    # 图片转灰
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 人脸特征模型
    face_rec_model = dlib.face_recognition_model_v1('static/FaceTzData/dlib_face_recognition_resnet_model_v1.dat')
    # 人脸检测
    rects = detector(gray, 1)
    # 遍历
    for k, rect in enumerate(rects):
        # 标记人脸中的68个关键点
        shape = predictor(image, rect)
        # 提取特征
        face_descriptor = face_rec_model.compute_face_descriptor(image, shape)
        # 特征转np模式（便于后期计算）
        d_test = np.array(face_descriptor)
        # 遍历进行对比
        for i in datalist:
            # 进行欧式距离计算
            dist_ = np.linalg.norm(i - d_test)
            # 将只存入dist
            dist.append(dist_)

    # 训练集人物和距离组成一个字典
    c_d = dict(zip(namelist, dist))
    # 比较字段得出最接近的值
    cd_sorted = sorted(c_d.items(), key=lambda d: d[1])
    r = (cd_sorted[0][0], cd_sorted[0][1])

if r:
    # 0.5为阈值，设定多少之内可以认定为此人
    if float(r[1]) <= 0.5:
        print ('哈哈被我认出来啦！你一定是'+r[0])
        print(r[1])
    else:
        print ('哎呀对不起，我不认识你！尝试添加人物进素材库后，再次尝试')
        print(r[1])
else:
    print ('哎呀对不起，一定要拍到正脸哦')
