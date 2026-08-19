import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date
from datetime import datetime

from database import (
    get_devices,
    add_repair,
    get_repairs,
    update_repair,
    delete_repair,
    search_repairs
)


class RepairsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.device_map = {}

        self.technician_validation = self.register(
            self.validate_technician_input
        )

        self.create_ui()
        self.load_devices()
        self.load_repairs()

    def create_ui(self):

        heading = ctk.CTkLabel(
            self,
            text="Repair Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        heading.pack(
            anchor="w",
            pady=(0, 20)
        )

        # ---------- FIRST ROW ----------

        form = ctk.CTkFrame(self)
        form.pack(
            fill="x",
            pady=(0, 15)
        )

        self.device_combo = ctk.CTkComboBox(
            form,
            values=["Select Device"],
            width=260,
            state="readonly"
        )
        self.device_combo.set("Select Device")
        self.device_combo.pack(
            side="left",
            padx=8,
            pady=15
        )

        self.technician_entry = ctk.CTkEntry(
            form,
            placeholder_text="Technician",
            validate="key",
            validatecommand=(
                self.technician_validation,
                "%P"
            )
        )
        self.technician_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        self.cost_entry = ctk.CTkEntry(
            form,
            placeholder_text="Repair Cost"
        )

        self.cost_entry.bind(
            "<KeyPress>",
            self.validate_cost_key
        )
        self.cost_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        # ---------- SECOND ROW ----------

        form2 = ctk.CTkFrame(self)
        form2.pack(
            fill="x",
            pady=(0, 15)
        )

        self.date_received_entry = ctk.CTkEntry(
            form2,
            placeholder_text="Date Received (YYYY-MM-DD)"
        )

        self.date_received_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        self.date_received_entry.bind(
            "<KeyPress>",
            self.validate_date_key
        )
        
        self.status_combo = ctk.CTkComboBox(
            form2,
            values=[
                "Pending",
                "In Progress",
                "Completed",
                "Delivered"
            ],
            state="readonly"
        )
        self.status_combo.set("Pending")
        self.status_combo.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        ctk.CTkButton(
            form2,
            text="Add Repair",
            command=self.add_repair
        ).pack(
            side="left",
            padx=8,
            pady=15
        )

        # ---------- SEARCH ----------

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        search_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search customer, device, status or technician"
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search
        ).pack(side="left")

        ctk.CTkButton(
            search_frame,
            text="Clear",
            width=80,
            command=self.load_repairs
        ).pack(
            side="left",
            padx=(10, 0)
        )

        # ---------- TABLE ----------

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Customer",
            "Device",
            "Status",
            "Technician",
            "Cost",
            "Received",
            "Delivered"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.table.heading(
                column,
                text=column
            )

        widths = {
            "ID": 55,
            "Customer": 130,
            "Device": 160,
            "Status": 110,
            "Technician": 120,
            "Cost": 90,
            "Received": 100,
            "Delivered": 100
        }

        for column, width in widths.items():
            self.table.column(
                column,
                width=width
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_repair
        )

        # ---------- ACTIONS ----------

        action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        action_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        ctk.CTkButton(
            action_frame,
            text="Edit Selected",
            command=self.edit_repair
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            command=self.delete_repair
        ).pack(
            side="left",
            padx=5
        )

    def validate_technician_input(self, value):

        return (
            value == ""
            or all(
                char.isalpha() or char.isspace()
                for char in value
            )
        )

    def validate_cost_key(self, event):

        if event.keysym in (
            "BackSpace",
            "Delete",
            "Left",
            "Right",
            "Home",
            "End",
            "Tab"
        ):
            return

        if not (
            event.char.isdigit()
            or event.char == "."
        ):
            return "break"

        current = self.cost_entry.get()

        if event.char == "." and "." in current:
            return "break"

    def validate_date_key(self, event):

        if event.keysym in (
            "BackSpace",
            "Delete",
            "Left",
            "Right",
            "Home",
            "End",
            "Tab"
        ):
            return

        if not event.char.isdigit():
            return "break"

        current = self.date_received_entry.get()

        # Maximum 8 digits + 2 hyphens
        if len(current) >= 10:
            return "break"

        # YYYY-
        if len(current) == 4:
            self.date_received_entry.insert("end", "-")

        # YYYY-MM-
        elif len(current) == 7:
            self.date_received_entry.insert("end", "-")

    # ---------- DEVICES ----------

    def load_devices(self):

        devices = get_devices()

        self.device_map = {
            f"{device['device_id']} - "
            f"{device['customer_name']} - "
            f"{device['brand']} {device['model']}":
            device["device_id"]
            for device in devices
        }

        values = list(self.device_map.keys())

        if values:
            self.device_combo.configure(
                values=["Select Device"] + values
            )
        else:
            self.device_combo.configure(
                values=["No Devices Available"]
            )

        self.device_combo.set(
            "Select Device"
            if values
            else "No Devices Available"
        )

    # ---------- LOAD REPAIRS ----------

    def load_repairs(self):

        for item in self.table.get_children():
            self.table.delete(item)

        repairs = get_repairs()

        for repair in repairs:

            device = (
                f"{repair['brand']} "
                f"{repair['model']}"
            )

            self.table.insert(
                "",
                "end",
                values=(
                    repair["repair_id"],
                    repair["customer_name"],
                    device,
                    repair["repair_status"],
                    repair["technician"],
                    repair["cost"],
                    repair["date_received"],
                    repair["date_delivered"] or ""
                )
            )

    # ---------- ADD ----------

    def add_repair(self):

        device_text = self.device_combo.get()

        if device_text not in self.device_map:
            messagebox.showwarning(
                "Select Device",
                "Please select a valid device."
            )
            return

        device_id = self.device_map[device_text]

        technician = (
            self.technician_entry
            .get()
            .strip()
        )

        cost_text = (
            self.cost_entry
            .get()
            .strip()
        )

        date_received = self.date_received_entry.get().strip()

        if not date_received:
            date_received = str(date.today())
            self.date_received_entry.insert(
                0,
                date_received
            )
        else:
            try:
                datetime.strptime(
                    date_received,
                    "%Y-%m-%d"
                )
            except ValueError:
                messagebox.showwarning(
                    "Invalid Date",
                    "Please enter date in YYYY-MM-DD format."
                )
                return

        if not date_received:
            date_received = str(date.today())
            self.date_received_entry.insert(
                0,
                date_received
            )

        if not technician:
            messagebox.showwarning(
                "Missing Information",
                "Please enter technician name."
            )
            return

        try:
            cost = float(cost_text or 0)
        except ValueError:
            messagebox.showwarning(
                "Invalid Cost",
                "Please enter a valid repair cost."
            )
            return

        add_repair(
            device_id,
            technician,
            cost,
            date_received
        )

        messagebox.showinfo(
            "Success",
            "Repair added successfully."
        )

        self.clear_form()
        self.load_repairs()

    # ---------- SELECT ----------

    def select_repair(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        status = values[3]

        if status in (
            "Pending",
            "In Progress",
            "Completed",
            "Delivered"
        ):
            self.status_combo.set(status)

        self.technician_entry.delete(
            0,
            "end"
        )
        self.technician_entry.insert(
            0,
            values[4]
        )

        self.cost_entry.delete(
            0,
            "end"
        )
        self.cost_entry.insert(
            0,
            values[5]
        )

        self.date_received_entry.delete(
            0,
            "end"
        )
        self.date_received_entry.insert(
            0,
            values[6]
        )

    # ---------- EDIT ----------

    def edit_repair(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a repair."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        repair_id = values[0]

        status = self.status_combo.get()

        technician = (
            self.technician_entry
            .get()
            .strip()
        )

        cost_text = (
            self.cost_entry
            .get()
            .strip()
        )

        try:
            cost = float(cost_text or 0)
        except ValueError:
            messagebox.showwarning(
                "Invalid Cost",
                "Please enter a valid repair cost."
            )
            return

        if status == "Delivered":
            date_delivered = str(date.today())
        else:
            date_delivered = None

        update_repair(
            repair_id,
            status,
            technician,
            cost,
            date_delivered
        )

        messagebox.showinfo(
            "Success",
            "Repair updated successfully."
        )

        self.load_repairs()

    # ---------- DELETE ----------

    def delete_repair(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a repair."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        repair_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this repair?"
        )

        if not confirm:
            return

        try:

            delete_repair(
                repair_id
            )

            messagebox.showinfo(
                "Success",
                "Repair deleted successfully."
            )

            self.load_repairs()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                f"Could not delete repair.\n\n{error}"
            )

    # ---------- SEARCH ----------

    def search(self):

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        if not search_text:
            self.load_repairs()
            return

        repairs = search_repairs(
            search_text
        )

        for item in self.table.get_children():
            self.table.delete(item)

        for repair in repairs:

            device = (
                f"{repair['brand']} "
                f"{repair['model']}"
            )

            self.table.insert(
                "",
                "end",
                values=(
                    repair["repair_id"],
                    repair["customer_name"],
                    device,
                    repair["repair_status"],
                    repair["technician"],
                    repair["cost"],
                    repair["date_received"],
                    repair["date_delivered"] or ""
                )
            )

    # ---------- CLEAR ----------

    def clear_form(self):

        self.device_combo.set(
            "Select Device"
            if self.device_map
            else "No Devices Available"
        )

        self.technician_entry.delete(
            0,
            "end"
        )

        self.cost_entry.delete(
            0,
            "end"
        )

        self.date_received_entry.delete(
            0,
            "end"
        )

        self.status_combo.set(
            "Pending"
        )