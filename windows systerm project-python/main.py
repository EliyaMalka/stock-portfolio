import sys
from PySide6.QtWidgets import QApplication
from presenter.login_manager import show_login_window

if __name__ == "__main__":
    app = QApplication(sys.argv)

    show_login_window(app) 
