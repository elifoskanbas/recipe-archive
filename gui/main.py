import customtkinter as ctk

import dashboard
import add_recipe
import manage_recipes
import settings
from texts import texts

import database


# -----------------------------
# THEME CONFIG
# -----------------------------
THEME = {
    "light": {
        "sidebar": "#FFF4E6",   
        "button": "#FF8C00",    
        "hover": "#FF7000",   
        "text": "#FFFFFF",
        "label":  "#000000" 
    },
    "dark": {
        "sidebar": "#3A3735",   
        "button": "#FF8C00",    
        "hover": "#FF7000",     
        "text": "#FFF7ED",   
        "label":  "#F8F8F8"  
    }
}


# -----------------------------
# APP
# -----------------------------
class CookBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CookBook")
        self.root.geometry("1200x650")

        # Language
        self.current_lang = settings.get_lang()

        # CustomTkinter base setup
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.current_theme = "light"

        # DB init
        database.setup_database()

        # UI
        self.create_ui()

        # First screen
        self.show_dashboard()

    # -----------------------------
    # UI SETUP
    # -----------------------------
    def create_ui(self):
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(
            self.root,
            width=220,
            corner_radius=0,
            fg_color=THEME[self.current_theme]["sidebar"]
        )
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Main content
        self.main_content_frame = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color="transparent"
        )
        self.main_content_frame.pack(side="right", fill="both", expand=True)

        self.create_menu_buttons()

    # -----------------------------
    # SIDEBAR
    # -----------------------------
    def create_menu_buttons(self):
        # Clear sidebar
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        # App title
        ctk.CTkLabel(
            self.sidebar_frame,
            text="🍳 CookBook",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color= "#000000" 
        ).pack(pady=(25, 35))

        # Menu items
        menu_items = [
            (texts[self.current_lang]["menu_dashboard"], "Dashboard"),
            (texts[self.current_lang]["menu_add_recipe"], "Add Recipe"),
            (texts[self.current_lang]["menu_manage_recipes"], "Manage Recipes"),
            (texts[self.current_lang]["menu_settings"], "Settings"),
        ]


        for text, action in menu_items:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=lambda a=action: self.menu_click(a),
                height=42,
                corner_radius=10,
                font=ctk.CTkFont(size=14),
                fg_color=THEME[self.current_theme]["button"],
                hover_color=THEME[self.current_theme]["hover"],
                text_color=THEME[self.current_theme]["text"]
            )
            btn.pack(fill="x", padx=18, pady=6)

        # Divider
        ctk.CTkFrame(
            self.sidebar_frame,
            height=1,
            fg_color="#475569"
        ).pack(fill="x", padx=18, pady=20)

        # Theme toggle
       
        ctk.CTkButton(
            self.sidebar_frame,
            text=texts[self.current_lang]["theme_label"],
            command=self.toggle_theme,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(size=14),
            fg_color=THEME[self.current_theme]["button"],
            hover_color=THEME[self.current_theme]["hover"],
            text_color=THEME[self.current_theme]["text"]
        ).pack(fill="x", padx=18, pady=6)

    # -----------------------------
    # NAVIGATION
    # -----------------------------
    def menu_click(self, action):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        if action == "Dashboard":
            self.show_dashboard()
        elif action == "Add Recipe":
            self.show_add_recipe()
        elif action == "Manage Recipes":
            self.show_manage_recipes()
        elif action == "Settings":
            self.show_settings()

    # -----------------------------
    # SCREENS
    # -----------------------------
    def show_dashboard(self):
        dashboard.show_dashboard(self.main_content_frame, self.current_lang)

    def show_add_recipe(self):
        add_recipe.show_add_recipe_screen(self.main_content_frame, self.current_lang)

    def show_manage_recipes(self):
        manage_recipes.show_manage_recipe_screen(self.main_content_frame, self.current_lang)

    def show_settings(self):
        settings.show_settings(
            self.main_content_frame,
            self.current_lang,
            on_language_change=self.on_language_change
        )

    # -----------------------------
    # LANGUAGE
    # -----------------------------
    def on_language_change(self, new_lang):
        self.current_lang = new_lang
        self.create_menu_buttons()
        self.show_dashboard()

    # -----------------------------
    # THEME
    # -----------------------------
    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            ctk.set_appearance_mode("dark")
        else:
            self.current_theme = "light"
            ctk.set_appearance_mode("light")

        theme = THEME[self.current_theme]

        self.sidebar_frame.configure(fg_color=theme["sidebar"])

        for widget in self.sidebar_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=theme["button"],
                    hover_color=theme["hover"],
                    text_color=theme["text"]
                )


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    root = ctk.CTk()
    app = CookBookApp(root)
    root.mainloop()
