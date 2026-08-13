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

# ---------------- DEVICE FUNCTIONS ----------------

def add_device(customer_id, brand, model, serial_no, problem):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO devices
        (customer_id, brand, model, serial_no, problem)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (customer_id, brand, model, serial_no, problem)
    )

    connection.commit()

    device_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return device_id


def get_devices():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            d.device_id,
            d.customer_id,
            c.name AS customer_name,
            d.brand,
            d.model,
            d.serial_no,
            d.problem
        FROM devices d
        JOIN customers c
            ON d.customer_id = c.customer_id
        ORDER BY d.device_id DESC
    """

    cursor.execute(query)

    devices = cursor.fetchall()

    cursor.close()
    connection.close()

    return devices


def update_device(
    device_id,
    customer_id,
    brand,
    model,
    serial_no,
    problem
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE devices
        SET customer_id = %s,
            brand = %s,
            model = %s,
            serial_no = %s,
            problem = %s
        WHERE device_id = %s
    """

    cursor.execute(
        query,
        (
            customer_id,
            brand,
            model,
            serial_no,
            problem,
            device_id
        )
    )

    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def delete_device(device_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM devices
        WHERE device_id = %s
    """

    cursor.execute(query, (device_id,))
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def search_devices(search_text):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            d.device_id,
            d.customer_id,
            c.name AS customer_name,
            d.brand,
            d.model,
            d.serial_no,
            d.problem
        FROM devices d
        JOIN customers c
            ON d.customer_id = c.customer_id
        WHERE c.name LIKE %s
           OR d.brand LIKE %s
           OR d.model LIKE %s
           OR d.serial_no LIKE %s
           OR d.problem LIKE %s
        ORDER BY d.device_id DESC
    """

    search_pattern = f"%{search_text}%"

    cursor.execute(
        query,
        (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )
    )

    devices = cursor.fetchall()

    cursor.close()
    connection.close()

    return devices