import customtkinter as ctk
from tkinter import ttk, messagebox

from database import (
    add_customer,
    get_customers,
    update_customer,
    delete_customer,
    search_customers
)


class CustomersPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.name_validation = (
            self.register(self.validate_name_input)
        )

        self.create_ui()
        self.load_customers()

    def create_ui(self):

        heading = ctk.CTkLabel(
            self,
            text="Customer Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        heading.pack(
            anchor="w",
            pady=(0, 20)
        )

        # ---------- FORM ----------

        form = ctk.CTkFrame(self)
        form.pack(
            fill="x",
            pady=(0, 15)
        )

        self.name_entry = ctk.CTkEntry(
            form,
            placeholder_text="Customer Name",
            validate="key",
            validatecommand=(
                self.name_validation,
                "%P"
            )
        )
        self.name_entry.pack(
            side="left",
            padx=10,
            pady=15,
            fill="x",
            expand=True
        )

        self.phone_entry = ctk.CTkEntry(
            form,
            placeholder_text="Phone Number",
            width=200
        )

        self.phone_entry.bind(
            "<KeyPress>",
            self.validate_phone_key
        )
        self.phone_entry.pack(
            side="left",
            padx=10,
            pady=15,
            fill="x",
            expand=True
        )

        ctk.CTkButton(
            form,
            text="Add Customer",
            command=self.add_customer
        ).pack(
            side="left",
            padx=10,
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
            placeholder_text="Search by name or phone"
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
            command=self.load_customers
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
            "Name",
            "Phone"
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
            width=80,
            anchor="center"
        )

        self.table.column(
            "Name",
            width=300
        )

        self.table.column(
            "Phone",
            width=200
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_customer
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
            command=self.edit_customer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            command=self.delete_customer
        ).pack(
            side="left",
            padx=5
        )

    def validate_name_input(self, value):

        return (
            value == ""
            or all(
                char.isalpha() or char.isspace()
                for char in value
            )
        )


    def validate_phone_key(self, event):

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

        current = self.phone_entry.get()

        if len(current) >= 10:
            return "break"

    # ---------- LOAD ----------

    def load_customers(self):

        for item in self.table.get_children():
            self.table.delete(item)

        customers = get_customers()

        for customer in customers:
            self.table.insert(
                "",
                "end",
                values=(
                    customer["customer_id"],
                    customer["name"],
                    customer["phone"]
                )
            )

    # ---------- ADD ----------

    def add_customer(self):

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please enter name and phone number."
            )
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain exactly 10 digits."
            )
            return

        add_customer(
            name,
            phone
        )

        messagebox.showinfo(
            "Success",
            "Customer added successfully."
        )

        self.name_entry.delete(
            0,
            "end"
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.load_customers()

    # ---------- SEARCH ----------

    def search(self):

        search_text = self.search_entry.get().strip()

        if not search_text:
            self.load_customers()
            return

        customers = search_customers(
            search_text
        )

        for item in self.table.get_children():
            self.table.delete(item)

        for customer in customers:
            self.table.insert(
                "",
                "end",
                values=(
                    customer["customer_id"],
                    customer["name"],
                    customer["phone"]
                )
            )

    # ---------- SELECT ----------

    def select_customer(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        self.name_entry.delete(
            0,
            "end"
        )

        self.name_entry.insert(
            0,
            values[1]
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.phone_entry.insert(
            0,
            values[2]
        )

    # ---------- EDIT ----------

    def edit_customer(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a customer."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        customer_id = values[0]

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Enter name and phone."
            )
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain exactly 10 digits."
            )
            return

        update_customer(
            customer_id,
            name,
            phone
        )

        messagebox.showinfo(
            "Success",
            "Customer updated successfully."
        )

        self.load_customers()

    # ---------- DELETE ----------

    def delete_customer(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a customer."
            )
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        customer_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this customer?"
        )

        if not confirm:
            return

        try:

            delete_customer(
                customer_id
            )

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully."
            )

            self.load_customers()

        except Exception as error:

            messagebox.showerror(
                "Delete Failed",
                f"Could not delete customer.\n\n{error}"
            )