import time

from PyQt5 import QtWidgets, QtCore, QtGui


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 580)

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 430, 300))
        self.textEdit.setObjectName("textEdit")

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(30, 330, 181, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 21, 16))
        self.label.setObjectName("label")
        self.naver_id = QtWidgets.QLineEdit(self.groupBox)
        self.naver_id.setGeometry(QtCore.QRect(50, 30, 113, 20))
        self.naver_id.setObjectName("naver_id")
        self.naver_pw = QtWidgets.QLineEdit(self.groupBox)
        self.naver_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.naver_pw.setGeometry(QtCore.QRect(50, 65, 113, 20))
        self.naver_pw.setObjectName("naver_pw")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 65, 31, 16))
        self.label_2.setObjectName("label_2")

        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(240, 330, 181, 101))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")

        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 21, 16))
        self.label_5.setObjectName("label_5")
        self.pin_id = QtWidgets.QLineEdit(self.groupBox_2)
        self.pin_id.setGeometry(QtCore.QRect(50, 30, 113, 20))
        self.pin_id.setObjectName("brunch_id")
        self.pin_pw = QtWidgets.QLineEdit(self.groupBox_2)
        self.pin_pw.setGeometry(QtCore.QRect(50, 65, 113, 20))
        self.pin_pw.setObjectName("brunch_pw")
        self.pin_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(20, 65, 31, 16))
        self.label_6.setObjectName("label_6")

        # 네이버 로그인 btn
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 440, 181, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.naver_start)

        # 브랜치 로그인 시작 btn
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 480, 181, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.post_start)

        # 포스트 시작 btn
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 520, 181, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.post_start)

        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(250, 445, 181, 16))

        self.checkBox2 = QtWidgets.QCheckBox(Form)
        self.checkBox2.setGeometry(QtCore.QRect(250, 470, 181, 16))

        self.checkBox3 = QtWidgets.QCheckBox(Form)
        self.checkBox3.setGeometry(QtCore.QRect(250, 495, 181, 16))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "네이버&브런치 포스팅"))

        self.groupBox.setTitle(_translate("Form", "네이버"))
        self.groupBox_2.setTitle(_translate("Form", "브런치"))

        self.label.setText(_translate("Form", "ID"))
        self.label_2.setText(_translate("Form", "PW"))
        self.label_5.setText(_translate("Form", "ID"))
        self.label_6.setText(_translate("Form", "PW"))
        self.pushButton.setText(_translate("Form", "네이버 로그인"))
        self.pushButton_2.setText(_translate("Form", "브런치 로그인"))
        self.pushButton_3.setText(_translate("Form", "포스트 시작"))
        self.checkBox.setText(_translate("Form", "네이버 블로그"))
        self.checkBox2.setText(_translate("Form", "네이버 포스트"))
        self.checkBox3.setText(_translate("Form", "브런치"))


    def naver_start(self):
        # naverPost = NaverPost(self.naver_id.text(), self.naver_pw.text())
        print(f"입력내용 {self.naver_id.text()} pw: {self.naver_pw.text()}")
        urls = [i for i in self.textEdit.toPlainText().split("\n") if "http" in i]
        # naverPost.blog(urls)

    def post_start(self):
        # naverPost = NaverPost(self.naver_id.text(), self.naver_pw.text())
        urls = [i for i in self.textEdit.toPlainText().split("\n") if "http" in i]
        # naverPost.post(urls)

    def pin_start(self):
        # pinterPost = PinterPost(self.pin_id.text(), self.pin_pw.text())
        urls = [i for i in self.textEdit.toPlainText().split("\n") if "http" in i]
        # pinterPost.pinterest(urls)

    def start(self):
        # naverPost = NaverPost(self.naver_id.text(), self.naver_pw.text())
        # pinterPost = PinterPost(self.pin_id.text(), self.pin_pw.text())
        print("start")
