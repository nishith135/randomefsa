from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, Signal
from ui.goods_receiving import GoodsReceivingForm
from ui.sales_form import SalesForm
from ui.product_master import ProductMasterForm

class DashboardPage(QWidget):
    logout_requested = Signal()  # Signal for logout

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget#SidebarContainer {
                background-color: #b0b0b0;
                border-right: 2px solid #aaa;
            }
            QPushButton {
                padding: 12px 16px;
                font-size: 17px;
                text-align: left;
                border: 1px solid #bbb;
                border-radius: 8px;
                background-color: white;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
            QPushButton#LogoutButton {
                color: white;
                background-color: #cc3300;
            }
            QPushButton#LogoutButton:hover {
                background-color: #b32d00;
            }
            QLabel#sidebarHeader {
                font-size: 18px;
                font-weight: bold;
                margin: 10px 0;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("SidebarContainer")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setAlignment(Qt.AlignTop)

        header = QLabel("📦 Inventory System")
        header.setObjectName("sidebarHeader")
        header.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(header)

        self.goods_btn = QPushButton("📥 Goods Receiving")
        self.sales_btn = QPushButton("🧾 Sales")
        self.product_btn = QPushButton("🗂 Product Master")
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setObjectName("LogoutButton")

        sidebar_layout.addWidget(self.goods_btn)
        sidebar_layout.addWidget(self.sales_btn)
        sidebar_layout.addWidget(self.product_btn)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.logout_btn)

        # Main content area
        self.stack = QStackedWidget()
        self.stack.addWidget(GoodsReceivingForm())
        self.stack.addWidget(SalesForm())
        self.stack.addWidget(ProductMasterForm())

        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.stack, 4)

        # Connect buttons
        self.goods_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.sales_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.product_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.logout_btn.clicked.connect(self.logout_requested.emit)
