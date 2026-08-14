import customtkinter as ctk
from database import get_dashboard_stats

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
            text="Customers",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(anchor="w")

        label = ctk.CTkLabel(
            self.content,
            text="Customer Management"
        )
        label.pack(anchor="w", pady=20)

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