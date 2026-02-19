# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QRect, QCoreApplication, QMetaObject
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit,
                               QPushButton, QTabWidget, QMenuBar, QStatusBar,QLabel)

import view.resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        # Set fixed size
        MainWindow.resize(1000, 650)
        MainWindow.setFixedSize(1000, 650)

        # רקע עם תמונה מתוך ה-resources
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setFixedSize(1000, 650)
        MainWindow.setFixedSize(1000, 650)
        self.bg_label = QLabel(self.centralwidget)
        self.bg_label.setPixmap(QPixmap(":/icons/images/loginBG.jpg"))
        self.bg_label.setGeometry(0, 0, 1000, 650)
        self.bg_label.lower() 




        # Tab Widget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(330, 100, 600, 450))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.tabBar().setExpanding(True)

        # --------------------- Login Tab ---------------------
        self.loginTab = QWidget()
        self.loginTab.setObjectName("loginTab")
        self.loginLayout = QVBoxLayout(self.loginTab)
        self.loginLayout.setContentsMargins(40, 40, 40, 40)
        self.loginLayout.setSpacing(20)
        self.loginLayout.setAlignment(Qt.AlignCenter)


        # Username
        self.userName = QLineEdit(self.loginTab)
        self.userName.setObjectName("userName")
        self.userName.setPlaceholderText("Username")
        self.loginLayout.addWidget(self.userName)

        # Password
        self.password = QLineEdit(self.loginTab)
        self.password.setObjectName("password")
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.loginLayout.addWidget(self.password)

        # Error message
        self.wrongDetails = QLabel(self.loginTab)
        self.wrongDetails.setObjectName("wrongDetails")
        self.wrongDetails.setText("")  # התחל עם טקסט ריק
        self.wrongDetails.setAlignment(Qt.AlignCenter)
        self.wrongDetails.setStyleSheet("color: red; background: transparent;")
        self.wrongDetails.setFixedHeight(20)  # גובה קבוע כדי למנוע שינוי בפריסה
        self.loginLayout.addWidget(self.wrongDetails)


        # Login Button
        self.login = QPushButton("Login", self.loginTab)
        self.login.setObjectName("login")
        self.login.setMaximumWidth(120)
        self.loginLayout.addWidget(self.login, alignment=Qt.AlignCenter)

        self.tabWidget.addTab(self.loginTab, "Login")

        # --------------------- Signup Tab ---------------------
        self.signupTab = QWidget()
        self.signupTab.setObjectName("signupTab")
        self.signupLayout = QVBoxLayout(self.signupTab)
        self.signupLayout.setContentsMargins(40, 40, 40, 40)
        self.signupLayout.setSpacing(20)
        self.signupLayout.setAlignment(Qt.AlignCenter)


        self.signupUsername = QLineEdit(self.signupTab)
        self.signupUsername.setObjectName("signupUsername")
        self.signupUsername.setPlaceholderText("Username")
        self.signupLayout.addWidget(self.signupUsername)

        self.signupEmail = QLineEdit(self.signupTab)
        self.signupEmail.setObjectName("signupEmail")
        self.signupEmail.setPlaceholderText("Email")
        self.signupLayout.addWidget(self.signupEmail)

        self.signupPassword = QLineEdit(self.signupTab)
        self.signupPassword.setObjectName("signupPassword")
        self.signupPassword.setPlaceholderText("Password")
        self.signupPassword.setEchoMode(QLineEdit.Password)
        self.signupLayout.addWidget(self.signupPassword)

        self.signupConfirmPassword = QLineEdit(self.signupTab)
        self.signupConfirmPassword.setObjectName("signupConfirmPassword")
        self.signupConfirmPassword.setPlaceholderText("Confirm Password")
        self.signupConfirmPassword.setEchoMode(QLineEdit.Password)
        self.signupLayout.addWidget(self.signupConfirmPassword)

        self.signup = QPushButton("Sign Up", self.signupTab)
        self.signup.setObjectName("signup")
        self.signup.setMaximumWidth(120)
        self.signupLayout.addWidget(self.signup, alignment=Qt.AlignCenter)

        self.tabWidget.addTab(self.signupTab, "Sign Up")
        

        # Finalize main window
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1000, 20))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "Login / SignUp", None))
        MainWindow.setWindowIcon(QIcon(":/icons/icons/LogoGreen.png"))


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
