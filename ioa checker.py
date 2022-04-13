import pandas as pd
import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QErrorMessage, QFileDialog
)

from ioa_gui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.metric = str(self.ui.comboBox.currentText())

        self.ui.pushButton.clicked.connect(self.csv_one)
        self.ui.pushButton_2.clicked.connect(self.csv_two)
        self.ui.pushButton_3.clicked.connect(self.calculate)
        self.ui.comboBox.currentTextChanged.connect(self.text_changed)

    def csv_one(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, ".csv file", "", ".csv file (*.csv)")
            if file_name:
                self.ui.lineEdit.setText(file_name)
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Not valid file')
            error_dialog.exec_()

    def csv_two(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self, ".csv file", "", ".csv file (*.csv)")
            if file_name:
                self.ui.lineEdit_2.setText(file_name)
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Not valid file')
            error_dialog.exec_()

    def calculate(self):
        try:
            df1 = pd.read_csv(self.ui.lineEdit.text())
            df2 = pd.read_csv(self.ui.lineEdit_2.text())
            # print(self.metric)
            if self.metric == 'Performance' or self.metric == 'Communication' or self.metric == 'Positive (Affect)' or self.metric == 'Negative (Affect)':
                freq_df1 = df1.shape[0]
                freq_df2 = df2.shape[0]
                ioa = 0
                if freq_df1 < freq_df2:
                    ioa = freq_df1/freq_df2
                else:
                    ioa = freq_df2/freq_df1
                self.ui.lineEdit_3.setText(str(ioa))

                if ioa < float(self.ui.lineEdit_4.text()):
                    self.ui.textEdit.setText(
                        "fix ioa score. Recode the video together")
                else:
                    self.ui.textEdit.setText("N/A")
        except:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Check inputs, something went wrong')
            error_dialog.exec_()

    def text_changed(self):
        self.metric = str(self.ui.comboBox.currentText())


if __name__ == '__main__':
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
