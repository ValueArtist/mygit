import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import sys
import cv2
import math


def pgm_to_rgb(file):
    im = Image.open(file)
    lis = list(im.getdata())
    l = np.array(lis)
    l = (l / 256).astype(np.uint8)
    image = l.reshape(im.size[1], im.size[0])
    # bayer_fmt = ['RGGB', 'GRBG', 'BGGR', 'GBRG']
    image = cv2.cvtColor(image, 48)
    return image


def pgm_to_rgb_saved():
    folder = '/CC'
    path = os.path.realpath(sys.argv[0])
    path = os.path.split(path)[0] + folder
    file_list = os.listdir(path)
    for i in file_list:
        if os.path.splitext(i)[1] == '.pgm':
            n = './CC/' + os.path.splitext(i)[0] + '.bmp'
            img = pgm_to_rgb('./CC/' + i)
            cv2.imwrite(n, img)
    return


def cal_awb_gain(img):
    i = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
    j = i.sum(axis=0)
    k = j / (img.shape[0] * img.shape[1])
    b_gain = k[1] / k[0]
    r_gain = k[1] / k[2]
    print('r_gain=', r_gain, 'b_gain=', b_gain)
    return [r_gain, b_gain]


def get_wb_point():
    folder = '/WB'
    path = os.path.realpath(sys.argv[0])
    path = os.path.split(path)[0] + folder
    file_list = os.listdir(path)
    w = []
    for i in file_list:
        if os.path.splitext(i)[1] == '.pgm':
            img = pgm_to_rgb('./WB/' + i)
            gain = cal_awb_gain(img)
            w.append(gain)
    print(w)
    return w


def show(white, color):
    # plt.xlim(1, 2)
    # x = np.arange(1.2, 2, 0.02)
    for i in range(len(white)):
        # plt.scatter(math.log(white[i][0]), math.log(white[i][1]), color='blue', marker='s', alpha=0.8)
        plt.scatter(white[i][0], white[i][1], color='blue', marker='s', alpha=0.8)
    for i in range(18):
        plt.scatter(color[i][0], color[i][1], color='red', marker='o', alpha=0.8)
    for i in range(18, 36):
        plt.scatter(color[i][0], color[i][1], color='red', marker='x', alpha=0.8)
    for i in range(36, 54):
        plt.scatter(color[i][0], color[i][1], color='red', marker='+', alpha=0.8)
    for i in range(54, len(color)):
        plt.scatter(color[i][0], color[i][1], color='red', marker='*', alpha=0.8)
        # plt.scatter(math.log(color[i][0]), math.log(color[i][1]), color='red', marker='*', alpha=0.8)
    # plt.plot(x, -1.0912 * x + 3.0706)  # y = -1.0912 * x + 3.2706
    # plt.plot(x, -1.0912 * x + 3.4706)
    plt.show()
    return


def show_mstar(white, color):
    for i in range(len(white)):
        plt.scatter(100/white[i][0], 100/white[i][1], color='blue', marker='s', alpha=0.8)
    for i in range(18):
        plt.scatter(100/color[i][0], 100/color[i][1], color='red', marker='o', alpha=0.8)
    for i in range(18, 36):
        plt.scatter(100/color[i][0], 100/color[i][1], color='red', marker='x', alpha=0.8)
    for i in range(36, 54):
        plt.scatter(100/color[i][0], 100/color[i][1], color='red', marker='+', alpha=0.8)
    for i in range(54, len(color)):
        plt.scatter(100/color[i][0], 100/color[i][1], color='red', marker='*', alpha=0.8)
    plt.show()
    return


def get_cs_std(strings):
    f = open(strings, 'r')
    c = f.read()
    f.close()
    c = c.strip('[]')
    d = c.split()
    e = []
    for i in range(len(d)):
        e.append(int(d[i]))
    f = np.array(e).reshape(24, 3)
    e = []
    for i in range(len(f)):
        e.append([f[i][1]/f[i][2], f[i][1]/f[i][0]])
    # print(e)
    return e


def get_color_chart_data():
    colour = []
    a = get_cs_std('A.txt')
    # print(a)
    tl84 = get_cs_std('TL84.txt')
    cwf = get_cs_std('CWF.txt')
    d65 = get_cs_std('D65.txt')
    lenth = 18
    for i in range(lenth):
        colour.append(a[i])
    for i in range(lenth):
        colour.append(tl84[i])
    for i in range(lenth):
        colour.append(cwf[i])
    for i in range(lenth):
        colour.append(d65[i])
    # print(colour)
    # print(len(colour))
    return colour


if __name__ == '__main__':
    # white_piont = get_wb_point() #获取几个光源的白点数值，把数据存放在列表中返回
    # pgm_to_rgb_saved() #将ccm的raw图转化成rgb图并保存
    white_piont = [[1.221523529552882, 1.9005078551478543], [1.584056936699208, 1.471756246637429], [1.8056047747022272, 1.2229159554387203], [1.6049064999055553, 1.7067048489954857], [1.497660652787104, 1.6357102437434043]]
    color = get_color_chart_data()
    show_mstar(white_piont, color)
