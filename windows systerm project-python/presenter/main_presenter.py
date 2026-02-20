"""
מנהל/מציג (Presenter) של החלון הראשי.

מטפל בלוגיקה עבור חלון השתמש הראשי לאחר התחברות מוצלחת.
מנהל את הניווט בסרגל הצד ומעבר בין תצוגות (עמודים) שונות
בתוך ה-stacked widget.
"""
from PySide6.QtWidgets import QMainWindow
from view.sidebar import Ui_MainWindow  # טעינת ממשק ה-UI

class MainWindow(QMainWindow):
    """
    מחלקת Presenter עבור חלון היישום הראשי.
    מחברת את כפתורי סרגל הצד לעמודים התואמים ב-stacked widget.
    """
    def __init__(self):
        """מאתחל את ממשק המשתמש, מסתיר סמלי ברירת מחדל ומחבר את כפתורי הניווט."""
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
        פונקציה כללית להחלפת העמוד הפעיל ב-stacked widget
        והדפסת הודעת ניפוי שגיאות (debug) לקונסולה.
        """
        print(message)
        self.ui.stackedWidget.setCurrentIndex(index)

