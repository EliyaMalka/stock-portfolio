import sys
import requests
from PySide6.QtCore import Qt, QFile, QTextStream, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QFrame, QSpacerItem, QSizePolicy
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


    def init_ui(self):
        self.setWindowTitle("User Details")
        self.setGeometry(100, 100, 650, 450)
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
        self.main_layout.addStretch(1)

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
        edit_button.setObjectName("editToggleButton")
        # Connect using lambda, passing the specific field
        edit_button.clicked.connect(lambda checked=False, field=input_field: self.toggle_edit_mode(field))
        row_layout.addWidget(edit_button)

        # Store the field and its button together
        self.editable_fields.append({'field': input_field, 'button': edit_button})

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

        balance_value_label = QLabel("0", self)
        balance_value_label.setObjectName("balanceValueLabel")
        balance_value_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        balance_value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        balance_value_label.setFixedHeight(36)
        balance_value_label.setStyleSheet("padding-left: 10px;")
        row_layout.addWidget(balance_value_label)

        placeholder = QWidget()
        placeholder.setFixedWidth(self.BUTTON_WIDTH)
        row_layout.addWidget(placeholder)

        parent_layout.addLayout(row_layout)
        return balance_value_label

    def toggle_edit_mode(self, clicked_field):
        """
        Toggles the edit mode for the clicked field.
        Ensures only one field is editable at a time.
        If the clicked field was already being edited, it locks it.
        """
        currently_editing = not clicked_field.isReadOnly()
        new_edit_state = not currently_editing # The desired state for the clicked field

        # --- Step 1: Reset all OTHER fields to read-only ---
        for item in self.editable_fields:
            field = item['field']
            button = item['button']
            # Only reset if it's NOT the clicked field AND it's currently editable
            if field is not clicked_field and not field.isReadOnly():
                field.setReadOnly(True)
                button.setText("Edit")
                button.setToolTip("Click to edit this field")
                # Apply style changes
                field.style().unpolish(field)
                field.style().polish(field)
                button.style().unpolish(button)
                button.style().polish(button)

        # --- Step 2: Set the state for the CLICKED field ---
        clicked_button = None
        for item in self.editable_fields:
            if item['field'] is clicked_field:
                clicked_button = item['button']
                break

        if clicked_button:
            # Set the field's read-only state based on the desired new state
            clicked_field.setReadOnly(not new_edit_state)

            if new_edit_state: # If the field should become editable
                clicked_button.setText("Lock")
                clicked_button.setToolTip("Click to lock this field")
                clicked_field.setFocus() # Focus when editable
            else: # If the field should become read-only
                clicked_button.setText("Edit")
                clicked_button.setToolTip("Click to edit this field")
                clicked_field.clearFocus()

            # Apply style changes for the clicked field/button
            clicked_field.style().unpolish(clicked_field)
            clicked_field.style().polish(clicked_field)
            clicked_button.style().unpolish(clicked_button)
            clicked_button.style().polish(clicked_button)


        
        
    def load_user_details(self):
        try:
            response = requests.get(f"{self.api_url}/{self.user_id}")
            response.raise_for_status()
            user_data = response.json()
            self.username.setText(user_data.get("Username", ""))
            self.email.setText(user_data.get("Email", ""))
            balance = float(user_data.get("Balance", 0))
            self.balance_label.setText(f"{balance:,.2f}")
            self.reset_edit_states()

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to API: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred loading details: {str(e)}")


    def save_user_details(self):
        username_text = self.username.text().strip()
        email_text = self.email.text().strip()

        if not username_text or not email_text:
            QMessageBox.warning(self, "Validation Error", "Username and Email cannot be empty.")
            return

        r = requests.get(f"{self.api_url}/{self.user_id}")
        user_data = r.json()

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
            response.raise_for_status()

            if response.status_code in [200, 204]:
                QMessageBox.information(self, "Success", "User details updated successfully.")
                balance = float(user_data.get("Balance", 0))
                self.balance_label.setText(f"{balance:,.2f}")
                self.reset_edit_states()
            else:
                error_msg = f"Status code: {response.status_code}"
                try:
                    error_msg += f"\nDetails: {response.json()}"
                except:
                    error_msg += f"\nResponse: {response.text}"
                QMessageBox.critical(self, "API Error", f"Failed to update user details.\n{error_msg}")

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
            needs_update = False # Flag to check if style refresh is needed

            if not field.isReadOnly(): # If it was editable, lock it
                field.setReadOnly(True)
                needs_update = True

            # Ensure button text is always "Edit" after reset
            if button.text() != "Edit":
                button.setText("Edit")
                button.setToolTip("Click to edit this field")
                needs_update = True

            # Apply style refresh only if something changed
            if needs_update:
                field.style().unpolish(field)
                field.style().polish(field)
                button.style().unpolish(button)
                button.style().polish(button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_id_to_show = 4
    api_endpoint = "http://localhost:5235/api/Users"
    window = UserDetailsWindow(user_id_to_show, api_endpoint)
    window.show()
    sys.exit(app.exec())