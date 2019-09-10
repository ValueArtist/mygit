import xml.etree.ElementTree as ET
import os
import sys


def change_dpf_value(file, x):
    t = ET.parse(file)
    r = t.getroot()
    a = r.find('sensor/DPF').findall('cell')
    n = 1
    for i in a:
        b = i.find('nll_coeff_n')
        print('第' + str(n) + '组修改前：')
        print(b.text)
        c = b.text
        index = c.find('[')
        d = c.split()
        d[0] = d[0].split('[')[1]
        d[-1] = d[-1].split(']')[0]
        string = c[0:index+1]
        for j in range(len(d)):
            string += str(int(int(d[j]) * x)) + ' '
        string = string[:-1]
        string += ']'
        print('第' + str(n) + '组修改后：')
        n += 1
        print(string)
        # b.text = string + '\n' + '           '
        # t.write('GC2053_new.xml', encoding="utf-8", xml_declaration=True, method='xml')
    return


def openfile():
    path = os.path.realpath(sys.argv[0])
    path = os.path.split(path)[0]
    os.chdir(path)
    if len(sys.argv) >= 2:
        i = sys.argv[1]
        print(i)
        return i
    else:
        file_list = os.listdir('./')
        for i in file_list:
            if os.path.splitext(i)[1] == '.xml':
                print(i)
                return i


if __name__ == '__main__':
    f = openfile()
    n = float(input("Enter your input: "))
    change_dpf_value(f, n)
    os.system('pause')
