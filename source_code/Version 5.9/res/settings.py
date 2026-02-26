import sys
import os
import json
import webbrowser
import threading
import re
from tkinter import messagebox
import customtkinter as ctk

# Импортируем компоненты из theme
from .theme import (
    MaterialColors, MD3Card, MD3Label, MD3Button,
    MD3Entry, MD3Switch, MaterialTypography
)

# Функции для работы с конфигом нужно передавать из главного скрипта
import sys
import os

# Версия и URL для обновлений
GITHUB_REPO_URL = "https://github.com/AsInsideOut/miunlocktool/releases/tag/Stable"


# Функция для получения текущей версии
def get_current_version():
    try:
        # Пытаемся получить из глобальной переменной
        import __main__
        if hasattr(__main__, 'CURRENT_VERSION'):
            return __main__.CURRENT_VERSION
    except:
        pass
    return "5.9"


class UpdateChecker:
    @staticmethod
    def get_current_version():
        return get_current_version()

    @staticmethod
    def extract_version_number(version_str):
        if not version_str:
            return None
        match = re.search(r'(\d+\.\d+)', str(version_str))
        return match.group(1) if match else None

    @staticmethod
    def compare_versions(version1, version2):
        try:
            v1_parts = list(map(int, version1.split('.')))
            v2_parts = list(map(int, version2.split('.')))

            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))

            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            return 0
        except Exception:
            return 0

    @staticmethod
    def check_for_updates():
        try:
            import requests
            current_version = UpdateChecker.get_current_version()
            current_num = UpdateChecker.extract_version_number(current_version)

            if not current_num:
                return None, "Не удалось определить текущую версию"

            api_url = "https://api.github.com/repos/AsInsideOut/miunlocktool/releases"
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    releases = response.json()
                    if releases:
                        latest_release = releases[0]
                        latest_tag = latest_release.get('tag_name', '')
                        latest_num = UpdateChecker.extract_version_number(latest_tag)

                        if latest_num and UpdateChecker.compare_versions(latest_num, current_num) > 0:
                            return latest_num, latest_tag
                        else:
                            return None, "Текущая версия актуальна"
            except requests.RequestException:
                pass

            version_parts = current_num.split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1])

            for i in range(1, 3):
                next_minor = minor + i
                test_version = f"{major}.{next_minor}"
                test_url = f"{GITHUB_REPO_URL}{test_version}"

                try:
                    response = requests.head(test_url, timeout=5)
                    if response.status_code == 200:
                        return test_version, f"Stable{test_version}"
                except requests.RequestException:
                    continue

            return None, "Текущая версия актуальна"

        except Exception as e:
            return None, f"Ошибка при проверке: {str(e)}"


class WelcomeWindow(ctk.CTkToplevel):
    def __init__(self, parent, translation):
        super().__init__(parent)
        self.translation = translation

        self.update_idletasks()
        self.title(self.translation.tr('welcome_title'))
        self.geometry("600x500")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()
        self.attributes("-topmost", True)

        dark_mode = ctk.get_appearance_mode() == "Dark"

        main_container = ctk.CTkFrame(
            self,
            fg_color=MaterialColors.get_color('surface_container', dark_mode),
            corner_radius=12
        )
        main_container.pack(fill="both", expand=True, padx=0, pady=0)

        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=30, pady=(30, 10))
        header_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            header_frame,
            text="🔓",
            font=("Arial", 48),
            text_color=MaterialColors.get_color('primary', dark_mode)
        )
        icon_label.pack(side="left", padx=(0, 20))

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y", expand=True)

        title_label = MD3Label(
            title_frame,
            text="Xiaomi Unlock Tool",
            typography='headline_large'
        )
        title_label.pack(anchor="w")

        version_label = MD3Label(
            title_frame,
            text=f"Version {UpdateChecker.get_current_version()}",
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode)
        )
        version_label.pack(anchor="w", pady=(5, 0))

        text_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=30, pady=20)

        welcome_text = self.translation.tr('welcome_text')

        text_widget = ctk.CTkTextbox(
            text_frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            height=200
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", welcome_text)
        text_widget.configure(state="disabled")

        button_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=60)
        button_frame.pack(fill="x", padx=30, pady=(0, 30))
        button_frame.pack_propagate(False)

        continue_button = MD3Button(
            button_frame,
            text=self.translation.tr('welcome_btn'),
            button_type='filled',
            size='large',
            command=self._on_ok
        )
        continue_button.pack(fill="x")

        self.protocol("WM_DELETE_WINDOW", self._on_ok)

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _on_ok(self):
        self.grab_release()
        self.destroy()


class InstructionsWindow(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.translation = app.translation

        self.title(self.translation.tr('instructions_title'))
        self.geometry("950x750")
        self.minsize(900, 750)
        self.resizable(True, True)
        self.update_idletasks()
        self.grab_set()

        self.skip_cookie_check_var = ctk.BooleanVar(
            value=self.app.settings.get('skip_cookie_check', False)
        )
        self.default_ping_var = ctk.StringVar(
            value=str(self.app.settings.get('default_ping', 165))
        )
        self.theme_var = ctk.StringVar(
            value=self.app.settings.get('theme', 'System')
        )
        self.language_var = ctk.StringVar(
            value=self.app.translation.language
        )
        self.log_to_txt_var = ctk.BooleanVar(
            value=self.app.settings.get('log_to_txt', False)
        )
        self.spam_mode_var = ctk.BooleanVar(
            value=self.app.settings.get('spam_mode', True)
        )

        self.skip_cookie_check_var.trace_add('write', self.auto_save_settings)
        self.default_ping_var.trace_add('write', self.auto_save_settings)
        self.theme_var.trace_add('write', self.on_theme_changed)
        self.language_var.trace_add('write', self.on_language_changed)
        self.log_to_txt_var.trace_add('write', self.auto_save_settings)
        self.spam_mode_var.trace_add('write', self.auto_save_settings)

        self.cookies_expanded = False
        self._is_updating = False
        self.current_content_provider = None

        self._create_layout()
        self._create_sidebar_buttons()

        self.show_about_content()

    def _recreate_ui(self):
        """Уничтожает и заново создает все виджеты в этом окне, чтобы отразить изменения темы/языка."""
        provider_func = self.current_content_provider
        cookies_expanded_state = self.cookies_expanded

        for widget in self.winfo_children():
            widget.destroy()

        self._create_layout()
        self._create_sidebar_buttons()

        if cookies_expanded_state:
            self.toggle_cookies_section()

        if provider_func:
            self.title(self.translation.tr('instructions_title'))
            provider_func()
        else:
            self.show_about_content()

    def on_language_changed(self, *args):
        if self._is_updating:
            return

        new_lang = self.language_var.get()
        if new_lang == self.app.translation.language:
            return

        self._is_updating = True
        try:
            self.app.translation.language = new_lang
            self.app.settings['language'] = new_lang
            # Используем функцию сохранения из главного приложения
            self.app.save_settings()

            self.app.update_ui_text()

            self._recreate_ui()

        finally:
            self._is_updating = False

    def on_theme_changed(self, *args):
        if self._is_updating:
            return

        self._is_updating = True
        try:
            theme = self.theme_var.get()
            self.app.settings['theme'] = theme
            self.auto_save_settings()

            self.app.apply_theme(theme)

            self._recreate_ui()

        finally:
            self._is_updating = False

    def auto_save_settings(self, *args):
        if self._is_updating:
            return

        self._is_updating = True
        try:
            try:
                ping_value = int(self.default_ping_var.get())
                if ping_value <= 0:
                    self._is_updating = False
                    return
                self.app.settings['default_ping'] = ping_value
            except ValueError:
                self._is_updating = False
                return

            self.app.settings['skip_cookie_check'] = self.skip_cookie_check_var.get()
            self.app.settings['log_to_txt'] = self.log_to_txt_var.get()
            self.app.settings['spam_mode'] = self.spam_mode_var.get()
            self.app.settings['theme'] = self.theme_var.get()
            self.app.settings['language'] = self.language_var.get()

            # Используем функцию сохранения из главного приложения
            self.app.save_settings()

            self.app.log_message(self.translation.tr('settings_saved'))
            self.app.log_message(
                self.translation.tr('cookie_check').format(
                    "Disabled" if self.skip_cookie_check_var.get() else "Enabled"
                )
            )
            self.app.log_message(
                self.translation.tr('default_ping').format(self.app.settings['default_ping'])
            )

        except Exception as e:
            print(f"Ошибка автосохранения настроек: {e}")
        finally:
            self._is_updating = False

    def get_current_theme(self):
        return self.theme_var.get()

    def _create_layout(self):
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=MaterialColors.get_color('background', dark_mode)
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.sidebar_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=MaterialColors.get_color('surface_container', dark_mode),
            width=230
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=MaterialColors.get_color('background', dark_mode)
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        self.header_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=MaterialColors.get_color('primary', dark_mode)
        )
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.translation.tr('instructions_title'),
            font=("Arial", 20, "bold"),
            text_color=MaterialColors.get_color('on_primary', dark_mode),
            fg_color=MaterialColors.get_color('primary', dark_mode)
        )
        self.title_label.pack(pady=12)

        self.content_area = ctk.CTkFrame(
            self.content_frame,
            fg_color=MaterialColors.get_color('background', dark_mode)
        )
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)

    def _create_sidebar_buttons(self):
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")
        button_font = ("Arial", 16, "bold")
        button_height = 48
        sidebar_bg = MaterialColors.get_color('surface_container', dark_mode)
        text_color = MaterialColors.get_color('on_surface', dark_mode)

        self.about_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('about_title'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_about_content
        )
        self.about_btn.pack(fill="x", padx=12, pady=(20, 8))

        self.general_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('general_title'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_general_content
        )
        self.general_btn.pack(fill="x", padx=12, pady=8)

        # Объединенная кнопка для получения cookies
        self.cookies_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('cookies_title'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_cookies_content
        )
        self.cookies_btn.pack(fill="x", padx=12, pady=8)

        self.trouble_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('trouble_title'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_trouble_content
        )
        self.trouble_btn.pack(fill="x", padx=12, pady=8)

        self.authors_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('authors_title'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_authors_content
        )
        self.authors_btn.pack(fill="x", padx=12, pady=8)

        self.settings_btn = ctk.CTkButton(
            self.sidebar_frame,
            text=self.translation.tr('settings'),
            font=button_font,
            height=button_height,
            fg_color=sidebar_bg,
            hover_color=MaterialColors.get_color('primary', dark_mode),
            text_color=text_color,
            corner_radius=10,
            border_width=2,
            border_color=MaterialColors.get_color('outline', dark_mode),
            anchor="w",
            command=self.show_settings_content
        )
        self.settings_btn.pack(fill="x", padx=12, pady=(8, 12))

    def clear_content_area(self):
        for w in self.content_area.winfo_children():
            w.destroy()
        self.about_text = None
        self.general_text = None
        self.cookies_text = None
        self.trouble_text = None
        self.authors_text = None
        self.settings_frame = None

    def show_about_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_about_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        frame.pack(fill="both", expand=True)

        self.about_text = ctk.CTkTextbox(
            frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            cursor="arrow"
        )
        self.about_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.about_text.insert("1.0", self.translation.tr('about_content'))
        self.about_text.configure(state="disabled")

    def show_general_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_general_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        frame.pack(fill="both", expand=True)

        self.general_text = ctk.CTkTextbox(
            frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            cursor="arrow"
        )
        self.general_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.general_text.insert("1.0", self.translation.tr('general_content'))
        self.general_text.configure(state="disabled")

    def show_cookies_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_cookies_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        frame.pack(fill="both", expand=True)

        # Объединенный текст для получения cookies
        if self.translation.language == 'ru':
            cookies_text = """Получение токена

Инструкция для всех браузеров:

1. Скачайте расширение Cookie Editor

2. Авторизуйтесь в аккаунт, предварительно
выйдя из него, на сайте Mi Community
http://new.c.mi.com/global


3. В окне Cookie Editor извлеките
New_bbs_ServiceToken и скопируйте его

Особенности работы:

1. Все время в скрипте является Пекинским
2. Регион в Mi Community стоит Global"""

        elif self.translation.language == 'id':
            cookies_text = """Mendapatkan token

Instruksi untuk semua browser:

1. Unduh ekstensi Cookie Editor

2. Masuk ke akun Anda (setelah keluar)
   di situs web Mi Community
   http://new.c.mi.com/global

3. Di jendela Cookie Editor, ekstrak
   New_bbs_ServiceToken dan salin

Catatan penting:

1. Semua waktu dalam skrip adalah waktu Beijing
2. Region akun Mi Community diatur ke Global"""

        elif self.translation.language == 'es':
            cookies_text = """Obteniendo token

Instrucciones para todos los navegadores:

1. Descargue la extensión Cookie Editor

2. Inicie sesión en su cuenta (después de cerrar sesión)
   en el sitio web de Mi Community
   http://new.c.mi.com/global

3. En la ventana de Cookie Editor, extraiga
   New_bbs_ServiceToken y cópielo

Notas importantes:

1. Todas las horas en el script son hora de Pekín
2. La región en Mi Community está configurada como Global"""

        elif self.translation.language == 'zh':
            cookies_text = """获取令牌

所有浏览器的说明：

1. 下载Cookie Editor扩展

2. 登录您的账户（先退出）
   在小米社区网站
   http://new.c.mi.com/global

3. 在Cookie Editor窗口中提取
   New_bbs_ServiceToken并复制

重要说明：

1. 脚本中的所有时间均为北京时间
2. Mi Community区域设置为全球"""

        else:  # English
            cookies_text = """Getting token

1. Download the Cookie Editor extension

2. Log in to your account (after logging out)
   on the Mi Community website
   http://new.c.mi.com/global

3. In the Cookie Editor window, extract
   New_bbs_ServiceToken and copy it

Important notes:

1. All times in the script are Beijing time
2. Region in Mi Community is set to Global"""

        self.cookies_text = ctk.CTkTextbox(
            frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            cursor="arrow"
        )
        self.cookies_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.cookies_text.insert("1.0", cookies_text)
        self.cookies_text.configure(state="disabled")

    def show_trouble_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_trouble_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        frame.pack(fill="both", expand=True)

        self.trouble_text = ctk.CTkTextbox(
            frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            cursor="arrow"
        )
        self.trouble_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.trouble_text.insert("1.0", self.translation.tr('trouble_content'))
        self.trouble_text.configure(state="disabled")

    def show_authors_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_authors_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        frame.pack(fill="both", expand=True)

        self.authors_text = ctk.CTkTextbox(
            frame,
            wrap="word",
            font=MaterialTypography.BODY_MEDIUM,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode),
            border_width=0,
            cursor="arrow"
        )
        self.authors_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.authors_text.insert("1.0", self.translation.tr('authors_content'))
        self.authors_text.configure(state="disabled")

    def show_settings_content(self):
        self.clear_content_area()
        self.current_content_provider = self.show_settings_content
        dark_mode = self.get_current_theme() == "Dark" or (
                    self.get_current_theme() == "System" and ctk.get_appearance_mode() == "Dark")

        self.settings_frame = MD3Card(
            self.content_area,
            fg_color=MaterialColors.get_color('surface_container_low', dark_mode),
            corner_radius=12,
            border_width=1,
            border_color=MaterialColors.get_color('outline_variant', dark_mode)
        )
        self.settings_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Map system theme names to translated theme names
        theme_map = {
            'System': self.translation.tr('theme_system'),
            'Light': self.translation.tr('theme_light'),
            'Dark': self.translation.tr('theme_dark')
        }

        def theme_command(choice):
            for system_name, translated_name in theme_map.items():
                if choice == translated_name:
                    self.theme_var.set(system_name)
                    break

        # Тема
        theme_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        theme_frame.pack(fill="x", pady=10, padx=18)

        theme_label_widget = MD3Label(
            theme_frame,
            text=self.translation.tr('theme_label'),
            typography='label_large'
        )
        theme_label_widget.pack(anchor="w", pady=(8, 4))

        theme_optionmenu = ctk.CTkOptionMenu(
            theme_frame,
            values=list(theme_map.values()),
            command=theme_command,
            width=200,
            height=34,
            font=("Arial", 14),
            fg_color=MaterialColors.get_color('surface_container', dark_mode),
            button_color=MaterialColors.get_color('primary', dark_mode),
            button_hover_color=MaterialColors.get_color('primary_container', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode)
        )
        theme_optionmenu.set(theme_map[self.theme_var.get()])
        theme_optionmenu.pack(anchor="w", pady=(0, 8))

        # Язык
        language_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        language_frame.pack(fill="x", pady=10, padx=18)

        language_label_widget = MD3Label(
            language_frame,
            text=self.translation.tr('language_label'),
            typography='label_large'
        )
        language_label_widget.pack(anchor="w", pady=(8, 4))

        # Добавляем испанский и китайский языки
        language_optionmenu = ctk.CTkOptionMenu(
            language_frame,
            values=['ru', 'en', 'id', 'es', 'zh'],
            variable=self.language_var,
            width=200,
            height=34,
            font=("Arial", 14),
            fg_color=MaterialColors.get_color('surface_container', dark_mode),
            button_color=MaterialColors.get_color('primary', dark_mode),
            button_hover_color=MaterialColors.get_color('primary_container', dark_mode),
            text_color=MaterialColors.get_color('on_surface', dark_mode)
        )
        language_optionmenu.pack(anchor="w", pady=(0, 8))

        # Проверка cookie
        skip_check_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        skip_check_frame.pack(fill="x", pady=10, padx=18)

        cookie_checkbox = MD3Switch(
            skip_check_frame,
            text=self.translation.tr('cookie_checkbox'),
            variable=self.skip_cookie_check_var
        )
        cookie_checkbox.pack(anchor="w", pady=8)

        # Логирование в TXT
        log_to_txt_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        log_to_txt_frame.pack(fill="x", pady=10, padx=18)

        log_to_txt_checkbox = MD3Switch(
            log_to_txt_frame,
            text=self.translation.tr('log_to_txt_checkbox'),
            variable=self.log_to_txt_var
        )
        log_to_txt_checkbox.pack(anchor="w", pady=8)

        # Режим спама
        spam_mode_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        spam_mode_frame.pack(fill="x", pady=10, padx=18)

        spam_mode_checkbox = MD3Switch(
            spam_mode_frame,
            text=self.translation.tr('spam_mode_checkbox'),
            variable=self.spam_mode_var
        )
        spam_mode_checkbox.pack(anchor="w", pady=(8, 4))

        spam_mode_desc_label = MD3Label(
            spam_mode_frame,
            text=self.translation.tr('spam_mode_desc'),
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode),
            wraplength=400,
            justify="left"
        )
        spam_mode_desc_label.pack(anchor="w", pady=(0, 8))

        # Пинг
        ping_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        ping_frame.pack(fill="x", pady=10, padx=18)

        ping_top_frame = ctk.CTkFrame(
            ping_frame,
            fg_color="transparent"
        )
        ping_top_frame.pack(fill="x", pady=(0, 4))

        ping_label_widget = MD3Label(
            ping_top_frame,
            text=self.translation.tr('ping_label'),
            typography='label_large'
        )
        ping_label_widget.pack(side="left", pady=(0, 0))

        ping_entry = MD3Entry(
            ping_frame,
            textvariable=self.default_ping_var,
            width=150,
            height=36
        )
        ping_entry.pack(anchor="w", pady=(0, 4))

        ping_note_label = MD3Label(
            ping_frame,
            text=self.translation.tr('ping_note'),
            typography='body_small',
            text_color=MaterialColors.get_color('on_surface_variant', dark_mode),
            wraplength=400,
            justify="left"
        )
        ping_note_label.pack(anchor="w", pady=(0, 8))

        # Версия (с кнопкой обновлений)
        update_frame = ctk.CTkFrame(
            self.settings_frame,
            fg_color="transparent"
        )
        update_frame.pack(fill="x", pady=10, padx=18)

        current_ver_label = MD3Label(
            update_frame,
            text=self.translation.tr('current_version').format(UpdateChecker.get_current_version()),
            typography='label_large'
        )
        current_ver_label.pack(anchor="w", pady=(8, 4))

        self.update_button = MD3Button(
            update_frame,
            text=self.translation.tr('check_updates'),
            command=self.check_updates,
            button_type='outlined',
            size='small'
        )
        self.update_button.pack(anchor="w", pady=(0, 8))

    def check_updates(self):
        self.update_button.configure(
            state="disabled",
            text=self.translation.tr('update_checking')
        )

        def worker():
            latest_version, message = UpdateChecker.check_for_updates()

            def finish():
                self.update_button.configure(
                    state="normal",
                    text=self.translation.tr('check_updates')
                )
                if latest_version:
                    self.show_update_dialog(latest_version, message)
                else:
                    messagebox.showinfo(
                        self.translation.tr('update_not_available'),
                        f"{self.translation.tr('current_version').format(UpdateChecker.get_current_version())} {message}"
                    )

            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    def show_update_dialog(self, latest_version, message):
        update_url = f"{GITHUB_REPO_URL}{latest_version}"

        dialog = ctk.CTkToplevel(self)
        dialog.title(self.translation.tr('update_available'))
        dialog.geometry("420x210")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self)

        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        msg_lbl = ctk.CTkLabel(
            frame,
            text=self.translation.tr('update_message').format(latest_version),
            font=("Arial", 14),
            wraplength=360,
            justify="left"
        )
        msg_lbl.pack(pady=(10, 16))

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", pady=(8, 0))

        def open_update():
            webbrowser.open(update_url)
            dialog.destroy()

        def close_dialog():
            dialog.destroy()

        update_btn = MD3Button(
            btns,
            text=self.translation.tr('update_btn_update'),
            command=open_update,
            button_type='filled',
            size='small'
        )
        update_btn.pack(side="right", padx=(10, 0))

        ok_btn = MD3Button(
            btns,
            text=self.translation.tr('update_btn_ok'),
            command=close_dialog,
            button_type='outlined',
            size='small'
        )
        ok_btn.pack(side="right")

    def destroy(self):
        current_theme = self.app.settings.get('theme', 'System')
        self.app.apply_theme(current_theme)
        super().destroy()