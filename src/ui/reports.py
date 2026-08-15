import customtkinter as ctk
from tkinter import messagebox

from database import get_dashboard_stats
from export import (
    export_customers,
    export_devices,
    export_repairs
)


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.create_ui()
        self.load_reports()

    def create_ui(self):

        heading = ctk.CTkLabel(
            self,
            text="Reports & Export",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        heading.pack(
            anchor="w",
            pady=(0, 20)
        )

        # ---------- STATISTICS ----------

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats_frame.pack(
            fill="x",
            pady=(0, 25)
        )

        self.total_customers = self.create_stat_card(
            stats_frame,
            "Total Customers"
        )

        self.total_devices = self.create_stat_card(
            stats_frame,
            "Total Devices"
        )

        self.total_repairs = self.create_stat_card(
            stats_frame,
            "Total Repairs"
        )

        self.total_cost = self.create_stat_card(
            stats_frame,
            "Total Repair Cost"
        )

        # ---------- REPAIR STATUS ----------

        status_frame = ctk.CTkFrame(self)
        status_frame.pack(
            fill="x",
            pady=(0, 25)
        )

        self.pending_label = ctk.CTkLabel(
            status_frame,
            text="Pending Repairs: 0",
            font=ctk.CTkFont(size=18)
        )
        self.pending_label.pack(
            side="left",
            padx=30,
            pady=20
        )

        self.completed_label = ctk.CTkLabel(
            status_frame,
            text="Completed Repairs: 0",
            font=ctk.CTkFont(size=18)
        )
        self.completed_label.pack(
            side="left",
            padx=30,
            pady=20
        )

        # ---------- EXPORT ----------

        export_heading = ctk.CTkLabel(
            self,
            text="Export Data",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )
        export_heading.pack(
            anchor="w",
            pady=(0, 10)
        )

        export_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        export_frame.pack(
            fill="x"
        )

        ctk.CTkButton(
            export_frame,
            text="Export Customers CSV",
            command=self.export_customers
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            export_frame,
            text="Export Devices CSV",
            command=self.export_devices
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            export_frame,
            text="Export Repairs CSV",
            command=self.export_repairs
        ).pack(
            side="left",
            padx=5
        )

        # ---------- REFRESH ----------

        ctk.CTkButton(
            self,
            text="Refresh Reports",
            command=self.load_reports
        ).pack(
            anchor="w",
            pady=30
        )

    def create_stat_card(self, parent, title):

        card = ctk.CTkFrame(
            parent,
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
                size=28,
                weight="bold"
            )
        )
        value.pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            card,
            text=title
        ).pack()

        return value

    def load_reports(self):

        try:

            stats = get_dashboard_stats()

            self.total_customers.configure(
                text=str(
                    stats["total_customers"]
                )
            )

            self.total_devices.configure(
                text=str(
                    stats["total_devices"]
                )
            )

            self.total_repairs.configure(
                text=str(
                    stats["total_repairs"]
                )
            )

            self.total_cost.configure(
                text=f"₹{stats['total_revenue']}"
            )

            self.pending_label.configure(
                text=f"Pending Repairs: "
                     f"{stats['pending_repairs']}"
            )

            self.completed_label.configure(
                text=f"Completed Repairs: "
                     f"{stats['completed_repairs']}"
            )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                f"Could not load reports.\n\n{error}"
            )

    def export_customers(self):

        if export_customers():
            messagebox.showinfo(
                "Export Successful",
                "Customers exported to customers.csv"
            )
        else:
            messagebox.showwarning(
                "No Data",
                "No customer data available."
            )

    def export_devices(self):

        if export_devices():
            messagebox.showinfo(
                "Export Successful",
                "Devices exported to devices.csv"
            )
        else:
            messagebox.showwarning(
                "No Data",
                "No device data available."
            )

    def export_repairs(self):

        if export_repairs():
            messagebox.showinfo(
                "Export Successful",
                "Repairs exported to repairs.csv"
            )
        else:
            messagebox.showwarning(
                "No Data",
                "No repair data available."
            )