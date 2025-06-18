import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

# Get absolute path
current_dir = Path(__file__).parent.absolute()
print(f"Current directory: {current_dir}")
print(f"Files in directory: {os.listdir(current_dir)}")
sys.path.insert(0, str(current_dir))

# Import custom pages
try:
    from dashboard import DashboardPage
    from login import LoginPage
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    raise

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory System")
        self.resize(600, 400)  # smaller and more practical size

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage()
        self.dashboard_page = DashboardPage()

        self.stack.addWidget(self.login_page)     # index 0
        self.stack.addWidget(self.dashboard_page) # index 1

        self.login_page.login_successful.connect(self.show_dashboard)
        self.dashboard_page.logout_requested.connect(self.show_login)

        self.stack.setCurrentWidget(self.login_page)

    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
