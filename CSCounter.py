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
