import customtkinter as ctk
from tkinter import ttk

from database import (
    get_dashboard_stats,
    get_recent_repairs
)


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.create_ui()
        self.load_dashboard()

    def create_ui(self):

        # ---------- HEADER ----------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            pady=(0, 20)
        )

        heading = ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        heading.pack(
            side="left"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="PC Repair & Service Center",
            text_color="gray"
        )
        subtitle.pack(
            side="left",
            padx=15,
            pady=8
        )

        # ---------- STAT CARDS ----------

        cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        cards_frame.pack(
            fill="x",
            pady=(0, 20)
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
                cards_frame,
                height=125,
                corner_radius=12
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

            card.pack_propagate(False)

            value = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(
                    size=30,
                    weight="bold"
                )
            )

            value.pack(
                anchor="w",
                padx=20,
                pady=(22, 2)
            )

            label = ctk.CTkLabel(
                card,
                text=title,
                text_color="gray"
            )

            label.pack(
                anchor="w",
                padx=20
            )

            self.card_values[key] = value

        # ---------- LOWER AREA ----------

        lower_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        lower_frame.pack(
            fill="both",
            expand=True
        )

        # ---------- RECENT REPAIRS ----------

        recent_frame = ctk.CTkFrame(
            lower_frame,
            corner_radius=12
        )
        recent_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        recent_title = ctk.CTkLabel(
            recent_frame,
            text="Recent Repairs",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        recent_title.pack(
            anchor="w",
            padx=18,
            pady=(18, 12)
        )

        table_container = ctk.CTkFrame(
            recent_frame,
            fg_color="transparent"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        columns = (
            "Customer",
            "Device",
            "Status",
            "Cost"
        )

        self.recent_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.recent_table.heading(
                column,
                text=column
            )

        self.recent_table.column(
            "Customer",
            width=130
        )

        self.recent_table.column(
            "Device",
            width=150
        )

        self.recent_table.column(
            "Status",
            width=100
        )

        self.recent_table.column(
            "Cost",
            width=80
        )

        self.recent_table.pack(
            fill="both",
            expand=True
        )

        # ---------- SUMMARY ----------

        summary_frame = ctk.CTkFrame(
            lower_frame,
            corner_radius=12
        )

        summary_frame.pack(
            side="right",
            fill="both",
            expand=False,
            padx=(8, 0)
        )

        summary_frame.configure(
            width=280
        )
        summary_frame.pack_propagate(False)

        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Repair Summary",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        summary_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 25)
        )

        self.pending_label = self.create_summary_row(
            summary_frame,
            "Pending Repairs"
        )

        self.completed_label = self.create_summary_row(
            summary_frame,
            "Completed"
        )

        self.revenue_label = self.create_summary_row(
            summary_frame,
            "Total Cost"
        )

    def create_summary_row(self, parent, title):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            text_color="gray"
        )

        label.pack(
            side="left"
        )

        value = ctk.CTkLabel(
            frame,
            text="0",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        value.pack(
            side="right"
        )

        return value

    def load_dashboard(self):

        try:

            stats = get_dashboard_stats()

            for key, label in self.card_values.items():

                label.configure(
                    text=str(
                        stats[key]
                    )
                )

            self.pending_label.configure(
                text=str(
                    stats["pending_repairs"]
                )
            )

            self.completed_label.configure(
                text=str(
                    stats["completed_repairs"]
                )
            )

            self.revenue_label.configure(
                text=f"₹{stats['total_revenue']}"
            )

            self.load_recent_repairs()

        except Exception as error:

            self.pending_label.configure(
                text="Error"
            )

            print(
                f"Dashboard error: {error}"
            )

    def load_recent_repairs(self):

        for item in self.recent_table.get_children():

            self.recent_table.delete(
                item
            )

        repairs = get_recent_repairs(8)

        for repair in repairs:

            device = (
                f"{repair['brand']} "
                f"{repair['model']}"
            )

            self.recent_table.insert(
                "",
                "end",
                values=(
                    repair["customer_name"],
                    device,
                    repair["repair_status"],
                    f"₹{repair['cost']}"
                )
            )