import os
from tkinter import *
import threading
import tkinter.messagebox


def get_awb_data():
    global ISP
    while run_flag:
        command = 'adb shell "io -4 -l 0x20 ' + ISP + '0528" '
        data = os.popen(command).read().split()
        # print(data)
        ISP_AWB_REF = data[1]
        # print(ISP_AWB_REF)
        if ISP_AWB_REF == 'deaddead':
            print('isp is dead, please open the camera')
        else:
            AWB_REF_CR = str(int(ISP_AWB_REF[4:6], 16))
            AWB_REF_CB = str(int(ISP_AWB_REF[6:8], 16))
            # print('AWB_REF_CR = ' + str(AWB_REF_CR))
            # print('AWB_REF_CB = ' + str(AWB_REF_CB))
            ISP_AWB_THRESH = data[2]
            AWB_MAX_Y = str(int(ISP_AWB_THRESH[0:2], 16))
            AWB_MIN_Y = str(int(ISP_AWB_THRESH[2:4], 16))
            AWB_MAX_CSUM = str(int(ISP_AWB_THRESH[4:6], 16))
            AWB_MIN_C = str(int(ISP_AWB_THRESH[6:8], 16))
            ISP_AWB_GAIN_G = data[6]
            AWB_GAIN_GR = str('{:.3f}'.format(int(ISP_AWB_GAIN_G[1:4], 16)/256))
            AWB_GAIN_GB = str('{:.3f}'.format(int(ISP_AWB_GAIN_G[5:8], 16)/256))
            ISP_AWB_GAIN_RB = data[7]
            AWB_GAIN_R = str('{:.3f}'.format(int(ISP_AWB_GAIN_RB[1:4], 16)/256))
            AWB_GAIN_B = str('{:.3f}'.format(int(ISP_AWB_GAIN_RB[5:8], 16)/256))
            '''
            awb_white_cnt = str(int(data[8][1:8], 16))
            # print(awb_white_cnt)
            isp_awb_mean = data[9]
            awb_mean_y = str(int(isp_awb_mean[2:4], 16))
            awb_mean_cb = str(int(isp_awb_mean[4:6], 16))
            awb_mean_cr = str(int(isp_awb_mean[6:8], 16))
            # print(awb_mean_y, awb_mean_cb, awb_mean_cr)
            '''
            v1.set('R_gain = ' + AWB_GAIN_R + '\n Gr_gain = ' + AWB_GAIN_GR + '\nGb_gain = '
                   + AWB_GAIN_GB + '\n B_gain = ' + AWB_GAIN_B)
            v2.set('Ref_Cr = ' + AWB_REF_CR + '\nRef_Cb = ' + AWB_REF_CB + '\nMax_Y = ' + AWB_MAX_Y
                   + '\nMin_Y = ' + AWB_MIN_Y + '\nMax_CSum = ' + AWB_MAX_CSUM + '\nMinC = ' + AWB_MIN_C)
    return


def get_awb():
    global run_flag, bus, ISP
    if ISP not in bus:
        ISP = get_bus_address()
    run_flag = 1
    th = threading.Thread(target=get_awb_data)
    th.setDaemon(True)  # 守护线程
    th.start()
    return


def stop():
    global run_flag
    run_flag = 0
    return


def get_bus_address():
    os.system('adb root')
    os.system('adb remount')
    global bus
    for i in range(len(bus)):
        try:
            command = 'adb shell "io -4 -l 0x4 ' + bus[i] + '052C" '
            result = os.popen(command).read().split()[1]
            # print(result)
            crc = int(result[6:8], 16)
            # print(crc)
            if 0 < crc < 30 or result == 'deaddead':
                print(bus[i])
                return bus[i]
        except:
            print('')
    return 'NULL'


if __name__ == '__main__':
    run_flag = 0
    ''' 3368, px30/3326 ,1808, 1108 '''
    bus = ['0xff91', '0xff4a', '0xffb5', '0x3002']
    ISP = get_bus_address()
    top = Tk()
    top.title('AWB')
    top.geometry('400x300')
    top.resizable(width=False, height=False)
    top['bg'] = 'LightSkyBlue'

    frm0 = tkinter.Frame(top, bg='Lavender')
    frm0.pack(side=TOP,pady=10)

    v1 = StringVar()
    v2 = StringVar()
    la1 = Label(frm0, textvariable=v1, fg='red', bg='Lavender', font=('Arial', 16)).pack(side=LEFT, padx=20, pady=10)
    la2 = Label(frm0, textvariable=v2, fg='green', bg='Lavender', font=('Arial', 12)).pack(side=LEFT, padx=20, pady=10)
    v1.set("R_gain = 0    \nGr_gain = 0    \nGb_gain = 0    \nB_gain = 0    ")
    v2.set("Ref_Cr = 0  \nRef_Cb = 0  \nMax_Y = 0  \nMin_Y = 0 \nMax_CSum = 0\nMinC = 0")
    b1 = Button(top, text='run', font=('Arial', 12), width=10, height=1, command=get_awb)
    b2 = Button(top, text='stop', font=('Arial', 12), width=10, height=1, command=stop)
    b3 = Button(top, text='quit', font=('Arial', 12), width=10, height=1, command=top.quit)
    b1.pack(side=LEFT, padx=15, pady=5)
    b2.pack(side=LEFT, padx=15, pady=5)
    b3.pack(side=LEFT, padx=15, pady=5)
    top.mainloop()
