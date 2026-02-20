"""
נקודת הכניסה הראשית של אפליקציית ניהול תיק מניות ל-Windows.

סקריפט זה מאתחל את אפליקציית ה-Qt ומפעיל את התצוגה הראשונית
(חלון ההתחברות). הוא גם מגדיר תצורות ספציפיות ל-Windows
עבור רינדור סמל בשורת המשימות.
"""
import sys
from PySide6.QtWidgets import QApplication
from presenter.login_manager import show_login_window

if __name__ == "__main__":
    import ctypes
    # Ensures the custom app icon displays correctly in the Windows taskbar 
    # instead of the default Python icon.
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)

    show_login_window(app) 
