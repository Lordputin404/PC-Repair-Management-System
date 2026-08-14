import csv

from database import (
    get_customers,
    get_devices,
    get_repairs
)


def export_customers(filename="customers.csv"):
    customers = get_customers()

    if not customers:
        return False

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=customers[0].keys()
        )

        writer.writeheader()
        writer.writerows(customers)

    return True


def export_devices(filename="devices.csv"):
    devices = get_devices()

    if not devices:
        return False

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=devices[0].keys()
        )

        writer.writeheader()
        writer.writerows(devices)

    return True


def export_repairs(filename="repairs.csv"):
    repairs = get_repairs()

    if not repairs:
        return False

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=repairs[0].keys()
        )

        writer.writeheader()
        writer.writerows(repairs)

    return True