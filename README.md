# Infoware Inventory Management System

This is a desktop-based Inventory Management System developed using **PySide6** and **MySQL** for Infoware's internship assignment.

## 📋 Features

### 1. Operator Login
- Secure login for two predefined operator accounts.
- Authenticates users before allowing access to forms.

### 2. Product Master Form
- Add new products with:
  - Barcode, SKU ID
  - Category, Subcategory
  - Product Name & Description
  - Tax %, Price, Unit
  - Product Image path (optional)
- Supports alphanumeric `product_id` for flexibility.

### 3. Goods Receiving Form
- Enter stock received from suppliers:
  - Product ID, Quantity, Unit
  - Rate per Unit, Total, Tax

### 4. Sales Form
- Record sales made to customers:
  - Product ID, Customer, Quantity, Rate, Unit
  - Tax %, Total

## 🗄️ Database

- **Database Name**: `infoware_db`
- Built using **MySQL**.
- Tables:
  - `operators`
  - `product_master`
  - `goods_receiving`
  - `sales`

## 👩‍💻 Technologies Used

- [x] Python 3
- [x] PySide6 (for GUI)
- [x] MySQL (local database)
- [x] PyMySQL (DB connector)

## 🔐 Operator Logins

| Username  | Password   |
|-----------|------------|
| operator1 | password123|
| operator2 | admin456   |

## 🚀 How to Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
