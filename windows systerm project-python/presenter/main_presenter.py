from PySide6.QtWidgets import QMainWindow
from view.sidebar import Ui_MainWindow  # טעינת ממשק ה-UI

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # חיבור האותות לפונקציות
        self.ui.home_btn_1.toggled.connect(lambda: self.change_page(0, "home1 toggled"))
        self.ui.home_btn_2.toggled.connect(lambda: self.change_page(0, "home2 toggled"))
        self.ui.dashboard_btn_1.toggled.connect(lambda: self.change_page(1, "dashboard1 toggled"))
        self.ui.dashboard_btn_2.toggled.connect(lambda: self.change_page(1, "dashboard2 toggled"))
        self.ui.order_btn_1.toggled.connect(lambda: self.change_page(2, "orders1 toggled"))
        self.ui.order_btn_2.toggled.connect(lambda: self.change_page(2, "orders2 toggled"))
        self.ui.customer_btn_1.toggled.connect(lambda: self.change_page(3, "customers1 toggled"))
        self.ui.customer_btn_2.toggled.connect(lambda: self.change_page(3, "customers2 toggled"))

    def change_page(self, index, message):
        """ פונקציה כללית לשינוי עמוד והדפסה למסוף """
        print(message)
        self.ui.stackedWidget.setCurrentIndex(index)
