"""
Login Presenter / Manager.

Handles the login UI logic, authenticates credentials against the FastAPI backend,
and manages the transition from the login window to the main application window.
"""
import hashlib  # For hashing the password for comparison
import requests
from PySide6.QtWidgets import QMainWindow, QMessageBox
from view.login import Ui_MainWindow
from presenter.main_presenter import MainWindow
import model.user


def hash_password(password):
    """Hash the password to match the hashedPassword format in the API."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username, password):
    """
    Authenticates the user by sending a POST request to the backend login endpoint.
    If successful, saves the user ID and username locally.
    """
    try:
        # Prepare the login payload
        payload = {
            "Username": username,
            "Password": password
        }

        # Make a POST request to the login endpoint
        response = requests.post('http://localhost:8000/api/v1/login', json=payload)
        
        if response.status_code == 200:
            user_data = response.json()
            # Save user data locally
            model.user.save_username(username)
            model.user.save_user_id(user_data['UserID'])
            return True
        elif response.status_code == 401:
            print("Login failed: Invalid credentials")
            return False
        else:
            print(f"Login failed with status: {response.status_code}")
            print(response.text)
            return False

    except requests.RequestException as e:
        print(f"Error while checking credentials: {e}")
        return False


class LoginWindow(QMainWindow):
    """
    The main login GUI class.
    Handles user input, styles, and button connections.
    """
    def __init__(self, app):
        """Initializes the UI components and connects the login button signal."""
        super().__init__()
        self.app = app  # שמירת QApplication לניהול נכון של האירועים
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # חיבור כפתור ההתחברות
        self.ui.login.clicked.connect(self.handle_login)

        # Apply the login window stylesheet
        self.apply_stylesheet()

    def apply_stylesheet(self):
        # טעינת קובץ העיצוב
        with open(r'view\loginWindowStyle.qss', 'r', encoding='utf-8') as style_file:
            self.setStyleSheet(style_file.read())

    def handle_login(self):
        """
        Slot function triggered when the login button is clicked.
        Validates credentials and manages window transition on success, 
        or shows an error message on failure.
        """
        username = self.ui.userName.text()
        password = self.ui.password.text()

        if check_credentials(username, password):
            # Hide the error message if login is successful
            self.ui.wrongDetails.setVisible(False)
            self.close()  # סגירת חלון ההתחברות
            self.show_main_window()  # פתיחת החלון הראשי
        else:
            self.ui.wrongDetails.setText("Incorrect username or password!")
            self.ui.wrongDetails.setVisible(True)  # Show the error message

    def show_main_window(self):
        """Initializes and displays the main application window, applying its specific stylesheet first."""
        from PySide6.QtWidgets import QApplication

        # טעינת קובץ העיצוב
        with open(r'view\mainWindowStyle.qss', 'r', encoding='utf-8') as style_file:
            self.app.setStyleSheet(style_file.read())

        self.main_window = MainWindow()
        self.main_window.show()


def show_login_window(app):
    """Helper function to instantiate and show the login window, then start the Qt event loop."""
    login_window = LoginWindow(app)
    login_window.show()
    app.exec()

