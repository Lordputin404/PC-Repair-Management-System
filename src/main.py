import customtkinter as ctk
from tkinter import ttk, messagebox
from database import (
    get_dashboard_stats,
    add_customer,
    get_customers,
    update_customer,
    delete_customer,
    search_customers
)

class RepairManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PC Repair & Service Center")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_sidebar()

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        self.show_dashboard()

    # ---------------- SIDEBAR ----------------

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="PC REPAIR\nCENTER",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        title.pack(pady=(35, 40))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customers),
            ("Devices", self.show_devices),
            ("Repairs", self.show_repairs),
            ("Reports", self.show_reports)
        ]

        for text, command in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=42,
                corner_radius=8,
                command=command
            )
            button.pack(
                padx=20,
                pady=6,
                fill="x"
            )

    # ---------------- PAGE CLEAR ----------------

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_content()

        heading = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(
            anchor="w",
            pady=(0, 25)
        )

        try:
            stats = get_dashboard_stats()
        except Exception as error:
            error_label = ctk.CTkLabel(
                self.content,
                text=f"Database Error: {error}",
                text_color="red"
            )
            error_label.pack(anchor="w")
            return

        cards_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x")

        cards = [
            ("Customers", stats["total_customers"]),
            ("Devices", stats["total_devices"]),
            ("Repairs", stats["total_repairs"]),
            ("Completed", stats["completed_repairs"])
        ]

        for title, value in cards:
            card = ctk.CTkFrame(
                cards_frame,
                height=120
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=6
            )

            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(
                    size=32,
                    weight="bold"
                )
            )
            value_label.pack(pady=(25, 5))

            title_label = ctk.CTkLabel(
                card,
                text=title
            )
            title_label.pack()

        # Repair summary
        summary = ctk.CTkFrame(self.content)
        summary.pack(
            fill="x",
            pady=30,
            padx=6
        )

        pending_label = ctk.CTkLabel(
            summary,
            text=f"Pending Repairs: {stats['pending_repairs']}",
            font=ctk.CTkFont(size=18)
        )
        pending_label.pack(
            side="left",
            padx=30,
            pady=20
        )

        revenue_label = ctk.CTkLabel(
            summary,
            text=f"Total Repair Cost: ₹{stats['total_revenue']}",
            font=ctk.CTkFont(size=18)
        )
        revenue_label.pack(
            side="left",
            padx=30,
            pady=20
        )

    # ---------------- CUSTOMERS ----------------

    def show_customers(self):
        self.clear_content()

        heading = ctk.CTkLabel(
            self.content,
            text="Customer Management",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        heading.pack(anchor="w", pady=(0, 20))

        # ---------- FORM ----------

        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", pady=(0, 15))

        self.customer_name_entry = ctk.CTkEntry(
            form,
            placeholder_text="Customer Name"
        )
        self.customer_name_entry.pack(
            side="left",
            padx=10,
            pady=15,
            fill="x",
            expand=True
        )

        self.customer_phone_entry = ctk.CTkEntry(
            form,
            placeholder_text="Phone Number"
        )
        self.customer_phone_entry.pack(
            side="left",
            padx=10,
            pady=15,
            fill="x",
            expand=True
        )

        add_button = ctk.CTkButton(
            form,
            text="Add Customer",
            command=self.add_customer_gui
        )
        add_button.pack(
            side="left",
            padx=10,
            pady=15
        )

        # ---------- SEARCH ----------

        search_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", pady=(0, 10))

        self.customer_search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by name or phone"
        )
        self.customer_search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_customer_gui
        )
        search_button.pack(side="left")

        clear_search_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            width=80,
            command=self.load_customers
        )
        clear_search_button.pack(
            side="left",
            padx=(10, 0)
        )

        # ---------- TABLE ----------

        table_frame = ctk.CTkFrame(self.content)
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Name",
            "Phone"
        )

        self.customer_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.customer_table.heading(
                column,
                text=column
            )

        self.customer_table.column(
            "ID",
            width=80,
            anchor="center"
        )

        self.customer_table.column(
            "Name",
            width=300
        )

        self.customer_table.column(
            "Phone",
            width=200
        )

        self.customer_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.customer_table.bind(
            "<<TreeviewSelect>>",
            self.select_customer
        )

        # ---------- ACTION BUTTONS ----------

        action_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        action_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        edit_button = ctk.CTkButton(
            action_frame,
            text="Edit Selected",
            command=self.edit_customer_gui
        )
        edit_button.pack(
            side="left",
            padx=5
        )

        delete_button = ctk.CTkButton(
            action_frame,
            text="Delete Selected",
            command=self.delete_customer_gui
        )
        delete_button.pack(
            side="left",
            padx=5
        )

        self.load_customers()

    def load_customers(self):
        for item in self.customer_table.get_children():
            self.customer_table.delete(item)

        customers = get_customers()

        for customer in customers:
            self.customer_table.insert(
                "",
                "end",
                values=(
                    customer["customer_id"],
                    customer["name"],
                    customer["phone"]
                )
            )


    def add_customer_gui(self):
        name = self.customer_name_entry.get().strip()
        phone = self.customer_phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please enter name and phone number."
            )
            return

        add_customer(name, phone)

        messagebox.showinfo(
            "Success",
            "Customer added successfully."
        )

        self.customer_name_entry.delete(0, "end")
        self.customer_phone_entry.delete(0, "end")

        self.load_customers()


    def search_customer_gui(self):
        search_text = self.customer_search_entry.get().strip()

        if not search_text:
            self.load_customers()
            return

        customers = search_customers(search_text)

        for item in self.customer_table.get_children():
            self.customer_table.delete(item)

        for customer in customers:
            self.customer_table.insert(
                "",
                "end",
                values=(
                    customer["customer_id"],
                    customer["name"],
                    customer["phone"]
                )
            )


    def edit_customer_gui(self):
        selected = self.customer_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a customer."
            )
            return

        values = self.customer_table.item(
            selected[0],
            "values"
        )

        customer_id = values[0]

        name = self.customer_name_entry.get().strip()
        phone = self.customer_phone_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Enter updated name and phone."
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


    def delete_customer_gui(self):
        selected = self.customer_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a customer."
            )
            return

        values = self.customer_table.item(
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
            delete_customer(customer_id)

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

    def select_customer(self, event=None):
        selected = self.customer_table.selection()

        if not selected:
            return

        values = self.customer_table.item(
            selected[0],
            "values"
        )

        self.customer_name_entry.delete(0, "end")
        self.customer_name_entry.insert(0, values[1])

        self.customer_phone_entry.delete(0, "end")
        self.customer_phone_entry.insert(0, values[2])

    # ---------------- DEVICES ----------------

    def show_devices(self):
        self.clear_content()

        heading = ctk.CTkLabel(
            self.content,
            text="Devices",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(anchor="w")

        label = ctk.CTkLabel(
            self.content,
            text="Device Management"
        )
        label.pack(anchor="w", pady=20)

    # ---------------- REPAIRS ----------------

    def show_repairs(self):
        self.clear_content()

        heading = ctk.CTkLabel(
            self.content,
            text="Repairs",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(anchor="w")

        label = ctk.CTkLabel(
            self.content,
            text="Repair Management"
        )
        label.pack(anchor="w", pady=20)

    # ---------------- REPORTS ----------------

    def show_reports(self):
        self.clear_content()

        heading = ctk.CTkLabel(
            self.content,
            text="Reports",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(anchor="w")

        label = ctk.CTkLabel(
            self.content,
            text="Reports & CSV Export"
        )
        label.pack(anchor="w", pady=20)


if __name__ == "__main__":
    app = RepairManagementApp()
    app.mainloop()