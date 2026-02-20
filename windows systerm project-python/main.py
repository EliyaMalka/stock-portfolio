"""
Main Entry Point for the Windows Stock Portfolio Application.

This script initializes the Qt Application and launches the initial view
(the Login Window). It also sets up Windows-specific configurations 
for taskbar icon rendering.
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
