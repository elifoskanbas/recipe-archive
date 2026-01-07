import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from texts import texts
import json
import os

# File used to store application settings
SETTINGS_FILE = 'app_settings.json'


def load_settings():
    """Load settings from file"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get('language', 'en')
        except:
            return 'en'
    return 'en'


def save_settings_to_file(language):
    """Save settings to file"""
    settings = {'language': language}
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_lang():
    """Return current language"""
    return load_settings()


def show_settings(parent_frame, language, on_language_change=None):
    """Display the settings screen"""
    current_lang = language

    # Clear the parent frame
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # ---------- MAIN CONTAINER ----------
    container = ctk.CTkFrame(
        parent_frame,
        fg_color=("#FFF8F0", "#2a2a2a")
    )
    container.pack(fill="both", expand=True, padx=40, pady=40)

    # ---------- TITLE ----------
    title_label = ctk.CTkLabel(
        container,
        text="⚙️ " + ("Ayarlar" if current_lang == "tr" else "Settings"),
        font=ctk.CTkFont(size=32, weight="bold"),
        text_color=("#1F2937", "#FFFFFF")
    )
    title_label.pack(anchor="w", pady=(0, 30))

    # ---------- LANGUAGE CARD ----------
    lang_card = ctk.CTkFrame(
        container,
        fg_color=("#FFF8F0", "#2a2a2a"),
        corner_radius=18,
        border_width=1,
        border_color=("#E0D6C8", "#3F3F3F")
    )
    lang_card.pack(fill="x", pady=15)

    lang_inner = ctk.CTkFrame(
        lang_card,
        fg_color="transparent"
    )
    lang_inner.pack(fill="x", padx=30, pady=30)

    # Language title
    language_title = ctk.CTkLabel(
        lang_inner,
        text=texts[current_lang]["language_label"],
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=("#1F2937", "#FFFFFF")
    )
    language_title.pack(anchor="w", pady=(0, 10))

    # Language description
    lang_desc = ctk.CTkLabel(
        lang_inner,
        text=("Uygulama dilini seçin / Select application language"
              if current_lang == "tr"
              else "Select application language"),
        font=ctk.CTkFont(size=13),
        text_color=("#7A6F64", "#B0B0B0")
    )
    lang_desc.pack(anchor="w", pady=(0, 20))

    # ---------- LANGUAGE SELECTION ----------
    lang_selection_frame = ctk.CTkFrame(
        lang_inner,
        fg_color="transparent"
    )
    lang_selection_frame.pack(anchor="w", pady=10)

    language_var = tk.StringVar(value=current_lang)

    en_radio = ctk.CTkRadioButton(
        lang_selection_frame,
        text="🇬🇧 English",
        variable=language_var,
        value="en",
        font=ctk.CTkFont(size=14),
        text_color=("#1F2937", "#FFFFFF")
    )
    en_radio.pack(anchor="w", pady=8)

    tr_radio = ctk.CTkRadioButton(
        lang_selection_frame,
        text="🇹🇷 Türkçe",
        variable=language_var,
        value="tr",
        font=ctk.CTkFont(size=14),
        text_color=("#1F2937", "#FFFFFF")
    )
    tr_radio.pack(anchor="w", pady=8)

    # ---------- SAVE BUTTON ----------
    button_frame = ctk.CTkFrame(container, fg_color="transparent")
    button_frame.pack(anchor="w", pady=(30, 0))

    def save_and_reload():
        new_lang = language_var.get()

        save_settings_to_file(new_lang)

        messagebox.showinfo(
            "✓ " + ("Başarılı" if new_lang == "tr" else "Success"),
            ("Dil ayarı kaydedildi!\nDeğişiklikler uygulandı."
             if new_lang == "tr"
             else "Language setting saved!\nChanges applied.")
        )

        if on_language_change:
            on_language_change(new_lang)

    save_button = ctk.CTkButton(
        button_frame,
        text=texts[current_lang]["save_btn"],
        command=save_and_reload,
        font=ctk.CTkFont(size=16, weight="bold"),
        height=45,
        corner_radius=12,
        fg_color="#FF8C00",
        hover_color="#FF7000",
        text_color="white",
    )
    save_button.pack(side="left", padx=5)
