import traceback
import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from scheme import Ui_MainWindow
import CSCounter_lib as cs


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #
        # variables
        #

        self.current_CS = None
        self.endian = 'little'
        self.old_group_len = None
        self.base = 16
        # Put "1" in polynomial start
        self.crc_8_params = {'poly': 0x131, 'rev': False, 'initCrc': 0xFF, 'xorOut': 0x00}
        self.crc_16_params = {'poly': 0x11021, 'rev': False, 'initCrc': 0xFFFF, 'xorOut': 0x0000}
        self.input = ''

        #
        # input actions connecting
        #
        self.ui.textEdit_input.textChanged.connect(self.input_handler)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.radioButton_bin.clicked.connect((lambda: self.change_base(2)))
        self.ui.radioButton_dec.clicked.connect((lambda: self.change_base(10)))
        self.ui.radioButton_hex.clicked.connect((lambda: self.change_base(16)))

        #
        # output actions connecting
        #
        self.ui.lineEdit_format.editingFinished.connect(self.transform)
        self.ui.checkBox_transform.clicked.connect(self.transform)
        self.ui.checkBox_group.clicked.connect(self.group)
        self.ui.spinBox_group.valueChanged.connect(self.group)
        self.ui.pushButton_endian.clicked.connect(self.change_endian)
        self.change_endian()
        self.locker()

    def locker(self):
        """
        Locks some functions. The will be available in future
        :return:
        """
        locked_functions = [self.ui.radioButton_bin,  self.ui.radioButton_dec,  self.ui.radioButton_hex]
        for function in locked_functions:
            function.setEnabled(False)

    def input_handler(self):
        """
        Input processing
        :return:
        """
        self.group()
        self.move_cursor_at_end()

    def set_text(self, text):
        """
        Set text to TextEdit_input
        :param text: text to set
        :return:
        """
        if type(text) is list:
            text = ''.join(text)
        elif type(text) is str:
            text = text.replace(' ', '')

        self.ui.textEdit_input.setPlainText(text)

    def move_cursor_at_end(self):
        cursor = self.ui.textEdit_input.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.textEdit_input.setTextCursor(cursor)

    def calculate(self):
        """
        Find out what is current CS and calculates
        :return:
        """
        # TODO take in account format
        if self.ui.checkBox_transform.checkState():
            pass
        else:
            result = ''
            cs_name = self.ui.toolBox_CS.itemText(self.ui.toolBox_CS.currentIndex())
            text = self.ui.textEdit_input.toPlainText()
            if cs_name == 'Суммирование':
                module = int(self.ui.lineEdit_abs_2.text())
                result = cs.check_sum_counter(cs.group_text(text, 4), module)
            elif cs_name == 'CRC-8':
                pass
            elif cs_name == 'CRC-16':
                pass
            self.ui.textBrowser_output.setText(result)

    def change_base(self, new_base):
        """
        Changes numeral system base to entered values and group bytes_meaning by 1
        :param new_base: new base (2 - bin, 10 - dec, 16 - hex)
        :return:
        """
        text = self.ui.textEdit_input.toPlainText()
        if new_base != 16 and self.base == 16:
            self.old_group_len = self.ui.spinBox_group.value()
            self.ui.spinBox_group.setValue(1)
        elif new_base == 16:
            if self.base != 16:
                self.ui.spinBox_group.setValue(self.old_group_len)
        else:
            self.ui.spinBox_group.setValue(1)

        if len(text) != 0:
            bases = {2: 'b', 10: '', 16: 'x'}

            old_bytes = text.split()
            new_bytes = []
            for old_byte in old_bytes:
                new_bytes.append(format(int(old_byte, self.base), bases[new_base]))
            with TempDisconnect(self, self.input_handler):
                self.ui.textEdit_input.setPlainText(' '.join(new_bytes))

        self.base = new_base

    def transform(self):
        """
        Transforms input according to format
        :return:
        """
        text_format = self.ui.lineEdit_format.text()
        text = self.ui.textEdit_input.toPlainText()
        if self.ui.checkBox_transform.checkState():
            text = cs.text_handler(text, text_format, to_strip=False)
            with TempDisconnect(self, self.input_handler):
                self.ui.textEdit_input.setPlainText(text)
        else:
            text = cs.text_handler(text, text_format, to_strip=True)
            # text_format = text_format.replace('{}', '')
            # text = text.replace(text_format, '')
            # text.replace(' ', '')
            self.ui.textEdit_input.setPlainText(text)




    def group(self):
        """
        Groups bytes in input
        :return:
        """
        if self.ui.checkBox_transform.checkState():
            pass
        else:
            text = self.ui.textEdit_input.toPlainText()
            with TempDisconnect(self, self.input_handler):
                if self.ui.checkBox_group.checkState():
                    self.ui.textEdit_input.setPlainText(' '.join(cs.group_text(text, self.ui.spinBox_group.value() * 2)))
                else:
                    self.ui.textEdit_input.setPlainText(''.join(cs.group_text(text, 2)))

    def change_endian(self):
        """
        Changes endian and button text
        :return:
        """
        if self.endian == 'little':
            self.endian = 'big'
        else:
            self.endian = 'little'

        self.ui.pushButton_endian.setText(self.endian)
        if self.ui.checkBox_transform.checkState():
            pass
        else:
            text = cs.reverse_bytes(self.ui.textEdit_input.toPlainText())
            with TempDisconnect(self, self.input_handler):
                self.ui.textEdit_input.setPlainText(''.join(text))
            self.group()

    @classmethod
    def start(cls):
        sys.excepthook = MainWindow.excepthook

        app = QtWidgets.QApplication([])
        application = cls()
        application.show()

        sys.exit(app.exec())

    @staticmethod
    def excepthook(exc_type, exc_value, exc_tb):
        """
        For catching errors in PyQt
        """
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print(tb)
        QtWidgets.QApplication.quit()


class TempDisconnect:
    """
    Temporarily disconnect the method from QMainWindow, and connects again with exit
    """
    def __init__(self, QMainWindow, method_to_disconnect):
        self.qt_window = QMainWindow
        self.connected_method = method_to_disconnect

    def __enter__(self):
        self.qt_window.ui.textEdit_input.textChanged.disconnect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.qt_window.ui.textEdit_input.textChanged.connect(self.connected_method)


if __name__ == '__main__':
    MainWindow.start()