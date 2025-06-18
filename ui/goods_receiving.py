from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QComboBox, QSpacerItem, QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt
from db_config import get_connection

class GoodsReceivingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QLineEdit, QComboBox {
                font-size: 16px;
                padding: 6px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                min-width: 200px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        title = QLabel("GOODS RECEIVING")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        self.barcode_input = QLineEdit()
        self.product_id_input = QLineEdit()
        self.product_name_input = QLineEdit()
        self.supplier_input = QLineEdit()
        self.quantity_input = QLineEdit("0")
        self.unit_input = QComboBox()
        self.unit_input.addItems(["kg", "pcs", "liters"])
        self.rate_input = QLineEdit()
        self.tax_rate_input = QComboBox()
        self.tax_rate_input.addItems(["0%", "5%", "12%", "18%", "28%"])
        self.total_display = QLineEdit("0.00")
        self.total_display.setReadOnly(True)

        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)
        self.tax_rate_input.currentTextChanged.connect(self.calculate_total)

        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("Product ID:", self.product_id_input)
        form_layout.addRow("Product Name:", self.product_name_input)
        form_layout.addRow("Supplier:", self.supplier_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Unit:", self.unit_input)
        form_layout.addRow("Rate:", self.rate_input)
        form_layout.addRow("Tax Rate:", self.tax_rate_input)
        form_layout.addRow("Total:", self.total_display)

        self.submit_button = QPushButton("SUBMIT RECEIPT")
        self.submit_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px;")
        self.submit_button.clicked.connect(self.submit_form)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(button_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

    def calculate_total(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax_percent = float(self.tax_rate_input.currentText().replace('%', ''))
            subtotal = qty * rate
            total = subtotal * (1 + tax_percent / 100)
            self.total_display.setText(f"{total:.2f}")
        except ValueError:
            self.total_display.setText("0.00")

    def submit_form(self):
        try:
            barcode = self.barcode_input.text().strip()
            product_id = self.product_id_input.text().strip()
            product_name = self.product_name_input.text().strip()
            supplier_name = self.supplier_input.text().strip()
            quantity = float(self.quantity_input.text())
            unit = self.unit_input.currentText()
            rate = float(self.rate_input.text())
            tax_percent = float(self.tax_rate_input.currentText().replace('%', ''))
            total_rate = float(self.total_display.text())

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO product_master 
                (barcode, sku_id, category, subcategory, product_name, description, tax, price, unit)
                VALUES (%s, %s, %s, %s, %s, '', %s, %s, %s)
            """, (barcode, product_id, '', '', product_name, tax_percent, rate, unit))

            cursor.execute("""
                INSERT INTO goods_receiving 
                (product_id, product_name, supplier_name, quantity, unit, rate, tax, total_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (product_id, product_name, supplier_name, quantity, unit, rate, tax_percent, total_rate))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Goods received and product added successfully!")

            # Clear fields
            self.barcode_input.clear()
            self.product_id_input.clear()
            self.product_name_input.clear()
            self.supplier_input.clear()
            self.quantity_input.setText("0")
            self.unit_input.setCurrentIndex(0)
            self.rate_input.clear()
            self.tax_rate_input.setCurrentIndex(0)
            self.total_display.setText("0.00")

        except Exception as e:
            QMessageBox.critical(self, "Submission Error", str(e))
