import os
from PIL import Image
import numpy as np
import shutil


def open_pgm(f):
    im = Image.open(f)
    lis = list(im.getdata())
    img = np.array(lis)
    img = (img / 256).astype(np.uint8)
    avg = np.mean(img)
    maximum = np.max(img)
    # minimum = np.min(img)
    # y = np.percentile(img, 97)
    # print(maximum, y)
    return avg, maximum


def check_raw(string, light):
    if string == 'BLC'or string == 'DPF':
        avg_low = 0
        maximum = 0
    elif string == 'LSC':
        maximum = 210
        avg_low = 0
    elif string == 'CC':
        avg_low = 60
        avg_high = 120
        maximum = 0
    elif string == 'AWB':
        avg_low = 60
        avg_high = 90
        maximum = 0
    else:
        return
    os.chdir(file_path)
    file_list = os.listdir(file_path)
    for i in file_list:
        if os.path.splitext(i)[1] == '.pgm':
            if avg_low == 0 and maximum == 0:
                if not os.path.exists(string):
                    os.mkdir(string)
                shutil.move(i, string)
            else:
                file_name = os.path.splitext(i)[0]
                n = file_name.split('EXPT', 1)
                name_new = n[0] + light + '_EXPT' + n[1] + '.pgm'
                a = open_pgm(i)
                if avg_low != 0:
                    if avg_low < a[0] < avg_high:
                        os.rename(i, name_new)
                        print('avg is ', int(a[0]), ',keep the raw file')
                        if not os.path.exists(string):
                            os.mkdir(string)
                        shutil.move(name_new, string)
                    else:
                        os.remove(i)
                        print('avg is', int(a[0]), ',remove the raw file')
                if maximum != 0:
                    if maximum - 20 < a[1] < maximum + 20:
                        os.rename(i, name_new)
                        print('max is ', a[1], ',keep the raw file')
                        if not os.path.exists(string):
                            os.mkdir(string)
                        shutil.move(name_new, string)
                    else:
                        os.remove(i)
                        print('max is', a[1], ',remove the raw file')
    return


def dump():
    # os.system('adb root')
    # os.system('adb remount')
    cmd = list()
    cmd.append('adb push ' + file_path + file + linux_path)
    cmd.append('adb shell chmod 777 ' + linux_path + file)
    cmd.append('adb shell ./' + linux_path + file)
    cmd.append('adb pull ' + linux_path + '/raw ' + file_path)
    for i in cmd:
        print(i)
        os.system(i)
    return


def set_exp_gain(cnt, gain, exp):
    f_r = open(file_path + file, 'r')
    lines = f_r.readlines()
    with open(file_path + file, 'w', newline='\n') as f_w:
        for line in lines:
            if -1 != line.find('for CNT'):
                line = cnt
            elif -1 != line.find('for GAIN'):
                line = gain
            elif -1 != line.find('for EXP'):
                line = exp
            f_w.write(line)
    return


if __name__ == '__main__':
    linux_path = 'tmp'
    file_path = 'C:/Users/y/Desktop/test'
    file = '/dump.sh '
    set_cnt = 'for CNT in `seq 1 1 1`; do\n'
    set_gain = 'for GAIN in `seq 128 128 1024`; do\n'
    set_exp = 'for EXP in `seq 2310 385 2310`; do\n'
    # tuning = 'BLC'
    # tuning = 'LSC'
    # tuning = 'CC'
    # tuning = 'AWB'
    tuning = 'DPF'
    # light_source = 'D50'
    light_source = 'D65'
    # light_source = 'CWF'
    # light_source = 'TL84'
    # light_source = 'A'
    set_exp_gain(set_cnt, set_gain, set_exp)
    dump()
    check_raw(tuning, light_source)
