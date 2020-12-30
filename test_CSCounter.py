from unittest import TestCase
from CSCounter_lib import *


class Test(TestCase):
    def setUp(self) -> None:
        self.user_inputs_to_split = ['0001 D0A527580211', '0001 D0A5 2758 0211', '0001D0A527580211', '0001D0A52758021 1',
                                     '0 0 01 D0A527580211']
        self.empty_user_inputs = ['', ' ']
        self.value = '1 ffff ffff 301 800f a000 a001 a002 a003 a004 a005 a006 a007 a008 a009 a00a'

    def test_values_handler(self):
        for user_input in self.user_inputs_to_split:
            with self.subTest(f'user input: {user_input}'):
                self.assertEqual(['0001', 'D0A5', '2758', '0211'], values_handler(user_input))

    def test_check_sum_counter(self):
        for user_input in self.user_inputs_to_split:
            with self.subTest(f'user input: {user_input}'):
                self.assertEqual('fa0f', check_sum_counter(user_input))

    def test_group_text(self):
        for user_input in self.user_inputs_to_split:
            with self.subTest(f'user input: {user_input}'):
                self.assertEqual(['0001', 'D0A5', '2758', '0211'], group_text(user_input, 4))
        with self.subTest('Not correct len'):
            self.assertEqual(['0001', 'D0A5', '2758', '02'],
                             group_text('0001D0A5275802', 4))

    def test_reverse_bytes(self):
        with self.subTest('Str input'):
            self.assertEqual(['34', '12', '78', '56', '90'], reverse_bytes('1234567890'))
        with self.subTest('Ling str input'):
            self.assertEqual(['34', '12', '78', '56', '11', '90', '13', '12', '15', '14', '17', '16', '18'],
                             reverse_bytes('12345678901112131415161718'))

        with self.subTest('List input'):
            self.assertEqual(['34', '12', '78', '56', '90'], reverse_bytes(['1234', '5678', '90']))

    def test_bytes_from_text(self):
        text = '1234567890'
        self.assertEqual(b'\x124Vx\x90', bytes_from_text(text))

    def test_test_handler(self):
        text = '1234 5678 90'
        # text = '0x1234_ш, 0x5678_ш, 0x90_ш,'
        with self.subTest('Format after {}'):
            self.assertEqual('1234_ш, 5678_ш, 90_ш,', text_handler(text, text_format='{}_ш,'))
        with self.subTest('Format before {}'):
            text_format = '0x{}_ш,'
            formatted_text = text_handler(text, text_format=text_format)
            self.assertEqual(text, text_handler(formatted_text, text_format, to_strip=True))



