from db_config import get_connection

def create_employee_table():
    conn = get_connection()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS employee (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        department VARCHAR(100),
        salary DECIMAL(10,2)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Employee table created successfully.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_employee_table()
