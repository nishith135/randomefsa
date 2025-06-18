from db_config import get_connection

def fetch_operators():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM operators")
    rows = cursor.fetchall()
    print("ID | Username | Password")
    print("-" * 30)
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

if __name__ == "__main__":
