from db_config import get_connection

# Insert into product_master
def insert_product_data(sku_id, barcode, category, subcategory, product_name, description, price, tax, unit, image_path=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO product_master 
            (sku_id, barcode, category, subcategory, product_name, description, price, tax, unit, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (sku_id, barcode, category, subcategory, product_name, description, price, tax, unit, image_path)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting product data:", e)
        return False


# Insert into goods_receiving
def insert_goods_data(product_name, quantity, supplier):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO goods_receiving (product_name, quantity, supplier)
            VALUES (%s, %s, %s)
            """,
            (product_name, quantity, supplier)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting goods data:", e)
        return False


# Insert into sales
def insert_sales_data(product_id, quantity, customer_name, unit, rate_per_unit, tax):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        total_rate = float(quantity) * float(rate_per_unit)

        cursor.execute(
            """
            INSERT INTO sales 
            (product_id, customer_name, quantity, unit, rate_per_unit, total_rate, tax)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (product_id, customer_name, quantity, unit, rate_per_unit, total_rate, tax)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Error inserting sales data:", e)
        return False
