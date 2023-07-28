from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from PyQt5.QtWidgets import QPushButton, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys
import json


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1300, 500)
        self.setWindowTitle("Markdown table maker")
        self.layout = QGridLayout()

        # 입력 텍스트
        self.src_text = QTextEdit()

        # 입력 버튼
        self.insert_btn = QPushButton("Put into the table")
        self.insert_btn.clicked.connect(self.parse_json)

        # 체크박스 테이블
        # "", 체크박스, 필드명, 필드값, 타입
        self.table = QTableWidget(5, 4)
        self.table.setHorizontalHeaderLabels(["필수값 여부", "필드명", "타입", "필드값"])

        self.table.setSortingEnabled(True)  # 정렬 가능

        # 결과 텍스트 생성 버튼
        self.rslt_btn = QPushButton("Make markdown table!")
        self.rslt_btn.clicked.connect(self.make_result)

        # 결과 텍스트
        self.dest_text = QTextEdit()

        # 결과 텍스트 클립보드 복사
        self.copy_btn = QPushButton('Copy!')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        # 위젯 삽입
        self.layout.addWidget(self.src_text, 0, 0)
        self.layout.addWidget(self.insert_btn, 1, 0)
        self.layout.addWidget(self.table, 0, 1)
        self.layout.addWidget(self.rslt_btn, 1, 1)
        self.layout.addWidget(self.dest_text, 2, 1)
        self.layout.addWidget(self.copy_btn, 3, 1)

        self.setLayout(self.layout)

    # def recturn_pressed(self):
    #     print(self.srcText.text())
    #     self.destText.setText(self.srcText.text())

    def parse_json(self):

        # test: String
        text = self.src_text.toPlainText()

        # convert json string to json object
        json_obj = json.loads(text)

        # 테이블 업데이트
        self.update_table(json_obj)

    def update_table(self, json_obj):

        """
        json object를 파싱하여 table에 삽입
        :param json_obj: Json 객체
        :return:
        """

        # 필드 개수 만큼 행 개수 업데이트
        row_cnt = len(json_obj.keys())
        self.table.setRowCount(row_cnt)

        # 테이블 아이템 셋
        for idx, (key, value) in enumerate(json_obj.items()):

            # 데이터 타입
            data_type = ''
            if isinstance(value, str):
                data_type = 'String'
            elif isinstance(value, int):
                data_type = 'int'
            elif isinstance(value, list):
                data_type = 'Array'
            elif isinstance(value, dict):
                data_type = 'Object'

            # [!중요] 모든 필드값을 str으로 형변환하여 테이블에 삽입해야 함
            value = str(value)

            # 체크박스
            checkbox = QCheckBox()
            if value and not value.isspace():  # 필수값 자동 체크 -빈 문자열 확인
                checkbox.setChecked(True)

            # print(idx, key, value, data_type)

            self.table.setCellWidget(idx, 0, checkbox)  # 체크박스
            self.table.setItem(idx, 1, QTableWidgetItem(key))  # 필드명
            self.table.setItem(idx, 2, QTableWidgetItem(data_type))  # 타입
            self.table.setItem(idx, 3, QTableWidgetItem(value))  # 필드값

    # end of update_table()

    def make_result(self):
        """
        테이블로부터 markdown table 문자열 생성
        :return:
        """

        # 테이블 헤더
        header_str = '''| 변수명 | 타입 | 설명 | 필수값 여부 | 비고 |\n|:------|:---:|:----|:---------:|:-----|'''

        data_str = ''
        row_cnt = self.table.rowCount()

        for idx in range(row_cnt):

            checkbox = self.table.cellWidget(idx, 0)  # 체크박스
            field_name = self.table.item(idx, 1).text()  # 필드명
            data_type = self.table.item(idx, 2).text()  # 타입
            # field_value = self.table.item(idx, 3).text()  # 필드값

            # 필수값 여부 - 체크박스 체크 여부 확인
            is_required = "Y" if checkbox.isChecked() else "N"

            # 행 생성
            data_str += f'''\n| {field_name} | {data_type} | - | {is_required} | - |'''

        # print("Result ::: Markdown table -------------- ")
        # print(header_str + data_str)

        self.dest_text.setText(header_str + data_str)

    def copy_to_clipboard(self):

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.dest_text.toPlainText(), mode=cb.Clipboard)

        # alert
        QMessageBox.about(self, "Message", "Copied!")

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
