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

# ---------------- REPAIR FUNCTIONS ----------------

def add_repair(device_id, technician, cost, date_received):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO repairs
        (device_id, repair_status, technician, cost, date_received)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (device_id, "Pending", technician, cost, date_received)
    )

    connection.commit()

    repair_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return repair_id


def get_repairs():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            r.repair_id,
            r.device_id,
            c.name AS customer_name,
            d.brand,
            d.model,
            d.problem,
            r.repair_status,
            r.technician,
            r.cost,
            r.date_received,
            r.date_delivered
        FROM repairs r
        JOIN devices d
            ON r.device_id = d.device_id
        JOIN customers c
            ON d.customer_id = c.customer_id
        ORDER BY r.repair_id DESC
    """

    cursor.execute(query)

    repairs = cursor.fetchall()

    cursor.close()
    connection.close()

    return repairs


def update_repair(
    repair_id,
    repair_status,
    technician,
    cost,
    date_delivered=None
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE repairs
        SET repair_status = %s,
            technician = %s,
            cost = %s,
            date_delivered = %s
        WHERE repair_id = %s
    """

    cursor.execute(
        query,
        (
            repair_status,
            technician,
            cost,
            date_delivered,
            repair_id
        )
    )

    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def delete_repair(repair_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM repairs
        WHERE repair_id = %s
    """

    cursor.execute(query, (repair_id,))
    connection.commit()

    affected_rows = cursor.rowcount

    cursor.close()
    connection.close()

    return affected_rows


def search_repairs(search_text):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            r.repair_id,
            r.device_id,
            c.name AS customer_name,
            d.brand,
            d.model,
            r.repair_status,
            r.technician,
            r.cost,
            r.date_received,
            r.date_delivered
        FROM repairs r
        JOIN devices d
            ON r.device_id = d.device_id
        JOIN customers c
            ON d.customer_id = c.customer_id
        WHERE c.name LIKE %s
           OR d.brand LIKE %s
           OR d.model LIKE %s
           OR r.repair_status LIKE %s
           OR r.technician LIKE %s
        ORDER BY r.repair_id DESC
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

    repairs = cursor.fetchall()

    cursor.close()
    connection.close()

    return repairs

# ---------------- REPORT FUNCTIONS ----------------

def get_dashboard_stats():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    stats = {}

    cursor.execute("SELECT COUNT(*) AS total FROM customers")
    stats["total_customers"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM devices")
    stats["total_devices"] = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM repairs")
    stats["total_repairs"] = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repairs
        WHERE repair_status = 'Pending'
    """)
    stats["pending_repairs"] = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM repairs
        WHERE repair_status IN ('Completed', 'Delivered')
    """)
    stats["completed_repairs"] = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COALESCE(SUM(cost), 0) AS total
        FROM repairs
    """)
    stats["total_revenue"] = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return stats


def get_recent_repairs(limit=10):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            r.repair_id,
            c.name AS customer_name,
            d.brand,
            d.model,
            r.repair_status,
            r.cost,
            r.date_received
        FROM repairs r
        JOIN devices d
            ON r.device_id = d.device_id
        JOIN customers c
            ON d.customer_id = c.customer_id
        ORDER BY r.repair_id DESC
        LIMIT %s
    """

    cursor.execute(query, (limit,))

    repairs = cursor.fetchall()

    cursor.close()
    connection.close()

    return repairs