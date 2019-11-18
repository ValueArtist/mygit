import sys
sys.path.append('D:/python_00/venv/Lib/site-packages')
import cv2
import numpy
import os
from PIL import Image


def pgm_to_gray(file):
    im = Image.open(file)
    lis = list(im.getdata())
    l = numpy.array(lis)
    l = (l / 256).astype(numpy.uint8)
    image = l.reshape(im.size[1], im.size[0])
    return image


def cal_awb_gain(img):
    i = numpy.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
    j = i.sum(axis=0)
    k = j / (img.shape[0] * img.shape[1])
    b_gain = k[1] / k[0]
    r_gain = k[1] / k[2]
    # print('r_gain=', r_gain, 'b_gain=', b_gain)
    return [r_gain, b_gain]


def auto_bayerfmt(img):
    bayer_fmt = ['RGGB', 'GRBG', 'BGGR', 'GBRG']
    for i in range(4):
        img0 = cv2.cvtColor(img, 46+i)
        gain = cal_awb_gain(img0)
        if gain[0] > gain[1] > 1:
            print('bayer_fmt is: ' + bayer_fmt[i])
            return img0
    print('Error, bayer format error.')
    return cv2.cvtColor(img, 46)


def awb_ccm(img):
    i = numpy.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
    awb_gain = cal_awb_gain(img)
    # print('r_gain=', r_gain,  'b_gain=', b_gain)
    awb_gain = [awb_gain[1], 1, awb_gain[0]]
    l = i * awb_gain
    l = numpy.clip(l, 0, 255)
    ccm_gain = numpy.array([[1, -0, 0], [-0, 1, -0], [-0, -0, 1]])
    ccm_gain = ccm_gain.transpose()
    ccm_gain = ccm_gain[::-1]
    ccm_gain = ccm_gain[:, ::-1]
    l = numpy.dot(l, ccm_gain)
    j = numpy.reshape(l, (img.shape[0], img.shape[1], img.shape[2]))
    j = numpy.clip(j, 0, 255)
    j = j.astype(numpy.uint8)
    return j


def gamma(img, gam):
    gamma_table = [numpy.power(x/255.0, gam)*255 for x in range(256)]
    # gamma_table = [x for x in range(256)]
    gamma_table = numpy.array(gamma_table).astype(numpy.uint8)
    img1 = cv2.LUT(img, gamma_table)
    return img1


def isp(str):
    # img0 = raw_to_gray(str)
    img0 = pgm_to_gray(str)
    img3 = auto_bayerfmt(img0)
    img4 = awb_ccm(img3)
    img4 = gamma(img4, 0.8)
    return img4


def open():
    path = os.path.realpath(sys.argv[0])
    path = os.path.split(path)[0]
    os.chdir(path)
    if len(sys.argv) >= 2:
        i = sys.argv[1]
        j = os.path.split(i)[1]
        k = os.path.splitext(j)[0]
        # s = k + '.bmp'
        im = isp(i)
        # cv2.imwrite(s, im)
        cv2.namedWindow(k, cv2.WINDOW_NORMAL)
        cv2.imshow(k, im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        file_list = os.listdir('./')
        for i in file_list:
            if os.path.splitext(i)[1] == '.pgm':
                n = os.path.splitext(i)[0]
                # s = n + '.bmp'
                im = isp(i)
                # cv2.imwrite(s, im)
                cv2.namedWindow(n, cv2.WINDOW_NORMAL)
                cv2.imshow(n, im)
                cv2.waitKey(3000)
                cv2.destroyAllWindows()
                print('Open the image ' + i + ' sucessfully.')
    return


if __name__ == '__main__':
    try:
        open()
    except Exception as e:
        print('Exception')
        print(e)
        os.system('pause')
    else:
        os.system('color 0a')
        # print('——by wuruiyuan 201907 *^_^* .')
        # os.system('pause')

