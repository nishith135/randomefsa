import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Replace with your MySQL username
        password="Giyu@123",  # Replace with your MySQL password
        database="infoware_db"
    )

if __name__ == "__main__":
    conn = get_connection()
    print("Connected:", conn.is_connected())
    conn.close()
