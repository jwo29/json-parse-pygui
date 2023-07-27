# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1300, 500)
        self.setWindowTitle("Make Markdown Table from JSON")

        self.layout = QGridLayout()

        # 입력
        self.srcText = QTextEdit()
        self.srcText.returnPressed.connect(self.recturn_pressed)

        # 결과
        self.destText = QTextEdit()

        # 체크박스 테이블
        # "", 체크박스, 필드명, 필드값, 타입
        self.table = QTableWidget(2, 4)
        self.table.setHorizontalHeaderLabels(["필수값 여부", "필드명", "타입", "필드값"])

        data = [
            ("bbb", "value1", "String"),
            ("aaa", "value2", "String")
        ]

        for idx, (key, value, dataType) in enumerate(data):

            item = QCheckBox()
            self.table.setCellWidget(idx, 0, item)
            self.table.setItem(idx, 1, QTableWidgetItem(key))
            self.table.setItem(idx, 2, QTableWidgetItem(value))
            self.table.setItem(idx, 3, QTableWidgetItem(dataType))

        # 데이터를 다 세팅한 후 정렬 가능하게 만들어야 데이터가 날아가지 않음
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(1, Qt.AscendingOrder)

        # 결과 버튼
        self.rsltBtn = QPushButton("To markdown table!")
        self.rsltBtn.clicked.connect(self.make_result)

        self.layout.addWidget(self.srcText, 0, 0)
        self.layout.addWidget(self.table, 0, 1)
        self.layout.addWidget(self.rsltBtn, 1, 1)
        self.layout.addWidget(self.destText, 2, 1)

        self.setLayout(self.layout)

    def recturn_pressed(self):
        print(self.srcText.text())
        self.destText.setText(self.srcText.text())

    def make_result(self):

        header_str = '''| 필드명 | 타입 | 필드값 | 필수값 여부 |\n|:------|:---:|:------|:---------:|'''

        data_str = ''
        item_cnt = self.table.rowCount()

        for idx in range(item_cnt):

            required = self.table.cellWidget(idx, 0)  # 필수값 여부
            field_name = self.table.item(idx, 1).text()  # 필드명
            field_value = self.table.item(idx, 2).text()  # 필드값
            data_type = self.table.item(idx, 3).text()  # 타입

            print(required.isChecked(), field_name, field_value, data_type)

            data_str += f'''\n| {field_name} | {data_type} | {field_value} | {required.isChecked()} |'''

        print("Result ::: Markdown table -------------- ")
        print(header_str + data_str)

        self.destText.setText(header_str + data_str)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app = QApplication(sys.argv)
    root = Window()
    root.show()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
