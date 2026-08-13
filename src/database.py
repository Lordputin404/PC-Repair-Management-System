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


# ---------------- CUSTOMER FUNCTIONS ----------------

def add_customer(name, phone):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO customers (name, phone)
        VALUES (%s, %s)
    """

    cursor.execute(query, (name, phone))
    connection.commit()

    customer_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return customer_id


def get_customers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT customer_id, name, phone
        FROM customers
        ORDER BY customer_id DESC
    """)

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers


def update_customer(customer_id, name, phone):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE customers
        SET name = %s, phone = %s
        WHERE customer_id = %s
    """

    cursor.execute(query, (name, phone, customer_id))
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def delete_customer(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM customers
        WHERE customer_id = %s
    """

    cursor.execute(query, (customer_id,))
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def search_customers(search_text):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT customer_id, name, phone
        FROM customers
        WHERE name LIKE %s OR phone LIKE %s
        ORDER BY customer_id DESC
    """

    search_pattern = f"%{search_text}%"

    cursor.execute(query, (search_pattern, search_pattern))

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers