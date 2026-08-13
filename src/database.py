import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "pc_repair_system")
    )


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("MySQL connection successful!")

        connection.close()

    except mysql.connector.Error as error:
        print("MySQL connection failed!")
        print("Error:", error)