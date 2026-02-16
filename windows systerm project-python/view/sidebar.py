# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'mainWindow.ui'
##
# Created by: Qt User Interface Compiler version 6.8.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                               QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
                               QStackedWidget, QVBoxLayout, QWidget)


import view.resource_rc as resource_rc

from view.StockGraph import StockGraph 
from view.TransactionsWindow import TransactionsWindow  
from view.userDetails import UserDetailsWindow
from view.chatWindow import ChatWindow
import model.user

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 650)
        MainWindow.setFixedSize(1000, 650)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.full_menu_widget = QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName(u"full_menu_widget")
        self.verticalLayout_4 = QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 5, 8, 10)
        self.logo_label_2 = QLabel(self.full_menu_widget)
        self.logo_label_2.setObjectName(u"logo_label_2")
        self.logo_label_2.setMinimumSize(QSize(40, 40))
        self.logo_label_2.setMaximumSize(QSize(40, 40))
        self.logo_label_2.setPixmap(QPixmap(u":/icons/icons/LogoGreen.png"))

        self.horizontalLayout.addWidget(self.logo_label_2)

        self.logo_label_3 = QLabel(self.full_menu_widget)
        self.logo_label_3.setObjectName(u"logo_label_3")
        font = QFont()
        font.setPointSize(15)
        self.logo_label_3.setFont(font)

        self.horizontalLayout.addWidget(self.logo_label_3)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.home_btn_2 = QPushButton(self.full_menu_widget)
        self.home_btn_2.setObjectName(u"home_btn_2")
        font1 = QFont()
        font1.setPointSize(12)
        self.home_btn_2.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/icons/icons/home-4-32.ico", QSize(),
                     QIcon.Mode.Normal, QIcon.State.Off)
        icon.addFile(u":/icons/icons/home-4-48.ico", QSize(),
                     QIcon.Mode.Normal, QIcon.State.On)
        self.home_btn_2.setIcon(icon)
        self.home_btn_2.setIconSize(QSize(14, 14))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.home_btn_2)

        self.dashboard_btn_2 = QPushButton(self.full_menu_widget)
        self.dashboard_btn_2.setObjectName(u"dashboard_btn_2")
        self.dashboard_btn_2.setFont(font1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/dashboard-5-32.ico",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon1.addFile(u":/icons/icons/dashboard-5-48.ico",
                      QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.dashboard_btn_2.setIcon(icon1)
        self.dashboard_btn_2.setIconSize(QSize(14, 14))
        self.dashboard_btn_2.setCheckable(True)
        self.dashboard_btn_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.dashboard_btn_2)

        self.order_btn_2 = QPushButton(self.full_menu_widget)
        self.order_btn_2.setObjectName(u"order_btn_2")
        self.order_btn_2.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/product-32.ico", QSize(),
                      QIcon.Mode.Normal, QIcon.State.Off)
        icon2.addFile(u":/icons/icons/product-48.ico", QSize(),
                      QIcon.Mode.Normal, QIcon.State.On)
        self.order_btn_2.setIcon(icon2)
        self.order_btn_2.setIconSize(QSize(14, 14))
        self.order_btn_2.setCheckable(True)
        self.order_btn_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.order_btn_2)

        self.customer_btn_2 = QPushButton(self.full_menu_widget)
        self.customer_btn_2.setObjectName(u"customer_btn_2")
        self.customer_btn_2.setFont(font1)
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/activity-feed-32.ico",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon3.addFile(u":/icons/icons/activity-feed-48.ico",
                      QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.customer_btn_2.setIcon(icon3)
        self.customer_btn_2.setIconSize(QSize(14, 14))
        self.customer_btn_2.setCheckable(True)
        self.customer_btn_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.customer_btn_2)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(
            20, 98, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.exit_butt_2 = QPushButton(self.full_menu_widget)
        self.exit_butt_2.setObjectName(u"exit_butt_2")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/close-window-64.ico",
                      QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exit_butt_2.setIcon(icon4)
        self.exit_butt_2.setIconSize(QSize(14, 14))
        self.exit_butt_2.setCheckable(True)
        self.exit_butt_2.setAutoExclusive(True)

        self.verticalLayout_4.addWidget(self.exit_butt_2)

        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_5 = QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.menu = QPushButton(self.widget_3)
        self.menu.setObjectName(u"menu")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/menu-4-32.ico", QSize(),
                      QIcon.Mode.Normal, QIcon.State.Off)
        self.menu.setIcon(icon5)
        self.menu.setIconSize(QSize(14, 14))
        self.menu.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.menu)

        self.horizontalSpacer = QSpacerItem(
            488, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.stackedWidget = QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")


        # Add StockGraph to the home page
        self.stock_graph = StockGraph()  # Create an instance of StockGraph
        self.home_layout = QVBoxLayout(self.page)  # Create a layout for the home page
        self.home_layout.addWidget(self.stock_graph)  # Add the StockGraph widget to the layout
        self.page.setLayout(self.home_layout)  # Set the layout for the home page


        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(210, 150, 71, 41))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")

        # Add TransactionsWindow to the dashboard page
        self.transactions_window = TransactionsWindow()  # צור מופע של TransactionsWindow
        self.dashboard_layout = QVBoxLayout(self.page_2)  # צור layout לעמוד dashboard
        self.dashboard_layout.addWidget(self.transactions_window)  # הוסף את TransactionsWindow ל-layout
        self.page_2.setLayout(self.dashboard_layout)  # הגדר את ה-layout לעמוד dashboard

        self.stackedWidget.addWidget(self.page_2) 



        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(160, 130, 191, 71))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_6 = QLabel(self.page_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(210, 140, 111, 91))

        # Add ChatWindow to the page_3
        self.chat_window = ChatWindow()  # Create an instance of ChatWindow
        self.customers_layout = QVBoxLayout(self.page_3)  
        self.customers_layout.addWidget(self.chat_window)  # Add the ChatWindow widget to the layout
        self.page_3.setLayout(self.customers_layout)  

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")

        
        # Add UserDetailsWindow to the last page (page_4)
        self.user_details_window = UserDetailsWindow(model.user.load_user_id(), "http://localhost:8000/api/v1/users")  # Create an instance of UserDetailsWindow
        self.customers_layout = QVBoxLayout(self.page_4)  # Create a layout for the last page
        self.customers_layout.addWidget(self.user_details_window)  # Add the UserDetailsWindow widget to the layout
        self.page_4.setLayout(self.customers_layout)  # Set the layout for the last page


        self.label_7 = QLabel(self.page_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(200, 150, 39, 11))
        self.stackedWidget.addWidget(self.page_4)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)

        self.icon_only_widget = QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName(u"icon_only_widget")
        self.verticalLayout_3 = QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.logo_label_1 = QLabel(self.icon_only_widget)
        self.logo_label_1.setObjectName(u"logo_label_1")
        self.logo_label_1.setMinimumSize(QSize(50, 50))
        self.logo_label_1.setMaximumSize(QSize(50, 50))
        self.logo_label_1.setPixmap(QPixmap(u":/icons/icons/LogoWhite.png"))

        self.horizontalLayout_2.addWidget(self.logo_label_1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.home_btn_1 = QPushButton(self.icon_only_widget)
        self.home_btn_1.setObjectName(u"home_btn_1")
        self.home_btn_1.setIcon(icon)
        self.home_btn_1.setIconSize(QSize(20, 20))
        self.home_btn_1.setCheckable(True)
        self.home_btn_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.home_btn_1)

        self.dashboard_btn_1 = QPushButton(self.icon_only_widget)
        self.dashboard_btn_1.setObjectName(u"dashboard_btn_1")
        self.dashboard_btn_1.setIcon(icon1)
        self.dashboard_btn_1.setIconSize(QSize(20, 20))
        self.dashboard_btn_1.setCheckable(True)
        self.dashboard_btn_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.dashboard_btn_1)

        self.order_btn_1 = QPushButton(self.icon_only_widget)
        self.order_btn_1.setObjectName(u"order_btn_1")
        self.order_btn_1.setIcon(icon2)
        self.order_btn_1.setIconSize(QSize(20, 20))
        self.order_btn_1.setCheckable(True)
        self.order_btn_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.order_btn_1)

        self.customer_btn_1 = QPushButton(self.icon_only_widget)
        self.customer_btn_1.setObjectName(u"customer_btn_1")
        self.customer_btn_1.setIcon(icon3)
        self.customer_btn_1.setIconSize(QSize(20, 20))
        self.customer_btn_1.setCheckable(True)
        self.customer_btn_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.customer_btn_1)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(
            20, 353, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.exit_butt_1 = QPushButton(self.icon_only_widget)
        self.exit_butt_1.setObjectName(u"exit_butt_1")
        self.exit_butt_1.setIcon(icon4)
        self.exit_butt_1.setIconSize(QSize(20, 20))
        self.exit_butt_1.setCheckable(True)
        self.exit_butt_1.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.exit_butt_1)

        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.menu.toggled.connect(self.icon_only_widget.setVisible)
        self.menu.toggled.connect(self.full_menu_widget.setHidden)
        self.home_btn_1.toggled.connect(self.home_btn_2.setChecked)
        self.dashboard_btn_1.toggled.connect(self.dashboard_btn_2.setChecked)
        self.order_btn_1.toggled.connect(self.order_btn_2.setChecked)
        self.customer_btn_1.toggled.connect(self.customer_btn_2.setChecked)
        self.home_btn_2.toggled.connect(self.home_btn_1.setChecked)
        self.dashboard_btn_2.toggled.connect(self.dashboard_btn_1.setChecked)
        self.order_btn_2.toggled.connect(self.order_btn_1.setChecked)
        self.customer_btn_2.toggled.connect(self.customer_btn_1.setChecked)
        self.customer_btn_2.toggled.connect(self.update_user_details_window)
        
        self.exit_butt_2.clicked.connect(MainWindow.close)
        self.exit_butt_1.clicked.connect(MainWindow.close)

        self.stackedWidget.setCurrentIndex(3)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.logo_label_2.setText("")
        self.logo_label_3.setText(QCoreApplication.translate(
            "MainWindow", u"StockWise", None))
        self.home_btn_2.setText(
            QCoreApplication.translate("MainWindow", u"Home", None))
        self.dashboard_btn_2.setText(
            QCoreApplication.translate("MainWindow", u"Transactions", None))
        self.order_btn_2.setText(
            QCoreApplication.translate("MainWindow", u"AI Chat", None))
        self.customer_btn_2.setText(
            QCoreApplication.translate("MainWindow", u"User", None))
        self.exit_butt_2.setText(
            QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menu.setText("")
        
        self.logo_label_1.setText("")
        self.home_btn_1.setText("")
        self.dashboard_btn_1.setText("")
        self.order_btn_1.setText("")
        self.customer_btn_1.setText("")
        self.exit_butt_1.setText("")
    # retranslateUi

    def update_user_details_window(self):
        """Update the user details window when navigating to the last page."""
        if self.customer_btn_2.isChecked():  # בדוק אם הכפתור נלחץ
            self.user_details_window.load_user_details()  # טען מחדש את פרטי המשתמש
            self.stackedWidget.setCurrentIndex(self.stackedWidget.indexOf(self.page_4))  # עבור לדף האחרון
