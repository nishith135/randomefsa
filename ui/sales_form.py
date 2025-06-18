from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QDateEdit, QLabel, QPushButton, QSpacerItem, QSizePolicy,
    QMessageBox, QCompleter
)
from PySide6.QtCore import QDate, Qt
from db_config import get_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QLineEdit, QComboBox, QDateEdit {
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
        self.load_product_barcodes()

    def init_ui(self):
        title = QLabel("SALES FORM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        self.barcode_input = QLineEdit()
        self.barcode_input.editingFinished.connect(self.autofill_product_data)

        self.customer_input = QLineEdit()
        self.quantity_input = QLineEdit()

        self.unit_input = QComboBox()
        self.unit_list = ["kg", "litre", "pcs", "box", "unit"]
        self.unit_input.addItems(self.unit_list)

        self.rate_input = QLineEdit()
        self.tax_rate_input = QComboBox()
        self.tax_rate_input.addItems(["0%", "5%", "12%", "18%", "28%"])

        self.total_label = QLabel("TOTAL: ₹0.00")
        self.total_label.setStyleSheet("color: red; font-weight: bold; font-size: 16px;")

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())

        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)
        self.tax_rate_input.currentTextChanged.connect(self.calculate_total)

        form_layout.addRow("Product Barcode:", self.barcode_input)
        form_layout.addRow("Customer Name:", self.customer_input)
        form_layout.addRow("Quantity:", self.quantity_input)
        form_layout.addRow("Unit:", self.unit_input)
        form_layout.addRow("Rate per Unit:", self.rate_input)
        form_layout.addRow("Tax Rate:", self.tax_rate_input)
        form_layout.addRow("Date:", self.date_input)

        self.record_button = QPushButton("RECORD SALE")
        self.record_button.setStyleSheet("background-color: #dc3545; color: white; border-radius: 5px;")
        self.record_button.clicked.connect(self.record_sale)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.record_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(self.total_label, alignment=Qt.AlignRight)

        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

    def load_product_barcodes(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT barcode FROM product_master")
            barcodes = [row[0] for row in cursor.fetchall()]
            completer = QCompleter(barcodes)
            self.barcode_input.setCompleter(completer)
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "DB Error", f"Could not load Barcodes: {e}")

    def autofill_product_data(self):
        barcode = self.barcode_input.text().strip()
        if not barcode:
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT unit, price, tax FROM product_master WHERE barcode = %s", (barcode,))
            result = cursor.fetchone()
            if result:
                unit, price, tax = result

                index = self.unit_input.findText(unit, Qt.MatchFixedString)
                if index >= 0:
                    self.unit_input.setCurrentIndex(index)
                else:
                    self.unit_input.addItem(unit)
                    self.unit_input.setCurrentText(unit)

                self.rate_input.setText(str(price))

                tax_str = f"{int(tax)}%"
                tax_index = self.tax_rate_input.findText(tax_str)
                if tax_index != -1:
                    self.tax_rate_input.setCurrentIndex(tax_index)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.warning(self, "Auto-fill Error", f"Could not fetch product data: {e}")

    def calculate_total(self):
        try:
            quantity = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            tax = float(self.tax_rate_input.currentText().replace('%', ''))
            total = (quantity * rate) * (1 + tax / 100)
            self.total_label.setText(f"TOTAL: ₹{total:.2f}")
        except ValueError:
            self.total_label.setText("TOTAL: ₹0.00")

    def record_sale(self):
        barcode = self.barcode_input.text().strip()
        customer_name = self.customer_input.text().strip()
        unit = self.unit_input.currentText()

        try:
            quantity = float(self.quantity_input.text())
            rate_per_unit = float(self.rate_input.text())
            tax_percent = float(self.tax_rate_input.currentText().replace('%', ''))
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for Quantity, Rate, and Tax.")
            return

        tax_amount = (rate_per_unit * quantity) * (tax_percent / 100)
        total_rate = (rate_per_unit * quantity) + tax_amount
        date = self.date_input.date().toPython()

        if not (barcode and customer_name):
            QMessageBox.warning(self, "Missing Info", "Please fill in Product Barcode and Customer Name.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sales (product_id, customer_name, quantity, unit, rate_per_unit, total_rate, tax, sale_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (barcode, customer_name, quantity, unit, rate_per_unit, total_rate, tax_percent, date))
            conn.commit()
            cursor.close()
            conn.close()

            self.total_label.setText(f"TOTAL: ₹{total_rate:.2f}")
            QMessageBox.information(self, "Success", "Sale recorded successfully.")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not save data:\n{e}")

    def clear_form(self):
        self.barcode_input.clear()
        self.customer_input.clear()
        self.quantity_input.clear()
        self.rate_input.clear()
        self.tax_rate_input.setCurrentIndex(0)
        self.unit_input.setCurrentIndex(0)
        self.total_label.setText("TOTAL: ₹0.00")
        self.date_input.setDate(QDate.currentDate())
