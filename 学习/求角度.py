# 计算任意两向量之间的夹角
#https://blog.csdn.net/DSTJWJW/article/details/84258760 
import math 

AB = [1,-3,5,-1]
CD = [4,1,4.5,4.5]
EF = [2,5,-2,6]
PQ = [-3,-4,1,-6]

def angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180/math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180/math.pi)
    # print(angle2)
    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle

ang1 = angle(AB, CD)
print("AB和CD的夹角")
print(ang1)
ang2 = angle(AB, EF)
print("AB和EF的夹角")
print(ang2)
ang3 = angle(AB, PQ)
print("AB和PQ的夹角")
print(ang3)
ang4 = angle(CD, EF)
print("CD和EF的夹角")
print(ang4)
ang5 = angle(CD, PQ)
print("CD和PQ的夹角")
print(ang5)
ang6 = angle(EF, PQ)
print("EF和PQ的夹角")
print(ang6)



# 用Python求解已知两条线段的顶点坐标，求两条线的夹角的方法
# https://blog.csdn.net/qq_41058594/article/details/85887433

# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 14:30:10 2019

@author: dell
"""

#两条线段的夹角的计算
#向量思维

import math
import numpy as np

#得到向量的坐标以及向量的模长
class Point(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def vector(self):
        c = (self.x1 - self.x2, self.y1 - self.y2)
        return c

    def length(self):
        d = math.sqrt(pow((self.x1 - self.x2), 2) + pow((self.y1 - self.y2), 2))
        return d

#计算向量夹角
class Calculate(object):
    def __init__(self, x, y, m, n):
        self.x = x
        self.y = y
        self.m = m
        self.n = n

    def Vector_multiplication(self):
        self.mu = np.dot(self.x, self.y)
        return self.mu

    def Vector_model(self):
        self.de = self.m * self.n
        return self.de

    def cal(self):
        result = Calculate.Vector_multiplication(self) / Calculate.Vector_model(self)
        return result

if __name__ == '__main__':

    first_point = Point(1, 2, 3, 2)
    two_point = Point(3, 5, 4, 2)
    ca = Calculate(first_point.vector(), two_point.vector(), first_point.length(), two_point.length())
    print('两向量的夹角', ca.cal())
