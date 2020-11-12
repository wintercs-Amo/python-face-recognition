import os
import numpy as np
import dlib, io
import cv2 as cv
import imutils
import json
import pymssql
from DBHelper import Mssql

conn = pymssql.connect('BF-202007141918', 'sa', '123456', 'FaceDB')
detector = dlib.get_frontal_face_detector()
# 加载人脸关键点检测模型
predictor = dlib.shape_predictor('static/FaceTzData/shape_predictor_68_face_landmarks.dat')
# 人脸特征模型
face_rec_model = dlib.face_recognition_model_v1('static/FaceTzData/dlib_face_recognition_resnet_model_v1.dat')
# 读取图片
image = cv.imread(r'C:\Users\Administrator\Desktop\80.jpg')
# 设置图片大小
image = imutils.resize(image, width=500)
# 转灰度
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# 展示图片
# cv.namedWindow('qi win')
cv.imshow('qi', gray)
cv.waitKey(0)
cv.destroyAllWindows()
# 人脸检测
rects = detector(image, 1)

for k, rect in enumerate(rects):
    # 标记人脸中的68个关键点
    shape = predictor(gray, rect)
    # 提取特征
    face_descriptor = face_rec_model.compute_face_descriptor(image, shape)
    # 转np列表格式
    v = np.array(face_descriptor)
    # np列表转普通列表格式（转换的目的是方便数据库存储）
    tzlist = v.tolist()
    # 组合成json字符串格式并且存入数据库
    jsonstr = json.dumps({"data": tzlist})
    a = jsonstr

    if a:
        db1 = Mssql().Excute("insert into pop values('%s','%s')" % ('巨石强森', a))
        print ('添加成功！')
    else:
        print ('添加失败！')
