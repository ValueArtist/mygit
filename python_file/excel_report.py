import openpyxl
from openpyxl.drawing.image import Image
import os


def merge_pic(col, row):
    wb = openpyxl.load_workbook('RK_Subjective_Standard_空白.xlsx')
    ws1 = wb['白平衡&色彩还原']
    w = ws1.column_dimensions[col].width
    w_x = 8
    h_x = 1.328
    file_list = os.listdir('./CWF/')
    num = 0
    for i in file_list:
        if os.path.splitext(i)[1] == '.jpg':
            s = './CWF/' + i
            h = ws1.row_dimensions[row+num].height
            img = Image(s)
            img.width = w * w_x
            img.height = h * h_x
            ws1.add_image(img, col + str(row+num))
            num += 1
    wb.save('RK_Subjective_Standard_OK.xlsx')
    return


if __name__ == '__main__':
    merge_pic('D', 4)



