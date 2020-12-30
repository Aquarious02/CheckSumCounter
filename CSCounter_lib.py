from crcmod import mkCrcFun


def text_handler(text: str, text_format: str, to_strip=False) -> str:
    """
    transform text to format. Or strip format
    :param text: text to transofrm
    :param text_format: to use in str.format. e.g. {}_x,
    :param to_strip: remove format if True (Returns with spaces)
    :return:
    """
    if not to_strip:
        text_blocks = text.split()
        for i, number in enumerate(text_blocks):
            text_blocks[i] = text_format.format(number)
        return ' '.join(text_blocks)
    else:
        text_format = text_format.split('{}')
        text_blocks = text.split()
        start_len, end_len = len(text_format[0]), len(text_format[1])
        for i, number in enumerate(text_blocks):
            text_blocks[i] = number[start_len: -end_len]
        return ' '.join(text_blocks)


def text_from_bytes(_bytes:bytes) -> str:
    text = []
    for byte in _bytes:
        text.append(format(byte, '02x'))
    return ''.join(text)


def bytes_from_text(text):
    if type(text) is list:
        text = ''.join(text)
    elif type(text) is str:
        text = text.replace(' ', '')
    int_bytes = [int(byte, 16) for byte in group_text(text, 2)]
    bytes_in_list = [byte.to_bytes(1, byteorder='little') for byte in int_bytes]

    real_bytes = b''
    for byte in bytes_in_list:
        real_bytes += byte

    return real_bytes


def reverse_bytes(text):
    """
    Changes endian in input
    :return: list of bytes, group by 1
    """
    if type(text) is list:
        text = ''.join(text)
    elif type(text) is str:
        text = text.replace(' ', '')
    text_bytes = group_text(text, 2)
    if len(text_bytes) != 0:
        for i in range(0, len(text_bytes) - len(text_bytes) % 2, 2):
            text_bytes[i], text_bytes[i + 1] = text_bytes[i + 1], text_bytes[i]
        return text_bytes
    else:
        return []


def group_text(text, group_len) -> list:
    """
    Groups bytes in input
    :param text: values come in group from this text
    :param group_len: len of groups in symbols
    :return:
    """
    text = text.replace(' ', '')
    return [text[i:i + group_len] for i in range(0, len(text), group_len)]


def crc_16(bytes_or_string_to_calculate) -> int:
    """
    Подсчет контрольной суммы по алгоритму CRC16 CCITT-FALSE
    :param bytes_or_string_to_calculate: str or bytes
    :return: crc16
    """

    if type(bytes_or_string_to_calculate) is str:
        bytes_or_string_to_calculate = bytes_or_string_to_calculate.encode('utf8')

    crc16 = mkCrcFun(poly=0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)  # Put "1" in polynomial start
    """From https://issue.life/questions/35205702"""

    # TODO Find out what to put: bytes or string
    return crc16(bytes_or_string_to_calculate)


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


def check_sum_counter(values, module: int = 65536) -> int:
    if type(values) is str:
        values = values_handler(values)

    total_sum = sum(map(lambda x: int(x, 16), values))
    return total_sum % module + total_sum // module


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
