import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QFileDialog, QGridLayout, QStackedWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon
import sys
import codecs


class Main_Page(QWidget):
    judge_file_open = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        global Path_Raw_Text
        Path_Raw_Text = "C:\\Program Files (x86)\\ETS-Lindgren\\EMQuest\\Final Data"    # "C:\\Users\\jiyoon_kim\\Desktop\\USA_Naming\\Final Data"

        btn1 = QPushButton('대상 폴더', self)

        btn1.setMaximumWidth(180)
        btn1.setMaximumHeight(60)

        btn1.setFont(QFont('Arial', 13, QFont.Bold))
        btn1.setStyleSheet("color : white;"
                           "background-color : rgb(255, 190, 11);"
                           "border-radius : 5px;"
                           )


        btn1.clicked.connect(self.getData_raw)

        btn2 = QPushButton("Run!!", self)

        btn2.setMaximumWidth(180)
        btn2.setMaximumHeight(60)

        btn2.setFont(QFont('Arial', 13, QFont.Bold))
        btn2.setStyleSheet("color : white;"
                           "background-color : rgb(255, 190, 11);"
                           "border-radius : 5px;"
                           )

        btn2.clicked.connect(self.clickMethod)
        btn2.clicked.connect(self.run)
        grid = QGridLayout()
        grid.addWidget(btn1, 1, 1)
        grid.addWidget(btn2, 1, 3)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(3, 1)
        grid.setColumnStretch(4, 1)

        self.setLayout(grid)

        self.show()

    def getData_raw(self):
        global Path_Raw
        self.judge_file_open = 1
        Path_Raw = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(Path_Raw)


    def run(self):
        if self.judge_file_open == 0:
            return 0

        num_of_check = 1000

        # 경로 지정

        raw_names = os.listdir(Path_Raw)

        text_names = os.listdir(Path_Raw_Text)[-num_of_check:]

        print(text_names)
        print(raw_names)

        # 텍스트에 있는 이름 저장
        for text in text_names:
            for config in raw_names:
                if text.replace(" .txt","") in config:
                    with codecs.open(Path_Raw_Text + "\\" + text, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        find_date = config[config.find(".")-4:config.find(".")+15]
                        if 'BHHR' in Path_Raw:
                            new_name = lines[10].strip() + ' BHHR ' + find_date + '.raw'
                        elif 'BHHL' in Path_Raw:
                            new_name = lines[10].strip() + ' BHHL ' + find_date + '.raw'
                        elif 'HR' in Path_Raw:
                            new_name = lines[10].strip() + ' HR ' + find_date + '.raw'
                        elif 'HL' in Path_Raw:
                            new_name = lines[10].strip() + ' HL ' + find_date + '.raw'
                        else:
                            new_name = lines[10].strip() + ' FS ' + find_date + '.raw'

                        os.rename(os.path.join(Path_Raw, config), os.path.join(Path_Raw, new_name))

    #-------------------------------------------------------------------------------------------------------------


    def clickMethod(self):                                                                     # 폴더 지정 안했을 때 에러 처리
        if os.path.isdir(Path_Raw_Text) == False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("에러")
            msg.setText("텍스트 파일의 경로가 잘못 되었습니다.")
            msg.setWindowTitle("Error")
            msg.exec_()
            exit()

        elif self.judge_file_open == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("에러")
            msg.setText("폴더를 선택하세요.")
            msg.setWindowTitle("Error")
            msg.exec_()

        else:
            QMessageBox.information(self,"Complete","완료되었습니다.")



class Vari_QStackedWidget(QStackedWidget):

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '종료하시겠습니까?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":


    app = QApplication(sys.argv)
    ex = Main_Page()
    widget = Vari_QStackedWidget()
    widget.addWidget(ex)

    widget.setWindowTitle("SGS Naming Auto_jiyoonkim")
    widget.setWindowIcon(QIcon("wraith.ico"))
    widget.resize(1000, 500)

    widget.show()
    sys.exit(app.exec_())