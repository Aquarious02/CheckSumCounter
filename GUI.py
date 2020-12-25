import traceback
import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from scheme import Ui_MainWindow
import CSCounter as cs


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
        # Put "1" in polynomial start
        self.crc_8_params = {'poly': 0x131, 'rev': False, 'initCrc': 0xFF, 'xorOut': 0x00}
        self.crc_16_params = {'poly': 0x11021, 'rev': False, 'initCrc': 0xFFFF, 'xorOut': 0x0000}
        self.input = ''

        #
        # input actions connecting
        #
        self.ui.textEdit_input.textChanged.connect(self.input_handler)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.radioButton_bin.clicked.connect((lambda: self.base_change(2)))
        self.ui.radioButton_dec.clicked.connect((lambda: self.base_change(10)))
        self.ui.radioButton_hex.clicked.connect((lambda: self.base_change(16)))

        #
        # output actions connecting
        #
        self.ui.lineEdit_format.editingFinished.connect(self.transform)
        self.ui.checkBox_transform.clicked.connect(self.transform)
        self.ui.checkBox_group.clicked.connect(self.group)
        self.ui.spinBox_group.valueChanged.connect(self.group)
        self.ui.pushButton_endian.clicked.connect(self.change_endian)
        self.change_endian()

    def input_handler(self):
        """
        Input processing
        :return:
        """
        self.group()
        self.move_cursor_at_end()


    def move_cursor_at_end(self):
        cursor = self.ui.textEdit_input.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.ui.textEdit_input.setTextCursor(cursor)

    def calculate(self):
        """
        Find out what is current CS and calculates
        :return:
        """
        pass

    def change_base(self, new_base):
        """
        Changes numeral system base to entered values
        :param new_base: new base (2 - bin, 10 - dec, 16 - hex)
        :return:
        """
        pass

    def transform(self):
        """
        Transforms input according to format
        :return:
        """
        pass

    def group(self):
        """
        Groups bytes in input
        :return:
        """
        text = self.ui.textEdit_input.toPlainText()
        self.ui.textEdit_input.textChanged.disconnect()
        if self.ui.checkBox_group.checkState():
            self.ui.textEdit_input.setPlainText(' '.join(cs.group_text(text, self.ui.spinBox_group.value() * 2)))
        else:
            self.ui.textEdit_input.setPlainText(''.join(cs.group_text(text, 2)))
        self.ui.textEdit_input.textChanged.connect(self.input_handler)

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


if __name__ == '__main__':
    MainWindow.start()