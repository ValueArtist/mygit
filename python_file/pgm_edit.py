import numpy as np
from PIL import Image


def pgm_crop(f, f_n, t):
    x0 = t[0]
    y0 = t[1]
    x1 = t[0] + t[2]
    y1 = t[1] + t[3]
    im = Image.open(f)
    if x1 > im.size[0] or y1 > im.size[1]:
        print('error')
        return
    dt = np.dtype('>u2') #定义np的数据类型，>大端序，u2=uint16
    lis = list(im.getdata())
    l = np.array(lis, dtype=dt)
    image = l.reshape(im.size[1], im.size[0])
    image1 = image[y0: y1]
    for i in range(t[3]):
        image1[i] = image[i+y0][x0: x1]
    image2 = image1.reshape(image1.shape[0] * image1.shape[1])
    head = 'P5\n' + str(image1.shape[1]) + ' ' + str(image1.shape[0]) + '\n65535\n'
    fp = open(f_n, 'w', newline='\n')
    fp.write(head)
    image2.tofile(fp)
    fp.close()
    return


'''raw图crop操作, 两种方法，第一种方法利用Image的crop方法，直接调用；
   第二种方法利用numpy数组里的操作，较复杂，但能熟悉处理过程'''
if __name__ == '__main__':
    # file = 'C:/Users/y/Desktop/1111/LSC/raw-1632x1224-870-128-1-20170805091447-LSC-D65.pgm'
    # im = Image.open(file)
    # box = (0, 152, 1632, 1070)
    # im1 = im.crop(box)
    # im1.save('C:/Users/y/Desktop/1111/LSC/raw-1632x1224-tmp-new.pgm')

    file = 'C:/Users/y/Desktop/1111/LSC/raw-1632x1224-870-128-1-20170805091447-LSC-D65.pgm'
    new_file = 'C:/Users/y/Desktop/1111/LSC/raw-1632x1224-870-128-1-tmp-new.pgm'
    box = (0, 152, 1632, 918)
    pgm_crop(file, new_file, box)