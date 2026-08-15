import customtkinter as ctk

from tkinter import ttk
from ui.dashboard import DashboardPage
from ui.customers import CustomersPage
from ui.devices import DevicesPage
from ui.repairs import RepairsPage
from ui.reports import ReportsPage


class RepairManagementApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("PC Repair & Service Center")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_theme = "Dark"
        self.setup_styles()
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

        self.show_page(DashboardPage)

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("default")

        if self.current_theme == "Light":
            background = "#ffffff"
            foreground = "#222222"
            heading_background = "#e5e5e5"
            selected_background = "#3a7ebf"

        else:
            background = "#1f1f1f"
            foreground = "#ffffff"
            heading_background = "#2b2b2b"
            selected_background = "#1f6aa5"

        style.configure(
            "Treeview",
            background=background,
            foreground=foreground,
            fieldbackground=background,
            rowheight=35,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=heading_background,
            foreground=foreground,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", selected_background)
            ],
            foreground=[
                ("selected", "white")
            ]
        )

    # ---------- SIDEBAR ----------

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

        title.pack(
            pady=(35, 40)
        )

        buttons = [
            ("Dashboard", DashboardPage),
            ("Customers", CustomersPage),
            ("Devices", DevicesPage),
            ("Repairs", RepairsPage),
            ("Reports", ReportsPage)
        ]

        for text, page in buttons:

            ctk.CTkButton(
                self.sidebar,
                text=text,
                height=42,
                corner_radius=8,
                command=lambda p=page: self.show_page(p)
            ).pack(
                padx=20,
                pady=6,
                fill="x"
            )

        # ---------- THEME TOGGLE ----------

        self.theme_combo = ctk.CTkComboBox(
            self.sidebar,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            state="readonly",
            command=self.change_theme
        )

        self.theme_combo.set("Dark")

        self.theme_combo.pack(
            side="bottom",
            padx=20,
            pady=20,
            fill="x"
        )

    # ---------- THEME ----------

    def change_theme(self, choice):

        if choice == "Dark":
            ctk.set_appearance_mode("dark")

        elif choice == "Light":
            ctk.set_appearance_mode("light")

        else:
            ctk.set_appearance_mode("system")

        self.current_theme = choice
        self.setup_styles()

    # ---------- PAGE NAVIGATION ----------

    def show_page(self, page_class):

        for widget in self.content.winfo_children():
            widget.destroy()

        page = page_class(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":

    app = RepairManagementApp()
    app.mainloop()