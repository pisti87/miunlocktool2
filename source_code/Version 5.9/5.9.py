import subprocess
import sys
import os
import hashlib
import random
import time
from datetime import datetime, timezone, timedelta
import tkinter as tk
from tkinter import messagebox
import webbrowser
import re
import threading
import json
import locale

# Проверка и установка библиотек
try:
    import customtkinter as ctk
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        import customtkinter as ctk
    except Exception as e:
        messagebox.showerror(
            "Installation Error",
            f"Failed to install customtkinter:\n{e}\n\n"
            "Try to install manually:\n"
            "pip install customtkinter"
        )
        sys.exit(1)

try:
    import ntplib
    import pytz
    import urllib3
    import statistics
    from icmplib import ping
    import requests
except ImportError as e:
    missing_module = str(e).split("'")[1]
    messagebox.showerror(
        "Import Error",
        f"Failed to import module: {missing_module}\n\n"
        f"Install it with:\n"
        f"pip install {missing_module}"
    )
    sys.exit(1)

# Импортируем модули из папки res
# Для поддержки как обычного Python, так и скомпилированного EXE
try:
    # Для обычного запуска Python
    from res.theme import *
    from res.requests import RequestHandler
    from res.settings import WelcomeWindow, InstructionsWindow, UpdateChecker
    from res.lang import Translation
except ImportError:
    # Для запуска из EXE (когда папка res рядом с exe)
    import sys
    import os

    # Добавляем путь к папке с программой
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    res_path = os.path.join(base_path, 'res')
    if res_path not in sys.path:
        sys.path.insert(0, base_path)  # Добавляем основную папку
        sys.path.insert(0, res_path)  # Добавляем папку res

    # Пробуем импортировать снова
    from theme import *
    from requests import RequestHandler
    from settings import WelcomeWindow, InstructionsWindow, UpdateChecker
    from lang import Translation

# Настройка MD3
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Версия
CURRENT_VERSION = "5.9"

# Конфигурация
if os.name == 'nt':
    CONFIG_DIR = os.path.join(os.environ['APPDATA'], 'MiUnlockTool')
else:
    CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'MiUnlockTool')

CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')
DEBUG_FORCE_WELCOME = False

# Серверы
ntp_servers = [
    "time1.google.com", "time2.google.com", "time3.google.com", "time4.google.com", "time.android.com",
    "time.aws.com", "time.google.com", "time.cloudflare.com",
    "ntp.time.in.ua", "stratum1.net", "ntp5.stratum2.ru"
]

MI_SERVERS = ['sgp-api.buy.mi.com']

os.system('cls' if os.name == 'nt' else 'clear')


def get_system_language():
    try:
        lang = locale.getlocale()[0]
        if lang:
            lang_lower = lang.lower()
            if lang_lower.startswith("ru"):
                return "ru"
            elif lang_lower.startswith("id") or lang_lower.startswith("in") or "indonesian" in lang_lower:
                return "id"
            elif lang_lower.startswith("es") or "spanish" in lang_lower:
                return "es"
            elif lang_lower.startswith("zh") or "chinese" in lang_lower:
                return "zh"
    except Exception:
        pass

    env_lang = (os.environ.get("LANG", "") + os.environ.get("LANGUAGE", "")).lower()
    if "ru" in env_lang:
        return "ru"
    elif "id" in env_lang or "in" in env_lang or "indonesian" in env_lang:
        return "id"
    elif "es" in env_lang or "spanish" in env_lang:
        return "es"
    elif "zh" in env_lang or "chinese" in env_lang:
        return "zh"

    return "en"


def ensure_config_dir():
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)
        return True
    except Exception as e:
        print(f"Ошибка создания папки конфигурации: {e}")
        return False


def load_config():
    system_language = get_system_language()
    default_config = {
        'cookie': '',
        'language': system_language,
        'theme': 'System',
        'skip_cookie_check': False,
        'default_ping': 165,
        'color_theme': 'Material 3',
        'log_to_txt': False,
        'first_run': True,
        'spam_mode': True
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            merged = {**default_config, **config}
            if 'language' in config:
                merged['language'] = config['language']
            return merged
    return default_config


def save_config(config):
    try:
        if not ensure_config_dir():
            return False
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения конфигурации: {e}")
        return False


def _on_key_release(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")


def open_miflash_unlock():
    try:
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        exe_path = os.path.join(
            base_dir,
            "FlashUnlock by ofici5l",
            "MiFlash Unlock.exe"
        )

        if not os.path.exists(exe_path):
            messagebox.showerror(
                "Error",
                f"MiFlash Unlock.exe not found:\n{exe_path}"
            )
            return

        subprocess.Popen(
            [exe_path],
            shell=False,
            cwd=os.path.dirname(exe_path)
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


class XiaomiUnlockTool:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.translation = Translation(self.config.get('language', 'ru'))

        self.instructions_windows = []

        self.root.title(self.translation.tr('title'))
        self.root.geometry("1000x800")
        self.root.minsize(900, 800)
        self.root.maxsize(1200, 880)
        self.root.resizable(True, True)

        self.root.bind_all("<KeyRelease>", _on_key_release, "+")

        self.settings = {
            'full_log': False,
            'skip_cookie_check': self.config.get('skip_cookie_check', False),
            'default_ping': self.config.get('default_ping', 165),
            'theme': self.config.get('theme', 'System'),
            'color_theme': 'Material 3',
            'log_to_txt': self.config.get('log_to_txt', False),
            'spam_mode': self.config.get('spam_mode', True)
        }

        self.cookie_value = ctk.StringVar(value=self.config.get('cookie', ''))
        self.device_id = ctk.StringVar()
        self.status_var = ctk.StringVar(value=self.translation.tr('status_ready'))
        self.ping_var = ctk.StringVar(value=self.translation.tr('ping'))
        self.time_var = ctk.StringVar(value=self.translation.tr('time'))
        self.mode_var = ctk.StringVar(value=self.translation.tr('auto_mode'))
        self.manual_time_var = ctk.StringVar(value="59.1")

        self.cookie_value.trace_add('write', self.auto_save_cookie)

        self.create_material_ui()

        # Инициализируем обработчик запросов
        self.request_handler = RequestHandler(self)

        self.start_beijing_time = None
        self.start_timestamp = None

        self.show_welcome_if_needed()

    def auto_save_cookie(self, *args):
        try:
            self.config['cookie'] = self.cookie_value.get()
            save_config(self.config)
        except Exception as e:
            print(f"Ошибка автосохранения cookie: {e}")

    def show_welcome_if_needed(self):
        first_run = self.config.get('first_run', True)

        if not first_run and not DEBUG_FORCE_WELCOME:
            return

        win = WelcomeWindow(self.root, self.translation)
        self.root.wait_window(win)

        if first_run:
            self.config['first_run'] = False
            self.config['cookie'] = self.cookie_value.get()
            save_config(self.config)

    def save_settings(self):
        """Сохраняет настройки в конфигурационный файл"""
        try:
            # Обновляем конфиг из настроек
            self.config['skip_cookie_check'] = self.settings['skip_cookie_check']
            self.config['default_ping'] = self.settings['default_ping']
            self.config['theme'] = self.settings['theme']
            self.config['language'] = self.settings.get('language', self.translation.language)
            self.config['log_to_txt'] = self.settings['log_to_txt']
            self.config['spam_mode'] = self.settings['spam_mode']
            self.config['cookie'] = self.cookie_value.get()

            # Сохраняем в файл
            save_config(self.config)
            return True
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            return False

    def apply_theme(self, theme: str):
        self.settings['theme'] = theme
        ctk.set_appearance_mode(theme)
        self.update_md3_colors()

    def update_colors(self):
        pass

    def create_material_ui(self):
        dark_mode = ctk.get_appearance_mode() == "Dark"

        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=MaterialColors.get_color('background', dark_mode)
        )
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)

        self.top_bar = MD3Card(self.main_container, elevation=1)
        self.top_bar.pack(fill="x", pady=(0, 20), padx=20)

        top_bar_inner = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        top_bar_inner.pack(fill="x", padx=24, pady=16)

        title_frame = ctk.CTkFrame(top_bar_inner, fg_color="transparent")
        title_frame.pack(side="left", fill="y")

        self.title_label = MD3Label(
            title_frame,
            text=self.translation.tr('main_title'),
            typography='headline_medium'
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = MD3Label(
            title_frame,
            text="https://t.me/miunlocktoolrevamp",
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode)
        )
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        mi_unlock_btn = MD3Button(
            top_bar_inner,
            text="Mi Unlock",
            button_type='outlined',
            size='small',
            command=open_miflash_unlock
        )
        mi_unlock_btn.pack(side="right", padx=(10, 0))

        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20)

        self.left_column = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=400)
        self.left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.right_column = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=400)
        self.right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.params_card = MD3Card(self.left_column, elevation=2)
        self.params_card.pack(fill="both", expand=True)

        card_header = ctk.CTkFrame(self.params_card, fg_color="transparent", height=60)
        card_header.pack(fill="x", padx=24, pady=(24, 0))
        card_header.pack_propagate(False)

        self.params_label = MD3Label(
            card_header,
            text=self.translation.tr('params'),
            typography='title_large'
        )
        self.params_label.pack(side="left")

        card_content = ctk.CTkFrame(self.params_card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=24, pady=16)

        mode_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        mode_frame.pack(fill="x", pady=(0, 16))

        self.mode_label = MD3Label(
            mode_frame,
            text=self.translation.tr('mode_label'),
            typography='label_large'
        )
        self.mode_label.pack(anchor="w", pady=(0, 8))

        self.mode_segmented = MD3SegmentedButton(
            mode_frame,
            values=[self.translation.tr('auto_mode'), self.translation.tr('manual_mode')],
            variable=self.mode_var,
            command=self.toggle_mode
        )
        self.mode_segmented.pack(fill="x")

        self.manual_time_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        self.manual_time_frame.pack(fill="x", pady=(0, 16))

        self.manual_time_label = MD3Label(
            self.manual_time_frame,
            text=self.translation.tr('manual_time_label'),
            typography='label_large'
        )
        self.manual_time_label.pack(anchor="w", pady=(0, 8))

        manual_time_input = ctk.CTkFrame(self.manual_time_frame, fg_color="transparent")
        manual_time_input.pack(fill="x")

        self.manual_time_entry = MD3Entry(
            manual_time_input,
            textvariable=self.manual_time_var,
            placeholder_text="59.1",
            width=120
        )
        self.manual_time_entry.pack(side="left")

        self.manual_time_hint = MD3Label(
            manual_time_input,
            text=self.translation.tr('manual_time_hint'),
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode)
        )
        self.manual_time_hint.pack(side="left", padx=(12, 0))

        cookie_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        cookie_frame.pack(fill="x", pady=(0, 16))

        self.cookie_text_label = MD3Label(
            cookie_frame,
            text=self.translation.tr('cookie_label'),
            typography='label_large'
        )
        self.cookie_text_label.pack(anchor="w", pady=(0, 8))

        self.cookie_entry = MD3Entry(
            cookie_frame,
            textvariable=self.cookie_value,
            placeholder_text="Вставьте ваш токен здесь..."
        )
        self.cookie_entry.pack(fill="x")
        self.cookie_entry.bind("<Return>", lambda event: self.start_process())

        self.info_card = MD3Card(card_content, elevation=1)
        self.info_card.pack(fill="x", pady=(0, 24))

        info_content = ctk.CTkFrame(self.info_card, fg_color="transparent")
        info_content.pack(fill="x", padx=16, pady=16)

        self.info_label = MD3Label(
            info_content,
            text=self.translation.tr('info'),
            typography='title_medium'
        )
        self.info_label.pack(anchor="w", pady=(0, 12))

        status_item = ctk.CTkFrame(info_content, fg_color="transparent")
        status_item.pack(fill="x", pady=(0, 8))

        status_icon = ctk.CTkLabel(
            status_item,
            text="⏳",
            font=("Arial", 16),
            width=24
        )
        status_icon.pack(side="left")

        self.status_text = MD3Label(
            status_item,
            textvariable=self.status_var,
            typography='body_medium'
        )
        self.status_text.pack(side="left", padx=(12, 0))

        ping_item = ctk.CTkFrame(info_content, fg_color="transparent")
        ping_item.pack(fill="x", pady=(0, 8))

        ping_icon = ctk.CTkLabel(
            ping_item,
            text="📶",
            font=("Arial", 16),
            width=24
        )
        ping_icon.pack(side="left")

        self.ping_text = MD3Label(
            ping_item,
            textvariable=self.ping_var,
            typography='body_medium'
        )
        self.ping_text.pack(side="left", padx=(12, 0))

        time_item = ctk.CTkFrame(info_content, fg_color="transparent")
        time_item.pack(fill="x")

        time_icon = ctk.CTkLabel(
            time_item,
            text="🕐",
            font=("Arial", 16),
            width=24
        )
        time_icon.pack(side="left")

        self.time_text = MD3Label(
            time_item,
            textvariable=self.time_var,
            typography='body_medium'
        )
        self.time_text.pack(side="left", padx=(12, 0))

        button_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        button_frame.pack(fill="x")

        action_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_buttons.pack(fill="x", pady=(0, 12))

        self.start_button = MD3Button(
            action_buttons,
            text=self.translation.tr('submit_application'),
            button_type='filled',
            size='large',
            command=self.start_process
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.instructions_button = MD3Button(
            action_buttons,
            text=self.translation.tr('script_info'),
            button_type='outlined',
            size='large',
            command=self.open_instructions
        )
        self.instructions_button.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.exit_button = MD3Button(
            button_frame,
            text=self.translation.tr('exit'),
            button_type='text',
            size='medium',
            command=self.exit_application
        )
        self.exit_button.pack(anchor="e")

        self.log_card = MD3Card(self.right_column, elevation=2)
        self.log_card.pack(fill="both", expand=True)

        log_header = ctk.CTkFrame(self.log_card, fg_color="transparent", height=60)
        log_header.pack(fill="x", padx=24, pady=(24, 0))
        log_header.pack_propagate(False)

        self.log_label = MD3Label(
            log_header,
            text=self.translation.tr('execution_log'),
            typography='title_large'
        )
        self.log_label.pack(side="left")

        log_controls = ctk.CTkFrame(log_header, fg_color="transparent")
        log_controls.pack(side="right")

        self.clear_log_btn = MD3Button(
            log_controls,
            text=self.translation.tr('clear_log_btn'),
            button_type='text',
            size='small',
            command=self.clear_log
        )
        self.clear_log_btn.pack(side="left")

        log_content = ctk.CTkFrame(self.log_card, fg_color="transparent")
        log_content.pack(fill="both", expand=True, padx=24, pady=16)

        log_text_container = ctk.CTkFrame(
            log_content,
            fg_color=MaterialColors.get_color('surface_container_lowest', dark_mode),
            corner_radius=8,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        log_text_container.pack(fill="both", expand=True)

        self.log_text = ctk.CTkTextbox(
            log_text_container,
            wrap="word",
            font=("Consolas", 12),
            fg_color=MaterialColors.get_color('surface_container_lowest', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(
            log_text_container,
            command=self.log_text.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.configure(state='disabled')

        desc_frame = ctk.CTkFrame(self.left_column, fg_color="transparent")
        desc_frame.pack(fill="x", pady=(10, 0))

        self.desc_label = MD3Label(
            desc_frame,
            text=self.translation.tr('desc'),
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode),
            wraplength=400,
            justify="left"
        )
        self.desc_label.pack()

        self.toggle_mode(self.mode_var.get())

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def toggle_mode(self, selected_mode):
        if selected_mode == self.translation.tr('manual_mode'):
            self.manual_time_frame.pack(fill="x", pady=(0, 16))
            self.ping_var.set(self.translation.tr('ping_not_measured_manual'))
            self.desc_label.configure(text=self.translation.tr('desc_manual'))
        else:
            self.manual_time_frame.pack_forget()
            self.ping_var.set(self.translation.tr('ping'))
            self.desc_label.configure(text=self.translation.tr('desc'))

    def update_ui_text(self):
        self.root.title(self.translation.tr('title'))
        self.title_label.configure(text=self.translation.tr('main_title'))

        current_mode = self.mode_var.get()
        is_manual_before_translate = "ручной" in current_mode.lower() or "manual" in current_mode.lower() or "manu" in current_mode.lower() or "手动" in current_mode.lower()

        self.desc_label.configure(
            text=self.translation.tr('desc_manual') if is_manual_before_translate else self.translation.tr('desc'))

        self.params_label.configure(text=self.translation.tr('params'))
        self.mode_label.configure(text=self.translation.tr('mode_label'))

        self.mode_segmented.configure(
            values=[self.translation.tr('auto_mode'), self.translation.tr('manual_mode')]
        )

        if is_manual_before_translate:
            self.mode_var.set(self.translation.tr('manual_mode'))
        else:
            self.mode_var.set(self.translation.tr('auto_mode'))

        self.manual_time_label.configure(text=self.translation.tr('manual_time_label'))
        self.manual_time_hint.configure(text=self.translation.tr('manual_time_hint'))
        self.cookie_text_label.configure(text=self.translation.tr('cookie_label'))
        self.info_label.configure(text=self.translation.tr('info'))
        self.status_var.set(self.translation.tr('status_ready'))

        if is_manual_before_translate:
            self.ping_var.set(self.translation.tr('ping_not_measured_manual'))
        else:
            self.ping_var.set(self.translation.tr('ping'))

        self.time_var.set(self.translation.tr('time'))
        self.log_label.configure(text=self.translation.tr('execution_log'))
        self.clear_log_btn.configure(text=self.translation.tr('clear_log_btn'))
        self.start_button.configure(text=self.translation.tr('submit_application'))
        self.instructions_button.configure(text=self.translation.tr('script_info'))
        self.exit_button.configure(text=self.translation.tr('exit'))

        if self.translation.language == 'ru':
            self.cookie_entry.configure(placeholder_text="Вставьте ваш токен здесь...")
        elif self.translation.language == 'id':
            self.cookie_entry.configure(placeholder_text="Tempel token Anda di sini...")
        elif self.translation.language == 'es':
            self.cookie_entry.configure(placeholder_text="Pegue su token aquí...")
        elif self.translation.language == 'zh':
            self.cookie_entry.configure(placeholder_text="在此粘贴您的令牌...")
        else:
            self.cookie_entry.configure(placeholder_text="Paste your token here...")

        self.manual_time_entry.configure(placeholder_text="59.1")

        self.toggle_mode(self.mode_var.get())

    def update_theme_globally(self):
        theme = self.settings.get('theme', 'System')
        self.apply_theme(theme)

    def update_md3_colors(self):
        dark_mode = ctk.get_appearance_mode() == "Dark"

        self.top_bar.configure(fg_color=MaterialColors.get_color('surface_container', dark_mode))
        self.title_label.configure(
            text_color=MaterialColors.get_color('on_surface', dark_mode)
        )
        self.subtitle_label.configure(
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode)
        )

        self.params_card.configure(fg_color=MaterialColors.get_color('surface_container', dark_mode))
        self.info_card.configure(fg_color=MaterialColors.get_color('surface_container', dark_mode))
        self.log_card.configure(fg_color=MaterialColors.get_color('surface_container', dark_mode))

        text_color = MaterialColors.get_color('on_surface', dark_mode)
        self.params_label.configure(text_color=text_color)
        self.mode_label.configure(text_color=text_color)
        self.manual_time_label.configure(text_color=text_color)
        self.cookie_text_label.configure(text_color=text_color)
        self.info_label.configure(text_color=text_color)
        self.log_label.configure(text_color=text_color)

        bg_color = MaterialColors.get_color('surface_container_lowest', dark_mode)
        border_color = MaterialColors.get_color('outline', dark_mode)

        self.cookie_entry.configure(
            fg_color=bg_color,
            border_color=border_color,
            text_color=text_color
        )

        self.manual_time_entry.configure(
            fg_color=bg_color,
            border_color=border_color,
            text_color=text_color
        )

        self.log_text.configure(
            fg_color=bg_color,
            text_color=text_color,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )

        self.status_text.configure(text_color=text_color)
        self.ping_text.configure(text_color=text_color)
        self.time_text.configure(text_color=text_color)

        self.start_button.configure(
            fg_color=MaterialColors.get_color('primary', dark_mode),
            hover_color=MaterialColors.get_color('primary_container', dark_mode),
            text_color=MaterialColors.get_color('on_primary', dark_mode),
            border_width=0
        )

        self.instructions_button.configure(
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            hover_color=MaterialColors.get_color('surface_container', dark_mode),
            text_color=MaterialColors.get_color('primary', dark_mode),
            border_color=border_color
        )

        self.exit_button.configure(
            fg_color='transparent',
            hover_color=MaterialColors.get_color('surface_container', dark_mode),
            text_color=MaterialColors.get_color('primary', dark_mode),
            border_width=0
        )

        self.clear_log_btn.configure(
            fg_color='transparent',
            hover_color=MaterialColors.get_color('surface_container', dark_mode),
            text_color=MaterialColors.get_color('primary', dark_mode),
            border_width=0
        )

        self.mode_segmented.configure(
            fg_color=MaterialColors.get_color('surface_container', dark_mode),
            selected_color=MaterialColors.get_color('primary', dark_mode),
            selected_hover_color=MaterialColors.get_color('primary_container', dark_mode),
            unselected_color=MaterialColors.get_color('surface_container_low', dark_mode),
            unselected_hover_color=MaterialColors.get_color('surface_container', dark_mode),
            text_color=text_color,
            text_color_disabled=MaterialColors.get_color('on_surface_variant', dark_mode)
        )

        self.main_container.configure(fg_color=MaterialColors.get_color('background', dark_mode))
        self.content_frame.configure(fg_color=MaterialColors.get_color('background', dark_mode))
        self.left_column.configure(fg_color=MaterialColors.get_color('background', dark_mode))
        self.right_column.configure(fg_color=MaterialColors.get_color('background', dark_mode))

        self.desc_label.configure(
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode)
        )

    def exit_application(self):
        self.config['cookie'] = self.cookie_value.get()
        save_config(self.config)
        self.root.destroy()
        sys.exit(0)

    def open_instructions(self):
        instructions_window = InstructionsWindow(self.root, self)
        instructions_window.protocol("WM_DELETE_WINDOW",
                                     lambda: self.on_instructions_close(instructions_window))
        self.instructions_windows.append(instructions_window)

    def on_instructions_close(self, window):
        if window in self.instructions_windows:
            self.instructions_windows.remove(window)
        window.destroy()

    def log_message(self, message, color=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        self.log_text.configure(state="normal")
        self.log_text.insert("end", formatted_message + "\n")

        if color:
            last_line_index = int(self.log_text.index("end-1c").split(".")[0])
            tag_name = f"color_{color}_{last_line_index}"
            self.log_text.tag_add(tag_name, f"end-2l", "end-1c")

            color_map = {
                'green': '#0D904F',
                'red': '#B3261E',
                'blue': '#006C84',
                'orange': '#FF6F00',
            }
            self.log_text.tag_config(tag_name, foreground=color_map.get(color, '#000000'))

        self.log_text.see("end")
        self.log_text.configure(state="disabled")

        # Логирование в файл в той же папке, где находится программа
        try:
            if self.settings.get('log_to_txt', False):
                if not hasattr(self, 'current_log_file') or self.current_log_file is None:
                    # Получаем путь к папке программы
                    if getattr(sys, 'frozen', False):
                        # Если запущено как exe
                        base_dir = os.path.dirname(sys.executable)
                    else:
                        # Если запущено как скрипт
                        base_dir = os.path.dirname(os.path.abspath(__file__))

                    # Формируем имя файла: log_miunlock_ddmmyyyy_hh_mm_ss.txt
                    now = datetime.now()
                    date_str = now.strftime("%d%m%Y_%H_%M_%S")
                    filename = f"log_miunlock_{date_str}.txt"
                    self.current_log_file = os.path.join(base_dir, filename)
                    self._write_log_header()

                with open(self.current_log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message + "\n")
        except Exception as e:
            print(f"Ошибка записи лога: {e}")

    def _write_log_header(self):
        try:
            with open(self.current_log_file, 'w', encoding='utf-8') as f:
                f.write("=== XIAOMI UNLOCK TOOL LOG ===\n")
                f.write(f"Version: {CURRENT_VERSION}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 30 + "\n")
                f.write("SETTINGS:\n")
                f.write(f"Mode: {self.mode_var.get()}\n")
                if self.mode_var.get() == self.translation.tr('auto_mode'):
                    f.write(f"Spam Mode: {self.settings.get('spam_mode')}\n")
                if self.mode_var.get() == self.translation.tr('manual_mode'):
                    f.write(f"Manual Time Target: {self.manual_time_var.get()}\n")
                f.write(f"Default Ping: {self.settings.get('default_ping')}\n")
                f.write(f"Skip Cookie Check: {self.settings.get('skip_cookie_check')}\n")
                f.write(f"Language: {self.translation.language}\n")
                f.write(f"Server List: {MI_SERVERS}\n")
                f.write("=" * 30 + "\n\n")
        except Exception:
            pass

    def wait_until_target_time(self, start_beijing_time, start_timestamp, script_time):
        seconds = int(script_time)
        milliseconds = int((script_time % 1) * 1000)

        target_time = start_beijing_time.replace(
            hour=23,
            minute=59,
            second=seconds,
            microsecond=milliseconds * 1000
        )

        current_time = self.request_handler.get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        if current_time > target_time:
            target_time = target_time + timedelta(days=1)

        if self.mode_var.get() == self.translation.tr('manual_mode'):
            self.log_message(self.translation.tr('target_time_manual').format(
                target_time.strftime('%Y-%m-%d %H:%M:%S.%f')))
        else:
            self.log_message(self.translation.tr('target_time').format(
                target_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                script_time
            ))

        def check_time():
            current_time = self.request_handler.get_synchronized_beijing_time(start_beijing_time, self.start_timestamp)
            time_diff = (target_time - current_time).total_seconds()

            self.time_var.set(
                f"{self.translation.tr('time_synchronized')}: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")

            if time_diff <= 0:
                self.log_message(self.translation.tr('time_reached').format(
                    current_time.strftime('%Y-%m-%d %H:%M:%S.%f')))
                self.request_handler.single_request()
            else:
                self.root.after(100, check_time)

        check_time()

    def start_process(self):
        cookie = self.cookie_value.get().strip()
        if not cookie:
            messagebox.showerror("Error", self.translation.tr('cookie_error'))
            return

        self.current_log_file = None

        self.log_message("\n" + self.translation.tr('unlock_process'))
        self.status_var.set(self.translation.tr('unlock_process'))

        device_id = self.request_handler.generate_device_id()

        if not self.request_handler.check_unlock_status(cookie, device_id):
            return

        self.start_beijing_time = self.request_handler.get_initial_beijing_time()
        if self.start_beijing_time is None:
            messagebox.showerror("Error", self.translation.tr('time_error'))
            return

        self.start_timestamp = time.time()

        if self.mode_var.get() == self.translation.tr('auto_mode'):
            if self.settings.get('spam_mode', True):
                self.log_message(self.translation.tr('log_auto_mode_spam_selected'), color="blue")
            else:
                self.log_message(self.translation.tr('log_auto_mode_single_selected'), color="blue")
            self.wait_for_presync_time()
        else:
            self.log_message(self.translation.tr('log_manual_mode_selected'), color="blue")
            self.start_manual_mode()

    def wait_for_presync_time(self):
        """Ожидание времени для синхронизации"""
        current_time = self.request_handler.get_synchronized_beijing_time(self.start_beijing_time, self.start_timestamp)
        current_hour = current_time.hour
        current_minute = current_time.minute

        # Определяем время следующей синхронизации
        if current_hour < 23 or (current_hour == 23 and current_minute < 58):
            # До 23:58 - синхронизация в 23:58
            target_sync_time = self.start_beijing_time.replace(hour=23, minute=58, second=0, microsecond=0)
            sync_type = "normal"
        elif current_hour == 23 and current_minute < 59:
            # Между 23:58 и 23:59 - синхронизация в 23:59:30
            target_sync_time = self.start_beijing_time.replace(hour=23, minute=59, second=30, microsecond=0)
            sync_type = "late"
        else:
            # После 23:59 - немедленная синхронизация
            self.log_message(self.translation.tr('log_time_gt_2355'), color="blue")
            new_time = self.request_handler.get_initial_beijing_time()
            if new_time:
                self.start_beijing_time = new_time
                self.start_timestamp = time.time()
                self.log_message(self.translation.tr('log_time_sync_success'), color="green")

            if self.settings.get('spam_mode', True):
                self.start_spam_attack()
            else:
                self.start_auto_single_request()
            return

        self.log_message(self.translation.tr('log_presync_wait').format(
            target_sync_time.strftime('%H:%M:%S')), color="blue")
        self.status_var.set(self.translation.tr('status_presync_wait').format(
            target_sync_time.strftime('%H:%M')))

        def check_presync():
            current_time = self.request_handler.get_synchronized_beijing_time(self.start_beijing_time,
                                                                              self.start_timestamp)
            self.time_var.set(
                f"{self.translation.tr('time_synchronized')}: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")

            if current_time >= target_sync_time:
                self.log_message(self.translation.tr('log_presync_start'), color="blue")

                new_time = self.request_handler.get_initial_beijing_time()
                if new_time:
                    self.start_beijing_time = new_time
                    self.start_timestamp = time.time()
                    self.log_message(self.translation.tr('log_time_updated').format(
                        new_time.strftime('%H:%M:%S.%f')), color="green")
                else:
                    self.log_message(self.translation.tr('log_resync_error'), color="red")

                if self.settings.get('spam_mode', True):
                    self.start_spam_attack()
                else:
                    self.start_auto_single_request()
            else:
                self.root.after(500, check_presync)

        check_presync()

    def start_spam_attack(self):
        """Запуск спам-атаки с исправленными временами"""
        # Исправленные времена для более ранней отправки
        spam_times = [58.2, 58.4, 58.7, 59.0, 59.3]  # Сдвинули немного раньше
        device_ids = [self.request_handler.generate_device_id() for _ in spam_times]
        base_time = self.start_beijing_time.replace(hour=23, minute=59, second=0, microsecond=0)

        attack_times = []
        for offset in spam_times:
            # Отправляем за 0.2 секунды до цели, чтобы компенсировать задержки
            attack_time = base_time + timedelta(seconds=offset - 0.2)
            attack_times.append((offset, attack_time))

        self.log_message(self.translation.tr('log_spam_mode_targets').format(spam_times), color="blue")
        self.status_var.set(self.translation.tr('status_spam_wait'))

        for seq_num, ((offset_val, target_time), device_id) in enumerate(zip(attack_times, device_ids), 1):
            threading.Thread(
                target=self.schedule_spam_request,
                args=(seq_num, offset_val, target_time, device_id),
                daemon=True
            ).start()

    def schedule_spam_request(self, seq_num, offset_val, target_time, device_id):
        """Планирует отправку спам-запроса на конкретное время с более точным таймингом"""
        while True:
            current_time = self.request_handler.get_synchronized_beijing_time(self.start_beijing_time,
                                                                              self.start_timestamp)
            time_diff = (target_time - current_time).total_seconds()

            if time_diff <= 0:
                self.log_message(self.translation.tr('log_spam_sending_at').format(seq_num, f"{offset_val:.1f}"),
                                 color="orange")
                self.request_handler.make_single_request_with_new_device_id(seq_num, offset_val, device_id)
                break
            elif time_diff > 0.05:
                # Если больше 50 мс, ждем 10 мс
                time.sleep(0.01)
            else:
                # Если меньше 50 мс, ждем 1 мс для более точной отправки
                time.sleep(0.001)

    def start_auto_single_request(self):
        self.log_message(self.translation.tr('log_normal_mode_ping'), color="blue")
        ping = self.request_handler.get_average_ping()
        if ping is None:
            ping = self.settings['default_ping']

        script_time = self.request_handler.calculate_script_time(ping)

        self.log_message(self.translation.tr('log_calculated_send_time').format(f"{script_time:.3f}"), color="blue")
        self.wait_until_target_time(self.start_beijing_time, self.start_timestamp, script_time)

    def start_manual_mode(self):
        try:
            script_time = float(self.manual_time_var.get())
            if script_time < 0 or script_time > 60:
                self.log_message(self.translation.tr('manual_time_error'))
                messagebox.showerror("Error", self.translation.tr('manual_time_error'))
                return
            self.log_message(self.translation.tr('manual_mode_start').format(script_time))
        except ValueError as e:
            self.log_message(f"Error: {e}")
            messagebox.showerror("Error", self.translation.tr('manual_time_error'))
            return

        self.wait_until_target_time(self.start_beijing_time, self.start_timestamp, script_time)


def main():
    root = ctk.CTk()
    app = XiaomiUnlockTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Зуммерские зуммеры зуммерочки занимаются зуммерской программой для зуммерской разблокировки зуммерского зарузчика на зуммерском телефоне Xiaomi/Redmi/Poco