from CSCounter_lib import *
from Temperature_Controller.sandbox import ui_py_converter

if __name__ == '__main__':
    ui_py_converter('G:\YandexDisk\cloud\PycharmProjects\Work\CheckSumCounter\scheme.ui',
                    'G:\YandexDisk\cloud\PycharmProjects\Work\CheckSumCounter\scheme.py')

    # print(check_sum_counter('0220 0040 0140 0004 1808 1320 c4bc 041a 00e1 0001 0002 0060 0d00 012c 0064 0001 0002 '
    #                         '001f 0200 0190 076c 0200 0190 076c 212c 304b 0060 0d01 01c2 0064 0002 001f 0200 0190 '
    #                         '076c 0200 0190 076c 212c 304b 0060 0d02 0258 0064 0002 001f 0200 0190 076c 0200 0190 '
    #                         '076c 212c 304b 0060 0d03 02ee 0064 0002 001f 0200 0190 076c 0200 0190 076c 212c 304b '
    #                         '0060 0d04 0384 0064 0002 001f 0200 0190 076c 0200 0190 076c 212c 304b 098c'))