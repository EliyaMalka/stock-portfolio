import sys
import requests
import yfinance as yf
from PySide6.QtCore import Qt, QFile, QTextStream, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QFrame, QSpacerItem, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView
)


class UserDetailsWindow(QMainWindow):
    LABEL_WIDTH = 90
    BUTTON_WIDTH = 75

   
    def __init__(self, user_id, api_url, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.api_url = api_url
        self.editable_fields = []
        self.init_ui()
        self.load_user_details()
        self.load_portfolio()


    def init_ui(self):
        self.setWindowTitle("User Details")
        self.setGeometry(100, 100, 700, 600)  # Increased height for table
        self.load_stylesheet(r"view\userDetails.qss") # Adjust path if needed

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 25, 30, 25)

        self.title_label = QLabel("User Details", self)
        self.title_label.setObjectName("mainLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # --- Form Fields Area ---
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        self.username = self.create_input_field(form_layout, "Username:")
        self.email = self.create_input_field(form_layout, "Email:")
        self.balance_label = self.create_balance_display(form_layout)

        self.main_layout.addLayout(form_layout)

        self.main_layout.addWidget(self.create_separator())

        # --- Portfolio Section ---
        portfolio_label = QLabel("Portfolio Holdings", self)
        portfolio_label.setObjectName("sectionLabel") # Assuming specific style or generic label style
        portfolio_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        self.main_layout.addWidget(portfolio_label)

        self.portfolio_table = QTableWidget()
        self.portfolio_table.setColumnCount(4)
        self.portfolio_table.setHorizontalHeaderLabels(["Symbol", "Quantity", "Current Price", "Total Value"])
        self.portfolio_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.portfolio_table.verticalHeader().setVisible(False)
        self.main_layout.addWidget(self.portfolio_table)

        self.main_layout.addWidget(self.create_separator())

        # --- Buttons Area ---
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.setObjectName("saveButton")
        self.save_button.setFixedWidth(140)
        self.save_button.setFixedHeight(38)
        self.save_button.clicked.connect(self.save_user_details)
        button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(button_layout)
        # self.main_layout.addStretch(1) # Removed stretch to let table expand

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("separatorFrame")
        return separator

    def load_stylesheet(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()
        else:
            print(f"Warning: Could not load stylesheet from {path}")

    def create_input_field(self, parent_layout, label_text):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        label = QLabel(label_text, self)
        label.setFixedWidth(self.LABEL_WIDTH)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setObjectName("fieldLabel")
        row_layout.addWidget(label)

        input_field = QLineEdit(self)
        input_field.setReadOnly(True)
        input_field.setFixedHeight(36)
        input_field.setProperty("fieldId", label_text.replace(":", "").lower())
        row_layout.addWidget(input_field)

        edit_button = QPushButton("Edit", self)
        edit_button.setFixedWidth(self.BUTTON_WIDTH)
        edit_button.setFixedHeight(36)
        edit_button.setObjectName("editButton")
        
        # We need to capture the specific field and button for the lambda
        edit_button.clicked.connect(lambda checked=False, f=input_field, b=edit_button: self.toggle_edit(f, b))
        
        row_layout.addWidget(edit_button)
        # Store the field and its button together
        # self.editable_fields.append({'field': input_field, 'button': edit_button}) # This is handled differently now
        parent_layout.addLayout(row_layout)
        return input_field

    def create_balance_display(self, parent_layout):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        label = QLabel("Balance:", self)
        label.setFixedWidth(self.LABEL_WIDTH)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setObjectName("fieldLabel")
        row_layout.addWidget(label)

        balance_value = QLabel("Loading...", self)
        balance_value.setObjectName("balanceValue") # For special styling if needed
        balance_value.setStyleSheet("font-weight: bold; color: #2e7d32; font-size: 14px;")
        row_layout.addWidget(balance_value)
        
        # Spacer to push balance to left, matching inputs
        row_layout.addStretch(1) 
        
        # Balance is usually not editable directly here, or maybe adds 'Add Funds' button later
        # For now, just display.
        parent_layout.addLayout(row_layout)
        return balance_value

    def toggle_edit(self, field, button):
        if field.isReadOnly():
            field.setReadOnly(False)
            field.setFocus()
            button.setText("Cancel")
            # Store original value to restore if cancelled
            field.setProperty("original_text", field.text())
            if field not in [f['field'] for f in self.editable_fields]:
                 self.editable_fields.append({'field': field, 'button': button})
        else:
            field.setReadOnly(True)
            button.setText("Edit")
            # Restore original value
            if field.property("original_text") is not None:
                field.setText(field.property("original_text"))
            # Remove from editable_fields list
            self.editable_fields = [item for item in self.editable_fields if item['field'] is not field]

        # Apply style changes
        field.style().unpolish(field)
        field.style().polish(field)
        button.style().unpolish(button)
        button.style().polish(button)
        
    def load_user_details(self):
        try:
            response = requests.get(f"{self.api_url}/{self.user_id}")
            if response.status_code == 200:
                user_data = response.json()
                self.username.setText(user_data.get("Username", ""))
                self.email.setText(user_data.get("Email", ""))
                balance = float(user_data.get("Balance", 0))
                self.balance_label.setText(f"${balance:,.2f}")
                self.reset_edit_states()
            else:
                 QMessageBox.warning(self, "Error", f"Failed to load details: {response.status_code}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred loading details: {str(e)}")


    def load_portfolio(self):
        try:
            response = requests.get(f"{self.api_url}/{self.user_id}/transactions")
            if response.status_code == 200:
                transactions = response.json()
                
                # Aggregate holdings
                holdings = {}
                for t in transactions:
                    symbol = t['StockSymbol'].upper()
                    qty = t['Quantity']
                    holdings[symbol] = holdings.get(symbol, 0) + qty
                
                # Filter > 0
                current_holdings = {k: v for k, v in holdings.items() if v > 0}
                
                self.portfolio_table.setRowCount(len(current_holdings))
                
                for row, (symbol, qty) in enumerate(current_holdings.items()):
                    self.portfolio_table.setItem(row, 0, QTableWidgetItem(symbol))
                    self.portfolio_table.setItem(row, 1, QTableWidgetItem(str(qty)))
                    
                    # Fetch price
                    try:
                        ticker = yf.Ticker(symbol)
                        history = ticker.history(period="1d")
                        if not history.empty:
                            price = history["Close"].iloc[-1]
                            value = price * qty
                            self.portfolio_table.setItem(row, 2, QTableWidgetItem(f"${price:.2f}"))
                            self.portfolio_table.setItem(row, 3, QTableWidgetItem(f"${value:.2f}"))
                        else:
                            self.portfolio_table.setItem(row, 2, QTableWidgetItem("N/A"))
                            self.portfolio_table.setItem(row, 3, QTableWidgetItem("N/A"))
                    except:
                         self.portfolio_table.setItem(row, 2, QTableWidgetItem("Error"))
                         self.portfolio_table.setItem(row, 3, QTableWidgetItem("Error"))
            else:
                # Silently fail or log for now
                print(f"Failed to load transactions: {response.status_code}")
        except Exception as e:
            print(f"Error loading portfolio: {e}")


    def save_user_details(self):
        username_text = self.username.text().strip()
        email_text = self.email.text().strip()

        if not username_text or not email_text:
            QMessageBox.warning(self, "Validation Error", "Username and Email cannot be empty.")
            return

        payload = {
            "Username": username_text,
            "Email": email_text
        }

        self.save_button.setEnabled(False)
        self.save_button.setText("Saving...")
        self.save_button.style().unpolish(self.save_button)
        self.save_button.style().polish(self.save_button)
        QApplication.processEvents()

        try:
            response = requests.put(f"{self.api_url}/{self.user_id}", json=payload)
            
            if response.status_code in [200, 204]:
                QMessageBox.information(self, "Success", "User details updated successfully.")
                self.load_user_details() # Reload to refresh and reset
            else:
                QMessageBox.critical(self, "API Error", f"Failed to update user details. Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to save data: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during save: {str(e)}")
        finally:
            self.save_button.setEnabled(True)
            self.save_button.setText("Save Changes")
            self.save_button.style().unpolish(self.save_button)
            self.save_button.style().polish(self.save_button)


    def reset_edit_states(self):
        """ Resets ALL editable fields to read-only and ensures their buttons say 'Edit'. """
        for item in self.editable_fields:
            field = item['field']
            button = item['button']
            
            if not field.isReadOnly():
                field.setReadOnly(True)
            
            if button.text() != "Edit":
                button.setText("Edit")
                
            field.style().unpolish(field)
            field.style().polish(field)
            button.style().unpolish(button)
            button.style().polish(button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_id_to_show = 4
    api_endpoint = "http://localhost:8000/api/v1/users" # Corrected default for testing
    window = UserDetailsWindow(user_id_to_show, api_endpoint)
    window.show()
    sys.exit(app.exec())