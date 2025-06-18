from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFrame
from PySide6.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
from PySide6.QtCore import Qt
from db_config import get_connection
from ui.dashboard import Dashboard

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory System")
        self.setFixedSize(600, 400)
        self.setAutoFillBackground(True)

        # Set gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor("#a1c4fd"))
        gradient.setColorAt(1.0, QColor("#c2e9fb"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Card container
        card = QFrame()
        card.setFixedSize(400, 300)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4285f4;
                color: white;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ae8;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("ACCOUNT LOGIN")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login Button
        self.login_button = QPushButton("LOG IN")
        self.login_button.clicked.connect(self.check_login)

        # Layouting
        card_layout.addWidget(title)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.login_button)

        outer_layout.addWidget(card)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM operators WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                QMessageBox.information(self, "Success", "Login successful!")
                self.dashboard = Dashboard()
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Failed", "Invalid credentials.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
