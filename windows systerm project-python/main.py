import sys
from PySide6.QtWidgets import QApplication
from presenter.login_manager import show_login_window

if __name__ == "__main__":
    import ctypes
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QApplication(sys.argv)

    show_login_window(app) 
