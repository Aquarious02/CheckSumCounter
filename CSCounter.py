from crcmod import mkCrcFun


def crc_16(bytes_or_string_to_calculate) -> int:
    """
    Подсчет контрольной суммы по алгоритму CRC16 CCITT-FALSE
    :param bytes_or_string_to_calculate: str or bytes
    :return: crc16
    """

    if type(bytes_or_string_to_calculate) is str:
        bytes_or_string_to_calculate = bytes_or_string_to_calculate.encode('utf8')

    crc16 = mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)  # Put "1" in polynomial start
    """From https://issue.life/questions/35205702"""

    # TODO Find out what to put: bytes or string
    return crc16(bytes_or_string_to_calculate)

# def crc_8


def values_handler(str_values: str) -> list:
    """
    values handling. Making list from str. Removing extra symbols
    :param str_values: values from input
    :return:
    """

    for symbol in ['h', 'x', 'х', 'ш', '\n']:
        str_values = str_values.replace(symbol, '')

    if len(str_values) == 0:
        raise TypeError('Неверный ввод')

    if ' ' in str_values:
        return str_values.split()
    else:
        return [str_values[i:i + 4] for i in range(0, len(str_values), 4)]


def check_sum_counter(values):
    if type(values) is str:
        values = values_handler(values)

    total_sum = sum(map(lambda x: int(x, 16), values))
    return format(total_sum % 65536 + total_sum // 65536, 'x')

instruction = '1. При вводе значений без пробелов, введенная строка будет поделена по 4 символа и расчет будет производиться по ним\n' \
              '2. Ввод производится в шестнадцатеричной системе счисления\n'

if __name__ == '__main__':
    values = None
    while values != '':
        try:
            values = input('Введите значения\n')
            if values != '':
                print(check_sum_counter(values))
            elif values == '?':
                print(instruction)
            else:
                input('press "Enter" to close\n')
        except TypeError as e:
            print(e)
        except KeyboardInterrupt:
            input('press "Enter" to close\n')
