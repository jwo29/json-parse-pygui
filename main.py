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
        # self.layout.setColumnStretch(0, 2)

        # 입력 텍스트
        self.src_text = QTextEdit()
        self.src_text.setPlaceholderText("Enter here")

        # 입력 버튼
        self.insert_btn = QPushButton("Put into the table")
        self.insert_btn.clicked.connect(self.parse_json)

        # 필드 정의표
        self.field_table = QTableWidget(5, 2)
        self.field_table.setHorizontalHeaderLabels(["필드명", "설명"])

        with open('./test.json', 'r', encoding='utf-8') as file:
            self.field_define = json.loads(file.read())
            # print(type(field_define))
            # print(field_define)

        # 필드 정의표 행 개수 재설정
        self.field_table.setRowCount(len(self.field_define.keys()))

        # 필드명/설명 아이템 셋
        for idx, (key, value) in enumerate(self.field_define.items()):
            # print(idx, key, value)
            self.field_table.setItem(idx, 0, QTableWidgetItem(key))  # 필드명
            self.field_table.setItem(idx, 1, QTableWidgetItem(str(value)))  # 필드 설명

        self.field_table.setSortingEnabled(True)  # 정렬 가능

        # 체크박스 테이블
        # "", 체크박스, 필드명, 필드값, 타입
        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["필수값 여부", "필드명", "설명", "타입", "필드값"])
        # self.table.cellChanged.connect(self.update_field_table)

        # 결과 텍스트 생성 버튼
        self.rslt_btn = QPushButton("Make markdown table!")
        self.rslt_btn.clicked.connect(self.make_result)

        self.rslt_option = QCheckBox("Only required")

        # 결과 텍스트
        self.dest_text = QTextEdit()
        self.dest_text.setPlaceholderText("Result markdown table(Read-Only)")
        self.dest_text.setReadOnly(True)

        # 결과 텍스트 클립보드 복사
        self.copy_btn = QPushButton('Copy!')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

        # 위젯 삽입
        self.layout.addWidget(self.src_text, 0, 0)
        self.layout.addWidget(self.insert_btn, 1, 0)
        self.layout.addWidget(self.field_table, 2, 0)
        self.layout.addWidget(self.table, 0, 1)
        self.layout.addWidget(self.rslt_btn, 1, 1)
        self.layout.addWidget(self.rslt_option, 1, 2)
        self.layout.addWidget(self.dest_text, 2, 1)
        self.layout.addWidget(self.copy_btn, 3, 1)

        self.setLayout(self.layout)

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

        self.table.setSortingEnabled(False)

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

            try:
                self.table.setItem(idx, 2, QTableWidgetItem(self.field_define[key]))  # 필드 설명
            except KeyError:
                self.table.setItem(idx, 2, QTableWidgetItem("-"))

            self.table.setItem(idx, 3, QTableWidgetItem(data_type))  # 타입
            self.table.setItem(idx, 4, QTableWidgetItem(value))  # 필드값

        self.table.setSortingEnabled(True)  # 정렬 가능

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

        # indexs = [*map(lambda x: x if self.table.cellWidget(x, 0).isChecked() else -1, self.table.)]

        # print(indexs)

        for idx in range(row_cnt):

            checkbox = self.table.cellWidget(idx, 0)  # 체크박스
            field_name = self.table.item(idx, 1).text()  # 필드명
            field_desc = self.table.item(idx, 2).text()  # 필드 설명
            data_type = self.table.item(idx, 3).text()  # 타입
            # field_value = self.table.item(idx, 4).text()  # 필드값

            # 필수값 여부 - 체크박스 체크 여부 확인
            is_required = "Y" if checkbox.isChecked() else "N"

            if self.rslt_option.isChecked() and is_required == "N":
                continue

            # 행 생성
            data_str += f'''\n| {field_name} | {data_type} | {field_desc} | {is_required} | - |'''

        self.dest_text.setText(header_str + data_str)

    def copy_to_clipboard(self):

        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.dest_text.toPlainText(), mode=cb.Clipboard)

        # alert
        QMessageBox.about(self, "Message", "Copied!")

    # 이벤트 핸들러
    def update_field_table(self, row, col):

        # 설명 필드 외에는 수정할 수 없도록 조건 필요

        self.field_table.setSortingEnabled(False)

        changed_cell = self.table.item(row, col)  # 수정된 필드 설명
        field_name = self.table.item(row, 1)  # 필드명

        # 새로운 행이 삽입될 위치
        row_pos = self.field_table.rowCount()

        self.field_table.insertRow(row_pos)
        self.field_table.setItem(row_pos, 0, QTableWidgetItem(field_name))  # 필드명
        self.field_table.setItem(row_pos, 1, QTableWidgetItem(changed_cell.text()))  # 필드 설명

        self.field_table.setSortingEnabled(True)

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
