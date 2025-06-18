# login.py
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class LoginPage(QWidget):
    login_successful = Signal()

    def __init__(self):
        super().__init__()

        # Centered vertical layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # Title
        title = QLabel("INVENTORY SYSTEM")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")

        # Inputs
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(300)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(300)

        # Login button
        login_button = QPushButton("Login")
        login_button.setFixedWidth(300)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        login_button.clicked.connect(self.handle_login)

        # Add widgets
        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)

        # Background styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
            }
        """)

    def handle_login(self):
        if self.username.text().strip() and self.password.text().strip():
            self.login_successful.emit()
