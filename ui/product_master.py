from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QLabel, QFileDialog, QHBoxLayout, QSpacerItem,
    QSizePolicy, QMessageBox
)
from PySide6.QtCore import Qt
from db_config import get_connection  # Ensure db_config.py returns a valid MySQL connection


class ProductMasterForm(QWidget):
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

    def browse_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_path_input.setText(path)

    def init_ui(self):
        title = QLabel("PRODUCT MASTER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignCenter)

        self.product_id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.barcode_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Electronics", "Clothing", "Food", "Furniture"])
        self.subcategory_input = QLineEdit()
        self.description_input = QLineEdit()
        self.price_input = QLineEdit()
        self.tax_rate_input = QComboBox()
        self.tax_rate_input.addItems(["0%", "5%", "12%", "18%", "28%"])
        self.unit_input = QComboBox()
        self.unit_input.addItems(["kg", "g", "litre", "piece"])

        self.image_path_input = QLineEdit()
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_image)

        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_path_input)
        image_layout.addWidget(browse_button)

        form_layout.addRow("Product ID:", self.product_id_input)
        form_layout.addRow("Product Name:", self.name_input)
        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("SKU:", self.sku_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Subcategory:", self.subcategory_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Tax Rate:", self.tax_rate_input)
        form_layout.addRow("Unit:", self.unit_input)
        form_layout.addRow("Product Image:", image_layout)

        self.save_button = QPushButton("SAVE PRODUCT")
        self.save_button.setStyleSheet("background-color: #28a745; color: white; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_product)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

    def save_product(self):
        product_id = self.product_id_input.text().strip()
        product_name = self.name_input.text().strip()
        barcode = self.barcode_input.text().strip()
        sku_id = self.sku_input.text().strip()
        category = self.category_input.currentText()
        subcategory = self.subcategory_input.text().strip()
        description = self.description_input.text().strip()

        try:
            price = float(self.price_input.text())
            tax = float(self.tax_rate_input.currentText().replace('%', ''))
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Price and Tax must be numbers.")
            return

        unit = self.unit_input.currentText()
        image_path = self.image_path_input.text().strip()

        if not product_id:
            QMessageBox.warning(self, "Missing Field", "Product ID is required.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if product_id already exists
            cursor.execute("SELECT id FROM product_master WHERE id = %s", (product_id,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Duplicate ID", "Product ID already exists. Please choose a unique ID.")
                cursor.close()
                conn.close()
                return

            cursor.execute("""
                INSERT INTO product_master 
                (id, barcode, sku_id, category, subcategory, product_name, description, tax, price, unit, image_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (product_id, barcode, sku_id, category, subcategory, product_name,
                  description, tax, price, unit, image_path))
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Success", "Product added successfully!")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_form(self):
        self.product_id_input.clear()
        self.name_input.clear()
        self.barcode_input.clear()
        self.sku_input.clear()
        self.subcategory_input.clear()
        self.description_input.clear()
        self.price_input.clear()
        self.image_path_input.clear()
