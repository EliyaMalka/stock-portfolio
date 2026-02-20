"""
רכיב תצוגת עסקאות.

אחראי על הצגת היסטוריית העסקאות של המשתמש בטבלה,
ומספק ממשקים (כרטיסיות) לביצוע פקודות קנייה ומכירה חדשות.
מקיים אינטראקציה ישירה עם ה-API של FastAPI לשליפת מגבלות והגשת פקודות.
"""
import sys
import os
import requests
import yfinance as yf
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QComboBox, QSpinBox, QFormLayout,
    QMessageBox, QTabWidget, QSizePolicy ,QHeaderView
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt, QDateTime, QFile, QTextStream
from model.user import load_user_id

API_URL = "http://localhost:8000/api/v1"
STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "TSMC", "ARM", "SSNLF", "NVDA", "ASML", "META"]

# --- Fix for timezone cache (critical for Windows users with non-ASCII names) ---
cache_dir = os.path.join(os.getcwd(), "py_cache")
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
try:
    yf.set_tz_cache_location(cache_dir)
except:
    pass


class TransactionsWindow(QWidget):
    """
    הווידג'ט הראשי עבור כרטיסיית העסקאות (Transactions).
    מכיל את כרטיסיות הקנייה/מכירה ואת טבלת היסטוריית העסקאות.
    """
    def __init__(self):
        """מאתחל את ממשק המשתמש, מחיל עיצוב, וטוען נתונים ראשוניים."""
        super().__init__()
        self.setWindowTitle("User Transactions")
        self.setGeometry(100, 0, 700, 500)

        self.apply_stylesheet()

        layout = QVBoxLayout()
        
        self.current_buy_price = 0
        self.current_sell_price = 0

        self.tabs = QTabWidget()
        self.buy_tab = QWidget()
        self.sell_tab = QWidget()
        self.buy_tab.setObjectName("buyTab")  # Unique name for Buy Stock tab
        self.sell_tab.setObjectName("sellTab")  # Unique name for Sell Stock tab
        self.tabs.addTab(self.buy_tab, "Buy Stock")
        self.tabs.addTab(self.sell_tab, "Sell Stock")

        self.setup_buy_tab()
        self.setup_sell_tab()
        layout.addWidget(self.tabs)

        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)  # Disable row numbers
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Size adjustment
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fit
        layout.addWidget(self.table)
        layout.setStretch(1, 1)  # Set Stretch for the table

        self.setLayout(layout)

        self.load_transactions()
        self.update_price("buy")
        self.update_price("sell")


    def apply_stylesheet(self):
        """טוען ומחיל עיצוב QSS עבור חלון העסקאות."""
        file = QFile(r"view\TransactionsWindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()

    def setup_buy_tab(self):
        """מגדיר את הפריסה והקלטים עבור כרטיסיית 'קניית מניות' (Buy Stock)."""
        layout = QFormLayout()
        self.buy_stock_symbol = QComboBox()
        self.buy_stock_symbol.addItems(STOCK_SYMBOLS)
        self.buy_stock_symbol.currentTextChanged.connect(lambda: self.update_price("buy"))
        layout.addRow("Stock Symbol:", self.buy_stock_symbol)

        self.buy_quantity = QSpinBox()
        self.buy_quantity.setRange(1, 1000)
        layout.addRow("Quantity:", self.buy_quantity)

        self.buy_price_label = QLabel("Price: Fetching...")
        layout.addRow("Price Per Stock:", self.buy_price_label)

        self.buy_button = QPushButton("Buy Stock")
        self.buy_button.setStyleSheet("""
        QPushButton {
            background-color: #6fb574;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #5fa064;
        }
        QPushButton:pressed {
            background-color: #4d8c55;
        }
    """)

        self.buy_button.clicked.connect(self.buy_stock)
        layout.addWidget(self.buy_button)

        self.buy_tab.setLayout(layout)

    def setup_sell_tab(self):
        """מגדיר את הפריסה והקלטים עבור כרטיסיית 'מכירת מניות' (Sell Stock)."""
        layout = QFormLayout()
        self.sell_stock_symbol = QComboBox()
        self.sell_stock_symbol.addItems(STOCK_SYMBOLS)
        self.sell_stock_symbol.currentTextChanged.connect(lambda: self.update_price("sell"))
        layout.addRow("Stock Symbol:", self.sell_stock_symbol)

        self.sell_quantity = QSpinBox()
        self.sell_quantity.setRange(1, 1000)
        layout.addRow("Quantity:", self.sell_quantity)

        self.sell_price_label = QLabel("Price: Fetching...")
        layout.addRow("Price Per Stock:", self.sell_price_label)

        self.sell_button = QPushButton("Sell Stock")
        self.sell_button.setStyleSheet("""
            QPushButton {
                background-color: #be2e44;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a12839;
            }
            QPushButton:pressed {
                background-color: #8a1f2f;
            }
        """)
        self.sell_button.clicked.connect(self.sell_stock)
        layout.addWidget(self.sell_button)

        self.sell_tab.setLayout(layout)

    def load_transactions(self):
        """שולף את היסטוריית העסקאות של המשתמש הנוכחי ממסד הנתונים/השרת."""
        try:
            user_id = load_user_id()
            response = requests.get(f"{API_URL}/users/{user_id}/transactions")
            if response.status_code == 200:
                transactions = response.json()
                self.populate_table(transactions)
            else:
                layout = self.layout()
        except requests.exceptions.RequestException as e:
            pass 


    def populate_table(self, transactions):
        """ממלא את טבלת ההיסטוריה (QTableWidget) בנתוני העסקאות שנשלפו."""
        sorted_transactions = sorted(transactions, key=lambda x: x["TransactionID"], reverse=True)
        self.table.setRowCount(len(sorted_transactions))
        self.table.setColumnCount(5)
        headers = ["Transaction ID", "User ID", "Stock Symbol", "Quantity", "Price Per Stock"]
        self.table.setHorizontalHeaderLabels(headers)

        for row, transaction in enumerate(sorted_transactions):
            # Transaction ID
            self.table.setItem(row, 0, self.create_readonly_item(str(transaction["TransactionID"])))

            # User ID
            self.table.setItem(row, 1, self.create_readonly_item(str(transaction["UserID"])))

            # Stock Symbol
            self.table.setItem(row, 2, self.create_readonly_item(transaction["StockSymbol"]))

            # Quantity
            quantity_item = self.create_readonly_item(str(transaction["Quantity"]))
            self.table.setItem(row, 3, quantity_item)

            # Price Per Stock
            price_item = self.create_readonly_item(str(transaction["PricePerStock"]))
            self.table.setItem(row, 4, price_item)

            # Set background color for the entire row based on buy/sell
            if transaction["Quantity"] > 0:  # Positive value (Buy)
                background_color = QColor("#e8f5e9")  # Light green
            elif transaction["Quantity"] < 0:  # Negative value (Sell)
                background_color = QColor("#ffebee")  # Light red
            else:
                background_color = QColor("#ffffff")  # White (Default)

            # Apply the background color to all cells in the row
            for column in range(5):
                self.table.item(row, column).setBackground(background_color)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def create_readonly_item(self, text):
        """פעולת עזר ליצירת תא טבלה תקני, לא ניתן לעריכה, ומיושר למרכז."""
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        item.setTextAlignment(Qt.AlignCenter)

        return item

    def update_price(self, source="buy"):
        """שולף את מחיר השוק העדכני ביותר עבור סמל המניה שנבחר באמצעות yfinance."""
        if source == "buy":
            stock = self.buy_stock_symbol.currentText()
            label = self.buy_price_label
        else:
            stock = self.sell_stock_symbol.currentText()
            label = self.sell_price_label

        try:
            print(f"Fetching price for {stock}...")
            stock_data = yf.Ticker(stock)
            history = stock_data.history(period="1d")
            
            if history.empty:
                print(f"Warning: History empty for {stock}")
                label.setText("Price: N/A")
                price = 0
            else:
                price = history["Close"].iloc[-1]
                print(f"Price for {stock}: {price}")
                label.setText(f"Price: {price:.2f}")

            if source == "buy":
                self.current_buy_price = price
            else:
                self.current_sell_price = price
        except Exception as e:
            print(f"Error fetching price for {stock}: {e}")
            label.setText("Price: Error")
            if source == "buy":
                self.current_buy_price = 0
            else:
                self.current_sell_price = 0


    def buy_stock(self):
        """
        מבצע פקודת קנייה.
        מוודא את יתרת המשתמש מול העלות הכוללת לפני שליחת העסקה לשרת.
        """
        user_id = load_user_id()
        
        # Fetch user details to get the balance
        try:
            print(f"Fetching user details for ID: {user_id}")
            user_response = requests.get(f"{API_URL}/users/{user_id}")
            if user_response.status_code == 200:
                user_data = user_response.json()
                print(f"User data received: {user_data}")
                user_balance = float(user_data.get("Balance", 0.0)) # Cast to float
            else:
                QMessageBox.warning(self, "Error", f"Failed to fetch user details. Status: {user_response.status_code}")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid balance format received from server.")
            return
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")
            return
        except Exception as e:
             QMessageBox.critical(self, "Error", f"Unexpected error checking balance: {e}")
             return

        # Calculate the total cost of the purchase
        total_cost = self.buy_quantity.value() * self.current_buy_price


        # Check if the user has enough balance
        if user_balance < total_cost:
            QMessageBox.warning(self, "Insufficient Balance", 
                                f"You do not have enough balance to complete this purchase.\n"
                                f"Your balance: {user_balance:.2f}\n"
                                f"Total cost: {total_cost:.2f}")
            return

        # Proceed with the transaction if balance is sufficient
        transaction_data = {
            "UserID": user_id,
            "StockSymbol": self.buy_stock_symbol.currentText(),
            "Quantity": self.buy_quantity.value(),
            "PricePerStock": round(self.current_buy_price, 2)
        }

        try:
            # Send the transaction
            response = requests.post(f"{API_URL}/transactions", json=transaction_data, headers={"Content-Type": "application/json"})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Stock purchased successfully!")
                self.load_transactions()
            else:
                 error_msg = f"Status code: {response.status_code}"
                 try:
                     error_msg += f"\nDetails: {response.json()}"
                 except:
                     error_msg += f"\nResponse: {response.text}"
                 QMessageBox.warning(self, "Error", f"Transaction failed.\n{error_msg}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")

    def sell_stock(self):
        """
        מבצע פקודת מכירה.
        מוודא שהמשתמש מחזיק במספיק מניות מהסוג הנבחר לפני שליחת העסקה.
        """
        user_id = load_user_id()
        stock_symbol = self.sell_stock_symbol.currentText()
        sell_quantity = self.sell_quantity.value()

        # Check if user has enough shares
        user_stock_quantity = self.get_user_stock_quantity(user_id, stock_symbol)
        if user_stock_quantity < sell_quantity:
            QMessageBox.warning(self, "Error", 
                                f"You do not have enough of the stock '{stock_symbol}' to sell.\n"
                                f"Your quantity: {user_stock_quantity}\n"
                                f"Quantity to sell: {sell_quantity}")
            return

        # Proceed with the transaction
        transaction_data = {
            "UserID": user_id,
            "StockSymbol": stock_symbol,
            "Quantity": -1 * sell_quantity,  # Negative quantity for selling
            "PricePerStock": round(self.current_sell_price, 2)
        }

        try:
            # Send the transaction
            response = requests.post(f"{API_URL}/transactions", json=transaction_data, headers={"Content-Type": "application/json"})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Stock sold successfully!")
                self.load_transactions()
            else:
                 error_msg = f"Status code: {response.status_code}"
                 try:
                     error_msg += f"\nDetails: {response.json()}"
                 except:
                     error_msg += f"\nResponse: {response.text}"
                 QMessageBox.warning(self, "Error", f"Transaction failed.\n{error_msg}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")

    def get_user_stock_quantity(self, user_id, stock_symbol):
        """פעולת עזר לחישוב הכמות נטו המוחזקת כעת עבור סמל מניה ספציפי."""
        try:
            # Fetch user transactions directly
            response = requests.get(f"{API_URL}/users/{user_id}/transactions")
            response.raise_for_status()  

            transactions = response.json()

            # Filter by stockSymbol
            stock_transactions = [
                t for t in transactions
                if t.get("StockSymbol") == stock_symbol
            ]

            total_quantity = sum(t.get("Quantity", 0) for t in stock_transactions)
            return total_quantity

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")
            return 0
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            return 0

    
    def send_transaction(self, transaction_data, success_message):
        """פעולת עזר לשליחת צקשת HTTP POST עבור עסקה (קנייה או מכירה)."""
        try:
            response = requests.post(API_URL, json=transaction_data, headers={"Content-Type": "application/json"})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", success_message)
                self.load_transactions()
            else:
                QMessageBox.warning(self, "Error", "Transaction failed.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Request failed: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransactionsWindow()
    window.show()
    sys.exit(app.exec())

