"""
מנהל/מציג (Presenter) של חלון ההתחברות.

מטפל בלוגיקת ממשק המשתמש של ההתחברות, מאמת הרשאות מול ה-API של FastAPI,
ומנהל את המעבר מחלון ההתחברות לחלון היישום הראשי.
"""
import hashlib  # For hashing the password for comparison
import requests
from PySide6.QtWidgets import QMainWindow, QMessageBox
from view.login import Ui_MainWindow
from presenter.main_presenter import MainWindow
import model.user


def hash_password(password):
    """מגבב את הסיסמה כדי שתתאים לפורמט ה-hashedPassword ב-API."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username, password):
    """
    מאמת את המשתמש על ידי שליחת בקשת POST לנקודת הקצה של התחברות בשרת.
    אם מצליח, שומר את מזהה המשתמש ושם המשתמש באופן מקומי.
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
    מחלקת ממשק המשתמש הראשית של חלון ההתחברות.
    מטפלת בקלט משתמש, סגנונות (styles) וחיבורי כפתורים.
    """
    def __init__(self, app):
        """מאתחל את רכיבי ממשק המשתמש ומחבר את האות (signal) של כפתור ההתחברות."""
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
        פונקציית חריץ (Slot) המופעלת בלחיצה על כפתור ההתחברות.
        מאמתת הרשאות ומנהלת מעבר חלונות במקרה של הצלחה,
        או מציגה הודעת שגיאה במקרה של כישלון.
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
        """מאתחל ומציג את חלון היישום הראשי, תוך החלת גיליון הסגנונות (stylesheet) הספציפי שלו תחילה."""
        from PySide6.QtWidgets import QApplication

        # טעינת קובץ העיצוב
        with open(r'view\mainWindowStyle.qss', 'r', encoding='utf-8') as style_file:
            self.app.setStyleSheet(style_file.read())

        self.main_window = MainWindow()
        self.main_window.show()


def show_login_window(app):
    """פונקציית עזר ליצירת מופע והצגת חלון ההתחברות, ולאחר מכן התחלת לולאת האירועים של Qt."""
    login_window = LoginWindow(app)
    login_window.show()
    app.exec()

