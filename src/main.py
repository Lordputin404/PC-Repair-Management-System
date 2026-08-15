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

        self.show_page(
            DashboardPage,
            "Dashboard"
        )

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

        # ---------- LOGO / TITLE ----------

        title = ctk.CTkLabel(
            self.sidebar,
            text="PC REPAIR\nCENTER",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.pack(
            pady=(35, 35)
        )

        self.nav_buttons = {}

        # ---------- MAIN ----------

        main_label = ctk.CTkLabel(
            self.sidebar,
            text="MAIN",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            anchor="w"
        )

        main_label.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.add_nav_button(
            "⌂  Dashboard",
            DashboardPage,
            "Dashboard"
        )

        # ---------- MANAGEMENT ----------

        management_label = ctk.CTkLabel(
            self.sidebar,
            text="MANAGEMENT",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            anchor="w"
        )

        management_label.pack(
            fill="x",
            padx=20,
            pady=(20, 8)
        )

        self.add_nav_button(
            "♟  Customers",
            CustomersPage,
            "Customers"
        )

        self.add_nav_button(
            "▣  Devices",
            DevicesPage,
            "Devices"
        )

        self.add_nav_button(
            "⚒  Repairs",
            RepairsPage,
            "Repairs"
        )

        # ---------- REPORTS ----------

        reports_label = ctk.CTkLabel(
            self.sidebar,
            text="REPORTS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            anchor="w"
        )

        reports_label.pack(
            fill="x",
            padx=20,
            pady=(20, 8)
        )

        self.add_nav_button(
            "▤  Reports",
            ReportsPage,
            "Reports"
        )

        # ---------- THEME ----------

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

    def add_nav_button(self, text, page_class, page_name):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            command=lambda: self.show_page(
                page_class,
                page_name
            )
        )

        button.pack(
            padx=12,
            pady=3,
            fill="x"
        )

        self.nav_buttons[page_name] = button

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

    def show_page(self, page_class, page_name):

        for widget in self.content.winfo_children():
            widget.destroy()

        for name, button in self.nav_buttons.items():

            if name == page_name:
                button.configure(
                    fg_color=("#1f6aa5", "#144870"),
                    text_color="white"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=("#222222", "#ffffff")
                )

        page = page_class(self.content)

        page.pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":

    app = RepairManagementApp()
    app.mainloop()