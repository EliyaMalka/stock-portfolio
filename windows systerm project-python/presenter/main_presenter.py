"""
Main Window Presenter.

Handles the logic for the main application window after a successful login.
Manages the sidebar navigation and switching between different views (pages) 
within the stacked widget.
"""
from PySide6.QtWidgets import QMainWindow
from view.sidebar import Ui_MainWindow  # טעינת ממשק ה-UI

class MainWindow(QMainWindow):
    """
    Presenter class for the main application window.
    Connects the sidebar buttons to the corresponding pages in the stacked widget.
    """
    def __init__(self):
        """Initializes the UI, hides default icons, and connects navigation buttons."""
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # Connect sidebar button toggles to page change functions
        self.ui.home_btn_1.toggled.connect(lambda: self.change_page(0, "home1 toggled"))
        self.ui.home_btn_2.toggled.connect(lambda: self.change_page(0, "home2 toggled"))
        self.ui.dashboard_btn_1.toggled.connect(lambda: self.change_page(1, "dashboard1 toggled"))
        self.ui.dashboard_btn_2.toggled.connect(lambda: self.change_page(1, "dashboard2 toggled"))
        self.ui.order_btn_1.toggled.connect(lambda: self.change_page(2, "orders1 toggled"))
        self.ui.order_btn_2.toggled.connect(lambda: self.change_page(2, "orders2 toggled"))
        self.ui.customer_btn_1.toggled.connect(lambda: self.change_page(3, "customers1 toggled"))
        self.ui.customer_btn_2.toggled.connect(lambda: self.change_page(3, "customers2 toggled"))

    def change_page(self, index, message):
        """
        General function to switch the active page in the stacked widget
        and print a debug message to the console.
        """
        print(message)
        self.ui.stackedWidget.setCurrentIndex(index)

