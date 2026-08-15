import customtkinter as ctk
from database import get_dashboard_stats


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.create_ui()
        self.load_dashboard()

    def create_ui(self):
        heading = ctk.CTkLabel(
            self,
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

        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.cards_frame.pack(
            fill="x"
        )

        self.card_values = {}

        cards = [
            ("Customers", "total_customers"),
            ("Devices", "total_devices"),
            ("Repairs", "total_repairs"),
            ("Completed", "completed_repairs")
        ]

        for title, key in cards:

            card = ctk.CTkFrame(
                self.cards_frame,
                height=120
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=6
            )

            value = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=32,
                    weight="bold"
                )
            )

            value.pack(
                pady=(25, 5)
            )

            label = ctk.CTkLabel(
                card,
                text=title
            )

            label.pack()

            self.card_values[key] = value

        self.summary = ctk.CTkFrame(
            self
        )

        self.summary.pack(
            fill="x",
            pady=30,
            padx=6
        )

        self.pending_label = ctk.CTkLabel(
            self.summary,
            text="Pending Repairs: 0",
            font=ctk.CTkFont(size=18)
        )

        self.pending_label.pack(
            side="left",
            padx=30,
            pady=20
        )

        self.revenue_label = ctk.CTkLabel(
            self.summary,
            text="Total Repair Cost: ₹0",
            font=ctk.CTkFont(size=18)
        )

        self.revenue_label.pack(
            side="left",
            padx=30,
            pady=20
        )

    def load_dashboard(self):

        try:
            stats = get_dashboard_stats()

            for key, label in self.card_values.items():
                label.configure(
                    text=str(stats[key])
                )

            self.pending_label.configure(
                text=f"Pending Repairs: {stats['pending_repairs']}"
            )

            self.revenue_label.configure(
                text=f"Total Repair Cost: ₹{stats['total_revenue']}"
            )

        except Exception as error:

            self.pending_label.configure(
                text=f"Database Error: {error}"
            )