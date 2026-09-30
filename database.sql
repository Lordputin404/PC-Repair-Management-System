CREATE DATABASE IF NOT EXISTS pc_repair_system;

USE pc_repair_system;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL
);

-- Devices table
CREATE TABLE IF NOT EXISTS devices (
    device_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    serial_no VARCHAR(100),
    problem TEXT NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Repairs table
CREATE TABLE IF NOT EXISTS repairs (
    repair_id INT AUTO_INCREMENT PRIMARY KEY,
    device_id INT NOT NULL,
    repair_status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    technician VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2) DEFAULT 0.00,
    date_received DATE NOT NULL,
    date_delivered DATE NULL,

    FOREIGN KEY (device_id)
        REFERENCES devices(device_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);