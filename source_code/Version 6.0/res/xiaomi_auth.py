import customtkinter as ctk

from .theme import MD3Card, MD3Label, MD3Button, MD3Entry, MaterialColors


class XiaomiAuthDialog(ctk.CTkToplevel):
    def __init__(self, parent, translation, config):
        super().__init__(parent)
        self.parent = parent
        self.translation = translation
        self.config = config

        coming_soon_text = self._get_coming_soon_text()

        self.title(self.translation.tr('login_title'))
        self.geometry("400x320")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        self.token = None
        self.success = False
        self.error_message = None

        self.create_ui(coming_soon_text)

        self.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() - self.winfo_width()) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def _get_coming_soon_text(self):
        lang = self.translation.language
        texts = {
            'ru': "Скоро появится",
            'en': "Coming Soon",
            'id': "Segera Hadir",
            'es': "Próximamente",
            'zh': "即将推出",
            'pt': "Em Breve"
        }
        return texts.get(lang, "Coming Soon")

    def create_ui(self, coming_soon_text):
        dark_mode = ctk.get_appearance_mode() == "Dark"

        main_frame = ctk.CTkFrame(
            self,
            fg_color=MaterialColors.get_color('background', dark_mode)
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        icon_label = ctk.CTkLabel(
            main_frame,
            text="🔧",
            font=("Arial", 64),
            text_color=MaterialColors.get_color('primary', dark_mode)
        )
        icon_label.pack(pady=(20, 10))

        coming_label = MD3Label(
            main_frame,
            text=coming_soon_text,
            typography='headline_medium'
        )
        coming_label.pack(pady=(10, 20))

        info_label = MD3Label(
            main_frame,
            text=self.translation.tr('login_token_extract_error'),
            typography='body_medium',
            wraplength=350,
            justify="center"
        )
        info_label.pack(pady=(0, 30))

        close_btn = MD3Button(
            main_frame,
            text=self.translation.tr('close_btn'),
            button_type='filled',
            command=self.destroy
        )
        close_btn.pack(pady=(0, 20))