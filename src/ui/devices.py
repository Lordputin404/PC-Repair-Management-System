import customtkinter as ctk
from tkinter import ttk, messagebox

from database import (
    get_customers,
    add_device,
    get_devices,
    update_device,
    delete_device,
    search_devices
)


class DevicesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.customer_map = {}

        self.create_ui()
        self.load_customers()
        self.load_devices()

    def create_ui(self):

        heading = ctk.CTkLabel(
            self,
            text="Device Management",
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

        self.customer_combo = ctk.CTkComboBox(
            form,
            values=["Select Customer"],
            width=220,
            state="readonly"
        )
        self.customer_combo.set("Select Customer")
        self.customer_combo.pack(
            side="left",
            padx=8,
            pady=15
        )

        self.brand_entry = ctk.CTkEntry(
            form,
            placeholder_text="Brand"
        )
        self.brand_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        self.model_entry = ctk.CTkEntry(
            form,
            placeholder_text="Model"
        )
        self.model_entry.pack(
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

        self.serial_entry = ctk.CTkEntry(
            form2,
            placeholder_text="Serial Number"
        )
        self.serial_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        self.problem_entry = ctk.CTkEntry(
            form2,
            placeholder_text="Problem Description"
        )
        self.problem_entry.pack(
            side="left",
            padx=8,
            pady=15,
            fill="x",
            expand=True
        )

        ctk.CTkButton(
            form2,
            text="Add Device",
            command=self.add_device
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
            placeholder_text="Search customer, brand, model, serial or problem"
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
            command=self.load_devices
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
            "Brand",
            "Model",
            "Serial No.",
            "Problem"
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

        self.table.column(
            "ID",
            width=60,
            anchor="center"
        )

        self.table.column(
            "Customer",
            width=150
        )

        self.table.column(
            "Brand",
            width=100
        )

        self.table.column(
            "Model",
            width=150
        )

        self.table.column(
            "Serial No.",
            width=150
        )

        self.table.column(
            "Problem",
            width=250
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_device
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
            command=self.edit_device
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            command=self.delete_device
        ).pack(
            side="left",
            padx=5
        )

    # ---------- CUSTOMERS ----------

    def load_customers(self):

        customers = get_customers()

        self.customer_map = {
            f"{customer['customer_id']} - {customer['name']}":
            customer["customer_id"]
            for customer in customers
        }

        values = list(self.customer_map.keys())

        if values:
            self.customer_combo.configure(
                values=["Select Customer"] + values
            )
        else:
            self.customer_combo.configure(
                values=["No Customers Available"]
            )

        self.customer_combo.set(
            "Select Customer"
            if values
            else "No Customers Available"
        )

    # ---------- LOAD DEVICES ----------

    def load_devices(self):

        for item in self.table.get_children():
            self.table.delete(item)

        devices = get_devices()

        for device in devices:
            self.table.insert(
                "",
                "end",
                values=(
                    device["device_id"],
                    device["customer_name"],
                    device["brand"],
                    device["model"],
                    device["serial_no"],
                    device["problem"]
                )
            )

    # ---------- ADD ----------

    def add_device(self):

        customer_text = self.customer_combo.get()

        if customer_text not in self.customer_map:
            messagebox.showwarning(
                "Select Customer",
                "Please select a valid customer."
            )
            return

        customer_id = self.customer_map[customer_text]

        brand = self.brand_entry.get().strip()
        model = self.model_entry.get().strip()
        serial_no = self.serial_entry.get().strip()
        problem = self.problem_entry.get().strip()

        if not brand or not model or not problem:
            messagebox.showwarning(
                "Missing Information",
                "Brand, model and problem are required."
            )
            return

        add_device(
            customer_id,
            brand,
            model,
            serial_no,
            problem
        )

        messagebox.showinfo(
            "Success",
            "Device added successfully."
        )

        self.clear_form()
        self.load_devices()

    # ---------- SELECT ----------

    def select_device(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        customer_name = values[1]

        for key in self.customer_map:

            if key.endswith(
                f"- {customer_name}"
            ):
                self.customer_combo.set(key)
                break

        self.brand_entry.delete(0, "end")
        self.brand_entry.insert(0, values[2])

        self.model_entry.delete(0, "end")
        self.model_entry.insert(0, values[3])

        self.serial_entry.delete(0, "end")
        self.serial_entry.insert(0, values[4])

        self.problem_entry.delete(0, "end")
        self.problem_entry.insert(0, values[5])

    # ---------- EDIT ----------

    def edit_device(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a device."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        device_id = values[0]

        customer_text = self.customer_combo.get()

        if customer_text not in self.customer_map:
            messagebox.showwarning(
                "Select Customer",
                "Please select a valid customer."
            )
            return

        customer_id = self.customer_map[customer_text]

        brand = self.brand_entry.get().strip()
        model = self.model_entry.get().strip()
        serial_no = self.serial_entry.get().strip()
        problem = self.problem_entry.get().strip()

        if not brand or not model or not problem:
            messagebox.showwarning(
                "Missing Information",
                "Brand, model and problem are required."
            )
            return

        update_device(
            device_id,
            customer_id,
            brand,
            model,
            serial_no,
            problem
        )

        messagebox.showinfo(
            "Success",
            "Device updated successfully."
        )

        self.load_devices()

    # ---------- DELETE ----------

    def delete_device(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a device."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        device_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this device?"
        )

        if not confirm:
            return

        try:

            delete_device(device_id)

            messagebox.showinfo(
                "Success",
                "Device deleted successfully."
            )

            self.load_devices()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                f"Could not delete device.\n\n{error}"
            )

    # ---------- CLEAR FORM ----------

    def clear_form(self):

        self.brand_entry.delete(
            0,
            "end"
        )

        self.model_entry.delete(
            0,
            "end"
        )

        self.serial_entry.delete(
            0,
            "end"
        )

        self.problem_entry.delete(
            0,
            "end"
        )

        if self.customer_map:
            self.customer_combo.set(
                "Select Customer"
            )

    # ---------- SEARCH ----------

    def search(self):

        search_text = self.search_entry.get().strip()

        if not search_text:
            self.load_devices()
            return

        devices = search_devices(
            search_text
        )

        for item in self.table.get_children():
            self.table.delete(item)

        for device in devices:

            self.table.insert(
                "",
                "end",
                values=(
                    device["device_id"],
                    device["customer_name"],
                    device["brand"],
                    device["model"],
                    device["serial_no"],
                    device["problem"]
                )
            )